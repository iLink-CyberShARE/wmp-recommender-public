import numpy as np
import pandas as pd
from ..database import settings
from app.main.model.item import Item
from app.main.model.role import Role
from app.main.model.implicit_log import Implicit_log
from lightfm.data import Dataset
from lightfm.cross_validation import random_train_test_split
from app.main.database import db_session, engine

# we will ignore pandas warning 
import warnings
warnings.filterwarnings('ignore')

class PreprocessHandler:
    '''
    The pre-process handler extracts training data from database and prepares for LightFM consumption.
    References:
    https://github.com/lyst/lightfm/tree/master/examples/dataset
    https://www.kaggle.com/niyamatalmass/lightfm-hybrid-recommendation-system
    https://making.lyst.com/lightfm/docs/index.html
    '''

    def __init__(self, model_id):

        # training flags for recommendation level
        self.model_id = model_id

        # training datasets
        self.df_roles = None
        self.df_items = None
        self.df_implicit_feedback = None
        self.df_explicit_feedback = None
        self.df_role_keywords = None
        self.df_item_keywords = None
        self.min_relevance_score = 0
        
    def transform_data(self, implicit, explicit, content):
        '''
        This functions loads input data from database and converts to pandas dataframes.
        It fetches items, users, implicit and explicit feedback logs and content keywords
        We group the interactions by user roles instead of direct users.
        '''
        if (implicit == False and explicit == False):
            raise Exception("At least one feedback option should be enabled.")

        # Set training data level
        self.implicit = implicit
        self.explicit = explicit
        self.content = content

        # Fetch user roles (used as lightfm users)
        self.df_roles = self.fetch_roles()

        # Fetch model items
        self.df_items = self.fetch_items()

        # Load implicit interaction logs from the database
        if (self.implicit):
            self.df_implicit_feedback = self.fetch_implicit_feedback()

        # Load explicit interaction logs from the database
        if (self.explicit): 
            self.df_explicit_feedback = self.fetch_explicit_feedback()

        # Load content keywords
        if (self.content):
            self.df_role_keywords, self.df_item_keywords = self.fetch_content_keywords()  

        return 

    def generate_interaction_dataset(self): 
        '''
        Prepares training datasets for consumption by LightFM.
        Interaction feedback weights are calculated.
        Interactions and weights are converted to Sparse Matrixes.
        Note: Call transform_data before using this function
        '''      
        # output declarations
        interactions = None
        weights = None
        role_features = None
        item_features = None

        # calculate implicit interaction weights
        if (self.implicit):
            implicit_weights = self.calculate_implicit_weights()
            calculated_weights = implicit_weights

        # calculate explicit interaction weights
        if (self.explicit):
            explicit_weights = self.calculate_explicit_weights()

        # if implicit and explicit is enabled average out the corresponding weights
        if (self.implicit and self.explicit):
            calculated_weights = self.merge_weights(implicit_weights, explicit_weights)

        if (not self.implicit and self.explicit):
            calculated_weights = explicit_weights

        # role, items mapping to assign internal ids
        train_dataset = Dataset()
        train_dataset.fit(
                        set(self.df_roles['id']),
                        set(self.df_items['id']))

        num_users, num_items = train_dataset.interactions_shape()

        # Merge interactions
        calculated_weights['role_item_tuple'] = list(zip(calculated_weights.role_id, calculated_weights.item_id, calculated_weights.weight))
        
        # Build the interactions matrix (role=row x item=column)
        interactions, weights = train_dataset.build_interactions(calculated_weights['role_item_tuple'])
         
        # if content based recommendation data is enabled
        if(self.content):
            # assignment of internal indices for unique keyword listings
            train_dataset.fit_partial(
                item_features=self.df_item_keywords['keyword'].unique(),
                user_features=self.df_role_keywords['keyword'].unique()
            )

            # prepare the data in the appropiate iterable form 
            df_role_features= self.create_features(self.df_role_keywords, 'keyword', 'role_id')
            df_item_features = self.create_features(self.df_item_keywords, 'keyword', 'item_id')

            # create feature matrixes
            role_features = train_dataset.build_user_features(df_role_features)
            item_features = train_dataset.build_item_features(df_item_features)

        return interactions, weights, role_features, item_features

    def generate_training_test_datasets(self, interactions, percent):
        '''
        Extracts a random percent of test data from interactions of a training dataset for model evaluation
        Uses lightFm dataset splitting
        '''
        
        train, test = random_train_test_split(interactions, percent, random_state=np.random.RandomState(3))

        return train, test


    def fetch_implicit_feedback(self):
        '''
        Fetch implicit feedback data from database and join with items table for the corresponding model.
        '''
        sql_query = 'SELECT r.id AS role_id, i.id AS item_id, r.name AS role FROM implicit_log, role AS r, item AS i WHERE i.id = item_id AND r.id = role_id'
        df_all_implicit = pd.read_sql_query(sql_query, con=engine.connect()) 

        # Merge with the list of items from this model only
        df_implicit_feedback = df_all_implicit.merge(
            self.df_items, how='inner',
            left_on='item_id', right_on='id'
        )

        # check if there is data, otherwise raise exception
        if df_implicit_feedback.empty:
            raise Exception("No implicit feedback entries found.")        

        return df_implicit_feedback

    def fetch_explicit_feedback(self):
        '''
        Fetch explicit feedback from database and join with items table for the corresponding model.
        '''
        sql_query = 'SELECT r.id AS role_id, i.id AS item_id, r.name AS role, rank_value FROM explicit_log, role AS r, item AS i WHERE i.id = item_id AND r.id = role_id'
        df_all_explicit = pd.read_sql_query(sql_query, con=engine.connect()) 

        # Merge with the list of items from this model only
        df_explicit_feedback = df_all_explicit.merge(
            self.df_items, how='inner',
            left_on='item_id', right_on='id'
        )

        # check if there is data, otherwise raise exception
        if df_explicit_feedback.empty:
            raise Exception("No explicit feedback entries found.")   

        return df_explicit_feedback


    def fetch_content_keywords(self):
        '''
        Fetch content-based keywords for user roles and model items
        '''
        role_keyword_sql = 'SELECT role_id, keyword from role_keyword'
        item_keyword_sql = 'SELECT item_id, keyword from item_keyword, item as i where item_id = i.id and model_id like "{0}"'.format(self.model_id)

        df_role_keywords = pd.read_sql_query(role_keyword_sql, con=engine.connect()) 
        df_item_keywords = pd.read_sql_query(item_keyword_sql, con=engine.connect()) 

        # check if there is data, otherwise raise exception
        if (df_role_keywords.empty or df_item_keywords.empty):
            raise Exception("Missing content keywords for item or role.")   

        return df_role_keywords, df_item_keywords

    def fetch_roles(self):
        '''
        Query list of user roles from the role table
        '''
        roles = db_session.query(Role).all()

        # convert role query results to pandas dataframe (user group list)
        df_roles = pd.DataFrame([(r.id, r.name) for r in roles], 
                  columns=['id', 'name'])

        return df_roles


    def fetch_items(self):
        '''
        Query list of items linked to the current model_id
        '''
        # Get item list by model id from the database (item list)
        items = db_session.query(Item).filter(Item.model_id == self.model_id).all()

        # convert output query results to pandas dataframe
        df_items = pd.DataFrame([(i.id, i.model_id, i.category_id, i.guid, i.name) for i in items], 
                  columns=['id', 'model_id', 'category_id', 'guid', 'name'])

        return df_items


    def calculate_implicit_weights(self):
        '''
        Calculate and normalize implicit feedback weights
        '''
        # group interactions by output and ad the weight column, each count adds one point
        grouped_interactions = self.df_implicit_feedback.groupby(['item_id', 'role_id'])['name'].count().reset_index()

        grouped_interactions = grouped_interactions.rename(
            columns={'name': 'weight'})

        # get the min click value
        min = grouped_interactions['weight'].min()

        # get the max click value
        max = grouped_interactions['weight'].max()

        # min-max normalize weights from 0 to 5 range
        grouped_interactions['weight'] = 5 * ((grouped_interactions['weight'] - min ) / (max - min))

        # print(f'Grouped interactions: \r {grouped_interactions}')
    
        return grouped_interactions


    def calculate_explicit_weights(self):
        '''
        Average out explicit feedback by role
        '''
        grouped_interactions = self.df_explicit_feedback.groupby(['item_id', 'role_id'])['rank_value'].mean().reset_index()

        grouped_interactions = grouped_interactions.rename(
            columns={'rank_value': 'weight'})

        '''
        with pd.option_context('display.max_rows', 
                        None,
                        'display.max_columns', 
                        None):  # more options can be specified also
            print(grouped_interactions)
        '''

        return grouped_interactions

    def merge_weights(self, implicit_weights, explicit_weights):
        '''
        Merges implicit and explicit feedback calculated weights as an average grouping of items and roles
        '''
        df_merged_weights = explicit_weights.merge(
            implicit_weights, on=['item_id', 'role_id'],
            how='outer'
        )

        # average out implicit and explicit columns into final weight column
        cols = ['weight_x','weight_y']
        df_merged_weights['weight'] = df_merged_weights[cols].astype(float).mean(axis=1)

        # view implicit and explicit weights separately
        '''
        with pd.option_context('display.max_rows', 
                        None,
                        'display.max_columns', 
                        None):  # more options can be specified also
            print(df_merged_weights)
        '''

        # export weight calculations to csv
        # df_merged_weights.to_csv(f'{settings.MODEL_OUTPUT_DIR}/{self.model_id}.csv', index = True)

        # remove separate weights after final calculation
        del df_merged_weights['weight_x']
        del df_merged_weights['weight_y']

        # prune irrelevant interactions
        df_merged_weights = self.prune_irrelevants(df_merged_weights, self.min_relevance_score)

        return df_merged_weights

    def prune_irrelevants(self, weights_df:pd.DataFrame, min_rating):
        '''
        Removes interaction entries below a minimum weight value
        '''
        df = weights_df[weights_df.weight >= min_rating]
        return df

    ### Helper Functions ###
    def df_to_csv(self, dataframe, name):
        # export dataframe to csv
        dataframe.to_csv(f'{settings.MODEL_OUTPUT_DIR}/{self.model_id}_{name}.csv', index = True)

    def assign_unique_id(self, dataframe, id_col_name):
        '''
        Utility function to assign unique ids per row of a pandas dataframe
        Source: https://www.kaggle.com/niyamatalmass/lightfm-hybrid-recommendation-system
        Note: No longer required, but left here just in case.
        '''
        new_dataframe=dataframe.assign(
            int_id_col_name=np.arange(len(dataframe))
            ).reset_index(drop=True)

        return new_dataframe.rename(columns={'int_id_col_name': id_col_name})


    def create_features(self, dataframe, features_name, id_col_name):
        '''
        Transform item/role features in structure needed by LightFM as (role/item id, [features])
        '''
        features = dataframe.groupby([id_col_name])[features_name].apply(list)
        features = list(zip(features.index, features))
        return features


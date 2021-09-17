from ..database import settings
import os
import glob
import pickle
import numpy as np
from datetime import datetime
from os import path
from pathlib import Path
from lightfm import LightFM
from lightfm.evaluation import precision_at_k, recall_at_k, auc_score
from app.main.database import db_session

class RecommenderHandler():
    def __init__(self, model_meta, new=False, save=True):
        '''
        Constructor that initializes thread, loads or create model
        and sets training parameters. Encapsulation of the LightFM library.

        References:
        https://making.lyst.com/lightfm/docs/index.html

        Args:
            model_meta(SQLAlchemy Model Row): metadata for the target model recommendation to use
            new: if new model will be created on train
        '''
        # model metadata object for database use
        self.model_meta = model_meta
        # model type and settings
        self.learning_rate = 0.05
        self.epochs = 30
        self.item_alpha = 0.0
        self.user_alpha = 0.0
        self.loss = 'warp' # only warp implemented for now =)
        # training data
        self.train_interactions = None
        self.train_weights = None
        # test data
        self.test_interactions = None
        self.test_weights = None
        # features (keywords)
        self.user_features = None
        self.item_features = None
        # recommendation model instance
        self.model = None 
        # use saved model or create new
        self.new = new
        # save model for updates or later use
        self.save = save

        self.last_model_name = self.get_name_last_model()
        print(self.last_model_name)
        if (path.isfile(self.last_model_name)):
            print('Opening previously trained model...')
            with open(f'{self.last_model_name}', 'rb') as model_file:
                self.model = pickle.load(model_file)
        else:
            self.new = True
            # self.model = LightFM(loss=self.loss, learning_rate=self.learning_rate)
            
    def get_name_last_model(self):
        '''
        Gets the last modified model according to file name stored in database

        Returns:
            str: filename of last modified model
        '''
        file_name = self.model_meta.model_file
        if(file_name != ""):
            return f'{settings.MODEL_OUTPUT_DIR}/{file_name}'
        
        return ""

    def save_model(self, filename):
        '''
        Given a name saves the model in the path specified in config as a .pickle file

        Args:
            filename (str): file name for the model
        '''
        try:
            with open(f'{settings.MODEL_OUTPUT_DIR}/{filename}.pickle', 'wb') as file_model:
                pickle.dump(self.model, file_model,
                        protocol=pickle.HIGHEST_PROTOCOL)
        
            return f'{filename}.pickle'

        except:
            return None

    def train(self):
        '''
        Trains a recommender model doing partial train by default if a model already exists. Otherwise new will be used.
            Harcoded to use the warp loss function and default lightFM paramaters

        Returns:
            response: true if success and false if exception
        '''
        try:
            if(self.new):
                print('creating new recommender model...')
                self.model = LightFM(loss=self.loss,learning_rate=self.learning_rate, item_alpha=self.item_alpha, user_alpha=self.user_alpha, random_state=2021)
                self.model._reset_state()

            # current date and time
            now = datetime.now()
            timestamp = datetime.timestamp(now)

            # set initial metadata (parameters)
            self.model_meta.epochs = self.epochs
            self.model_meta.learning_rate = self.learning_rate
            self.model_meta.loss = self.loss
            self.model_meta.user_alpha = self.user_alpha
            self.model_meta.item_alpha = self.item_alpha
            self.model_meta.model_file = ""

            # fit/train model
            self.model.fit_partial(self.train_interactions, self.user_features, self.item_features, self.train_weights, self.epochs,
                        1 , False)

            # save model to file
            if(self.save):
                model_file = self.save_model(timestamp)
                self.model_meta.model_file = model_file

            # interaction dimensions
            n_users, n_items = self.train_interactions.shape

            # model final metadata to save on database (outputs)
            self.model_meta.num_users = n_users
            self.model_meta.num_items = n_items
            self.model_meta.last_trained = datetime.now()
            self.model_meta.message = 'Model has been trained successfully'
            self.model_meta.status = 'success'
            
            return True

        except Exception as e: 
            print(str(e))
            self.model_meta.last_trained = datetime.now()
            self.model_meta.status = 'fail'
            self.model_meta.message = str(e)
            return False

    def get_recommendation_byuser(self, user, user_list, output_list):
        '''
        Gets recommendation of a specific user/role/profile/group 
        '''

        # get the name of the selected role
        user_list.set_index("id", inplace = True) 
        result = user_list.loc[user] 

        # get the number of all items
        n_items = self.model_meta.num_items
        
        # find the output scores for that role
        scores = self.model.predict(user, np.arange(n_items))

        output_list['score'] = scores

        # print the scores based on the order of most liked to least liked
        top_outputs = output_list.sort_values(by='score', ascending=False)
 
        return top_outputs

    def evaluate_p_at_k(self, k=10):
        '''
        Evaluate performance of a fitted LightFM model using precision_at_k metric. A perfect score is 1.0.
        Returns the mean p@k across all users.
        For more information see: https://making.lyst.com/lightfm/docs/lightfm.evaluation.html
        '''

        # return 0 if the model training is on fail status
        if (self.model_meta.status == 'fail'):
            return 0.0

        precision = precision_at_k(self.model, self.test_interactions, user_features=self.user_features, 
        item_features = self.item_features, k = k).mean()
        return precision

    def evaluate_p_at_k_puser(self, k=10):
        '''
        Evaluate performance of a fitted LightFM model using precision_at_k methodology. A perfect score is 1.0.
        Returns p@k per user.
        For more information see: https://making.lyst.com/lightfm/docs/lightfm.evaluation.html
        '''

        # return 0 if the model training is on fail status
        if (self.model_meta.status == 'fail'):
            return 0.0

        precision_puser = precision_at_k(self.model, self.test_interactions, self.train_interactions, user_features=self.user_features, 
        item_features = self.item_features, k = k)

        print(precision_puser)


    def evaluate_r_at_k(self, k=10):
        '''
        Evaluate performance of a fitted LightFM model using recall_at_k metric. A perfect score is 1.0.
        Returns the mean r@k across all users.
        For more information see: https://making.lyst.com/lightfm/docs/lightfm.evaluation.html
        '''
        # return 0 if the model training is on fail status
        if (self.model_meta.status == 'fail'):
            return 0.0

        recall = recall_at_k(self.model, self.test_interactions, user_features=self.user_features, 
        item_features = self.item_features, k = k).mean()
        return recall


    def evaluate_r_at_k_puser(self, k=10):
        '''
        Evaluate performance of a fitted LightFM model using recall_at_k metric. A perfect score is 1.0.
        Returns r@k per user.
        For more information see: https://making.lyst.com/lightfm/docs/lightfm.evaluation.html
        '''
        # return 0 if the model training is on fail status
        if (self.model_meta.status == 'fail'):
            return 0.0

        recall_puser = recall_at_k(self.model, self.test_interactions, user_features=self.user_features, 
        item_features = self.item_features, k = k)

        print(recall_puser)

    def evaluate_auc(self):
        '''
        Evaluate performance of a fitted LightFM model using precision_at_k methodology. A perfect score is 1.0.
        Returns the mean AUC across all users.
        For more information see: https://making.lyst.com/lightfm/docs/lightfm.evaluation.html
        '''
        # return 0 if the model training is on fail status
        if (self.model_meta.status == 'fail'):
            return 0.0

        auc = auc_score(self.model, self.test_interactions, user_features=self.user_features, 
        item_features = self.item_features).mean()
        return auc

    def evaluate_auc_puser(self):
        '''
        Evaluate performance of a fitted LightFM model using ROC AUC metric. A perfect score is 1.0.
        Returns ROC AUC per user.
        For more information see: https://making.lyst.com/lightfm/docs/lightfm.evaluation.html
        '''

        # return 0 if the model training is on fail status
        if (self.model_meta.status == 'fail'):
            return 0.0

        auc_puser = auc_score(self.model, self.test_interactions, user_features=self.user_features, 
        item_features = self.item_features)

        print(auc_puser)


    def get_stats(self):
        '''
        Data Stats: interaction count and sparcity percentage
        '''
        non_zero_training = self.train_interactions.count_nonzero()
        non_zero_test = self.test_interactions.count_nonzero()

        total_combinations = self.model_meta.num_users  * self.model_meta.num_items 

        training_sparsity = (total_combinations - non_zero_training) / total_combinations
        test_sparcity = (total_combinations - non_zero_test) / total_combinations

        print(f'Model Identifer: {self.model_meta.model_id} ' )
        print(f'Total Training Interactions: {non_zero_training}' )
        print(f'Total Test Interactions: {non_zero_test}'  )
        print(f'Train set sparcity: {training_sparsity}')
        print(f'Test set sparcity: {test_sparcity}')

        return

    ### Helper Functions ###

    def save_changes(self, data):
        '''
        Insert/Update and commit database changes.
        '''
        db_session.add(data)
        db_session.commit()

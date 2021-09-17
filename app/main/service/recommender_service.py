from ..handler.recommender_handler import RecommenderHandler 
from ..handler.preprocess_handler import PreprocessHandler
from ..model.training import Training
from app.main.database import db_session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func
from flask import abort
import json
import sys

def train_model(data):
    '''
    Fit a selected model with training data.
    '''
    try:
        session = db_session()
        # get the training meta for the selected recommendation model
        query_ok = False
        training_meta = session.query(Training).filter(Training.model_id == data['model_id']).first()

        # check if the model exists
        if (training_meta == None):
            query_ok = True
            raise Exception("Model id not found")
                
        # prepare training data for lightFM consumption
        data_preprocessor = PreprocessHandler(data['model_id'])
        data_preprocessor.min_relevance_score = 2 # set minimum weight to consider as a positive interaction
        data_preprocessor.transform_data(data['implicit'], data['explicit'], data['content'])
        interactions, weights, role_features, item_features = data_preprocessor.generate_interaction_dataset()

        # set flags for trainig data level used
        training_meta.implicit = data_preprocessor.implicit
        training_meta.explicit = data_preprocessor.explicit
        training_meta.content = data_preprocessor.content

        # store disjoint test data percent
        training_meta.test_percent = data['test_percent']

        # split into training and testing data
        train_set, test_set = data_preprocessor.generate_training_test_datasets(interactions, data['test_percent'])
        train_weights, test_weights = data_preprocessor.generate_training_test_datasets(weights, data['test_percent'])

        # instantiate model handler
        recommender = RecommenderHandler(training_meta, new=data['new'])

        # assign model hyper parameters
        recommender.epochs = data['epochs']
        recommender.learning_rate = data['learning_rate']
        recommender.user_alpha = data['user_alpha']
        recommender.item_alpha = data['item_alpha']

        # assign model train and test data
        recommender.train_interactions = train_set
        recommender.test_interactions = test_set
        recommender.train_weights = train_weights
        recommender.test_weights = test_weights
        recommender.user_features = role_features
        recommender.item_features = item_features

        # train the model
        response = recommender.train()

        # evaluate
        p_at_k_score = recommender.evaluate_p_at_k(10)
        print(f'learning rate = {recommender.learning_rate}')
        print(f'p@k = {p_at_k_score}')

        # save results into database
        save_changes(recommender.model_meta)

        # print stats
        recommender.get_stats()

        # prepare exit response
        response = {
            'status': recommender.model_meta.status,
            'message': recommender.model_meta.message
        }

        session.close()   
        return response, 202

    except SQLAlchemyError as e:
        session.rollback()
        response = {
            'status': 'fail',
            'message': str(e)
        }
        return response, 500 

    except Exception as e:
        if(query_ok):
            training_meta.message = 'fail'
            training_meta.message = str(e)
            save_changes(training_meta)
        response = {
            'status': 'fail',
            'message': str(e)
        }
    return response, 500
    

def get_model_info(model_id):
    '''
        Get training metadata from the selected model identifer
    '''

    session = db_session()
    training_meta = session.query(Training).filter(Training.model_id == model_id).first()
    session.close()

    if training_meta:
        response_object = {
            'status': 'success',
            'data': {
                'model_id' : training_meta.model_id,
                'status': training_meta.status,
                'message' : training_meta.message,
                'last_trained' : training_meta.last_trained.strftime("%Y-%m-%d %H:%M:%S"),
                'model_file' : training_meta.model_file,
                'is_implicit' : training_meta.implicit,
                'is_explicit' : training_meta.explicit,
                'is_content' : training_meta.content,
                'test_percent' : training_meta.test_percent,
                'learning_rate' : training_meta.learning_rate,
                'epochs' : training_meta.epochs,
                'loss' : training_meta.loss,
                'user_alpha' : training_meta.user_alpha,
                'item_alpha' : training_meta.item_alpha
            }
        }
        return response_object, 200
    else:
        abort(400, 'Model information not found')

    return None, 200     
    
 
def evaluate(data): 
    '''
    Evaluate the performance of the selected fitted model.
    '''
    try:
        session = db_session()
        # get the metadata from the selected recommendation model
        training_meta = db_session.query(Training).filter(Training.model_id == data['model_id']).first()

        # check if model if existed
        if (training_meta == None):
             raise Exception("Model id not found")
            
        # get interaction data
        data_preprocessor = PreprocessHandler(data['model_id'])
        data_preprocessor.min_relevance_score = 2
        data_preprocessor.transform_data(training_meta.implicit, training_meta.explicit, training_meta.content)
        interactions, weights, role_features, item_features = data_preprocessor.generate_interaction_dataset()

        # get original test data percent from all interactions
        test_percent = training_meta.test_percent

        # split into training and testing data
        train_set, test_set = data_preprocessor.generate_training_test_datasets(interactions, test_percent)

        # load model
        recommender = RecommenderHandler(training_meta)

        # specify test data and features
        recommender.test_interactions = test_set
        recommender.user_features = role_features
        recommender.item_features = item_features

        # evaluate and assign scores
        p_at_k_score = recommender.evaluate_p_at_k(data['k'])
        p_at_k_score = json.dumps(p_at_k_score.item())

        r_at_k_score = recommender.evaluate_r_at_k(data['k'])
        r_at_k_score = json.dumps(r_at_k_score.item())

        auc_score = recommender.evaluate_auc()
        auc_score = json.dumps(auc_score.item())

        '''
        print('p@k:')
        recommender.evaluate_p_at_k_puser()
        print('r@k:')
        recommender.evaluate_r_at_k_puser()
        print('auc')
        recommender.evaluate_auc_puser()
        '''

        session.close()

        response = {
            'status': 'success',
            'p_at_k_score': float(p_at_k_score),
            'r_at_k_score': float(r_at_k_score),
            'auc_score' : float(auc_score) 
        }

        return response, 200

    except SQLAlchemyError as e:
        session.rollback()
        response = {
            'status': 'fail',
            'message': str(e)
        }
        return response, 500 

    except Exception as e:
        response = {
            'status': 'fail',
            'message': str(e)
        }
        return response, 500


def role_recommendation(data):
    '''
    Provides ordered list by rank of recommended items for a user/role
    '''
    try:
        session = db_session()
        # get the metadata from the selected recommendation model
        training_meta = session.query(Training).filter(Training.model_id == data['model_id']).first()

        # check if model if existed
        if (training_meta == None):
            raise Exception("Model id not found") 

        # get the list of unique roles and items
        data_preprocessor = PreprocessHandler(data['model_id'])
        roles = data_preprocessor.fetch_roles()
        items = data_preprocessor.fetch_items()

        # instantiate model recommender handler
        recommender = RecommenderHandler(training_meta)

        # get the ordered list of recommended items (top to bottom)
        item_list_df = recommender.get_recommendation_byuser(data['role_id'], roles, items)

        # count the number of rows
        item_rows, item_columns = item_list_df.shape

        # validate data limit number from 1 count of item_list
        if( data['num_items'] < 1 or data['num_items'] > item_rows ):
            raise Exception("Number of items is out of range") 

        # convert to json up to the specified limit
        items_json = []
        for index, row in item_list_df[:data['num_items']].iterrows():
            items_json.append({'item_id': row['id'],  'item_name': row['name'], 'rank_value': row['score']})

        session.close()

        response = {
            'status': 'success',
            'items': items_json
        }

        return response, 200

    except SQLAlchemyError as e:
        session.rollback()
        response = {
            'status': 'fail',
            'message': str(e)
        }
        return response, 500      
    
    except Exception as e:
        response = {
            'status': 'fail',
            'message': str(e)
        }
        return response, 500
    
### Database Helper Functions ###

def save_changes(data):
    db_session.add(data)
    db_session.commit()
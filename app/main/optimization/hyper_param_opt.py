# import lightgbm as lgb
import os
import optuna
from optuna.samplers import TPESampler
from optuna.visualization import plot_optimization_history
from ..model.training import Training
from app.main.database import db_session
from ..handler.recommender_handler import RecommenderHandler 
from ..handler.preprocess_handler import PreprocessHandler
from ..database import settings
from ..config import config_by_name

def lightfm_objective(recommender: RecommenderHandler, metric, k=10):
    '''
    Objective function factory to run optuna trials
    Accepted metric strings: p@k, r@k and auc.
    Uses the precision at 10 by default unless other metric is specified.
    '''
    def objective(trial):
        # sample hyper-parameter values
        recommender.learning_rate = trial.suggest_float('learning_rate', 0, 0.08, log=False)
        # recommender.epochs = trial.suggest_int('epochs', 15, 500)
        recommender.item_alpha = trial.suggest_loguniform('item_alpha', 1e-10, 1e-0)
        recommender.user_alpha = trial.suggest_loguniform('user_alpha', 1e-10, 1e-0)
        # train model and evaluate
        recommender.train()
        target = None
        if(metric == 'r@k'):
            target = recommender.evaluate_r_at_k(k)
        elif(metric == 'auc'):
            target = recommender.evaluate_auc()
        else:
            target = recommender.evaluate_p_at_k(k)
        # store trial-specific information for later use
        trial.set_user_attr('epochs', recommender.epochs)
        return target
    return objective

def start_opt_studies():
    '''
    Start batch of optimization studies for each recommendation model
    '''

    print('Starting optimization trials...')

    # Hydroeconomic Model
    # optimize p@k
    run_optimization_trials('5d8cdb841328534298eacf4a', True, False, False, 0.2, 'p@k', 10, 1) #HE2
    run_optimization_trials('5d8cdb841328534298eacf4a', False, True, False, 0.2, 'p@k', 10, 2) #HE6
    run_optimization_trials('5d8cdb841328534298eacf4a', True, True, False, 0.2, 'p@k', 10, 3)  #HE10
    run_optimization_trials('5d8cdb841328534298eacf4a', True, True, True, 0.2, 'p@k', 10, 4) #HE14
    run_optimization_trials('5d8cdb841328534298eacf4a', True, False, True, 0.2, 'p@k', 10, 5) #HE18
    run_optimization_trials('5d8cdb841328534298eacf4a', False, True, True, 0.2, 'p@k', 10, 6) #HE22

    # optimize r@k
    run_optimization_trials('5d8cdb841328534298eacf4a', True, False, False, 0.2, 'r@k', 10, 7) #HE3
    run_optimization_trials('5d8cdb841328534298eacf4a', False, True, False, 0.2, 'r@k', 10, 8) #HE7
    run_optimization_trials('5d8cdb841328534298eacf4a', True, True, False, 0.2, 'r@k', 10, 9) #HE11
    run_optimization_trials('5d8cdb841328534298eacf4a', True, True, True, 0.2, 'r@k', 10, 10) #HE15
    run_optimization_trials('5d8cdb841328534298eacf4a', True, False, True, 0.2, 'r@k', 10, 11) #HE19
    run_optimization_trials('5d8cdb841328534298eacf4a', False, True, True, 0.2, 'r@k', 10, 12) #HE23

    # optimize auc
    run_optimization_trials('5d8cdb841328534298eacf4a', True, False, False, 0.2, 'auc', 10, 13) #HE4
    run_optimization_trials('5d8cdb841328534298eacf4a', False, True, False, 0.2, 'auc', 10, 14) #HE8
    run_optimization_trials('5d8cdb841328534298eacf4a', True, True, False, 0.2, 'auc', 10, 15) #HE12
    run_optimization_trials('5d8cdb841328534298eacf4a', True, True, True, 0.2, 'auc', 10, 16) #HE16
    run_optimization_trials('5d8cdb841328534298eacf4a', True, False, True, 0.2, 'auc', 10, 17) #HE20
    run_optimization_trials('5d8cdb841328534298eacf4a', False, True, True, 0.2, 'auc', 10, 18) #HE24


    # Water Balance Model
    # optimize p@k
    run_optimization_trials('5d76cc181328534d8cb7d17c', True, False, False, 0.2, 'p@k', 10, 1) #WB2
    run_optimization_trials('5d76cc181328534d8cb7d17c', False, True, False, 0.2, 'p@k', 10, 2) #WB6
    run_optimization_trials('5d76cc181328534d8cb7d17c', True, True, False, 0.2, 'p@k', 10, 3) #WB10
    run_optimization_trials('5d76cc181328534d8cb7d17c', True, True, True, 0.2, 'p@k', 10, 4) #WB14
    run_optimization_trials('5d76cc181328534d8cb7d17c', True, False, True, 0.2, 'p@k', 10, 5) #WB18
    run_optimization_trials('5d76cc181328534d8cb7d17c', False, True, True, 0.2, 'p@k', 10, 6) #WB22

    # optimize r@k
    run_optimization_trials('5d76cc181328534d8cb7d17c', True, False, False, 0.2, 'r@k', 10, 7) #WB3
    run_optimization_trials('5d76cc181328534d8cb7d17c', False, True, False, 0.2, 'r@k', 10, 8) #WB7
    run_optimization_trials('5d76cc181328534d8cb7d17c', True, True, False, 0.2, 'r@k', 10, 9) #WB11
    run_optimization_trials('5d76cc181328534d8cb7d17c', True, True, True, 0.2, 'r@k', 10, 10) #WB15
    run_optimization_trials('5d76cc181328534d8cb7d17c', True, False, True, 0.2, 'r@k', 10, 11) #WB19
    run_optimization_trials('5d76cc181328534d8cb7d17c', False, True, True, 0.2, 'r@k', 10, 12) #WB23

    # optimize auc
    run_optimization_trials('5d76cc181328534d8cb7d17c', True, False, False, 0.2, 'auc', 10, 13) #WB4
    run_optimization_trials('5d76cc181328534d8cb7d17c', False, True, False, 0.2, 'auc', 10, 14) #WB8
    run_optimization_trials('5d76cc181328534d8cb7d17c', True, True, False, 0.2, 'auc', 10, 15) #WB12
    run_optimization_trials('5d76cc181328534d8cb7d17c', True, True, True, 0.2, 'auc', 10, 16) #WB16
    run_optimization_trials('5d76cc181328534d8cb7d17c', True, False, True, 0.2, 'auc', 10, 17) #WB20
    run_optimization_trials('5d76cc181328534d8cb7d17c', False, True, True, 0.2, 'auc', 10, 18) #WB24

    '''
    # generate plots from specific studies
    study = loadStudy('optimization-study-5d8cdb841328534298eacf4a-r16')
    parameters = ['learning_rate','item_alpha', 'user_alpha']
    generate_plots(study, parameters)
    '''

    return

def run_optimization_trials(model_id:str, implicit:bool, explicit:bool, content:bool, test_percent:float, metric:str, k:int, revision:int):
    '''
    sets up study and runs trials
    optuna database storage enabled by default
    default number of trials: 
    approach: epochs in outer loop, more trials on lower epochs, rest of hyperparams optimized via optuna trials
    '''

    environment = (os.getenv('BOILERPLATE_ENV') or 'dev')
    settings = config_by_name[environment]

    session = db_session()
    training_meta = session.query(Training).filter(Training.model_id == model_id).first()

    training_meta.implicit = implicit
    training_meta.explicit = explicit
    training_meta.content = content
    training_meta.test_percent = test_percent

    # prepare training data for lightFM consumption
    data_preprocessor = PreprocessHandler(model_id)
    data_preprocessor.min_relevance_score = 2
    data_preprocessor.transform_data(implicit, explicit, content)
    interactions, weights, role_features, item_features = data_preprocessor.generate_interaction_dataset()

    # split into training and testing data
    train_set, test_set = data_preprocessor.generate_training_test_datasets(interactions, test_percent)
    train_weights, test_weights = data_preprocessor.generate_training_test_datasets(weights, test_percent)

    # declare the model handler
    recommender = RecommenderHandler(training_meta, True, False)
    
    # set model data and fixed settings
    recommender.train_interactions = train_set
    recommender.test_interactions = test_set
    recommender.train_weights = train_weights
    recommender.test_weights = test_weights
    recommender.user_features = role_features
    recommender.item_features = item_features

    # prepare study
    study_name = f'optimization-study-{model_id}-r{revision}'  # Unique identifier of the study.
    storage_name = settings.TRIAL_DATABASE_URL.format(study_name)

    n_trials = {
    # epochs: # trials
        5: 60,
        15: 50,
        30: 45,
        50: 35,
        100: 30,
        200: 20,
        500: 5
    }

    '''
    n_trials = {
    # epochs: # trials
        15: 50,
        100: 25
    }
    '''

    objective = lightfm_objective(recommender, metric, k)
    
    study = optuna.create_study(
        direction = 'maximize',
        study_name= study_name,
        storage = storage_name,
        sampler=TPESampler(seed=2021),
        load_if_exists = False
    )

    # loop for preset epoch trials
    for num_epochs, num_trials in n_trials.items():
        print(f'Epoch: {num_epochs}')
        recommender.epochs = num_epochs
        study.optimize(objective, n_trials=num_trials)
    
     

    # epochs not preset optimized epochs
    # study.optimize(objective, n_trials=200)

    #export results
    print(f'Study: optimization-study-{model_id}-r{revision}', file=open(f'{settings.MODEL_OUTPUT_DIR}/study-results.txt', "a"))

    '''
    # epochs optimized in trials
    print(f'The best value of precision@k={study.best_value:0.4f} was achieved with '
      f'learning_rate={study.best_params["learning_rate"]:.04e} '
      f'item_alpha={study.best_params["item_alpha"]:.04e} '
      f'user_alpha={study.best_params["user_alpha"]:.04e} '
      f'epochs={study.best_params["epochs"]}', file=open(f'{settings.MODEL_OUTPUT_DIR}/study-results.txt', "a"))
    '''
    
    # epochs on outter loop
    print(f'The best value of {metric}={study.best_value:0.4f} was achieved with '
      f'learning_rate={study.best_params["learning_rate"]:.04e} '
      f'item_alpha={study.best_params["item_alpha"]:.04e} '
      f'user_alpha={study.best_params["user_alpha"]:.04e} '
      f'within {study.best_trial.user_attrs["epochs"]} epochs.', file=open(f'{settings.MODEL_OUTPUT_DIR}/study-results.txt', "a"))
    
    print(f'{study.best_trial.user_attrs["epochs"]}\t'
     f'{study.best_params["learning_rate"]:.04e}\t'
     f'{study.best_params["item_alpha"]:.04e}\t'
     f'{study.best_params["user_alpha"]:.04e}\t'
     f'{study.best_value:0.4f}'   
    , file=open(f'{settings.MODEL_OUTPUT_DIR}/study-results.txt', "a"))

    print('--------------------------------------', file=open(f'{settings.MODEL_OUTPUT_DIR}/study-results.txt', "a"))

    return study

def loadStudy(study_name):
    '''
    Load a previously executed study from a database
    '''

    storage_name = 'mysql://root:@localhost:3306/swim-recommender-studies'.format(study_name)
    study = optuna.create_study(
        study_name=study_name, 
        direction='maximize', 
        storage=storage_name, 
        load_if_exists=True)

    return study

def generate_plots(study, parameters:list):
    '''
    Generate plots from a finished optimization study
    '''
    # study plots
    fig1 = optuna.visualization.plot_param_importances(study)
    fig2 = optuna.visualization.plot_optimization_history(study)
    fig3 = optuna.visualization.plot_slice(study, params=parameters)

    # show plots
    fig1.show()  
    fig2.show()  
    fig3.show()


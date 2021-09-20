import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    MODEL_OUTPUT_DIR = ""
    DATABASE_URL = ''
    USER_DATABASE_URL = ''
    TRIAL_DATABASE_URL = ''
    POOL_PRE_PING = True
    POOL_SIZE = 5
    POOL_RECYCLE= 3600   
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    MODEL_OUTPUT_DIR = ""
    DATABASE_URL = ''
    USER_DATABASE_URL = ''
    TRIAL_DATABASE_URL = ''
    POOL_PRE_PING = True
    POOL_SIZE = 10
    POOL_RECYCLE= 3600   
    DEBUG = True
    TESTING = True

class ProductionConfig(Config):
    MODEL_OUTPUT_DIR = "/recommender/model"
    DATABASE_URL = os.getenv('RECOMM_DATABASE_URL') 
    USER_DATABASE_URL = os.getenv('USER_DATABASE_URL') 
    TRIAL_DATABASE_URL = os.getenv('TRIAL_DATABASE_URL') 
    POOL_PRE_PING = True
    POOL_SIZE = 10
    POOL_RECYCLE= 3600   
    DEBUG = False
    TESTING = False

config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

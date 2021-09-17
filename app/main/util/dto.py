from flask_restplus import Namespace, fields

class AuthDto:
    api = Namespace('/recommender/auth', description='Authentication endpoint for token retrival')

class TrainDto:
    api = Namespace('/recommender/train', description='Recommendation model training')
    train = api.model('train', {
        'model_id': fields.String(required=True, description='Id of the model', example='5d76cc181328534d8cb7d17c'),
        'new': fields.Boolean(required=True, description='Create a new model or part from existing', example=True),
        'epochs': fields.Integer(required=True, description='Number of epochs to run the training', example=30),
        'learning_rate': fields.Float(required=True, description='model learning rate', example=0.05),
        'test_percent' :  fields.Float(required=True, description='disjoint percent of test data', example=0.2),
        'item_alpha' : fields.Float(required=True, description='importance penalty on item features', example=0.0),
        'user_alpha' : fields.Float(required=True, description='importance penalty on user features', example=0.0),
        'implicit' : fields.Boolean(required=True, description='Enable training with implicit feedback data', example=True),
        'explicit' : fields.Boolean(required=True, description='Enable training with explicit feedback data', example=False),
        'content' : fields.Boolean(required=True, description='Enable training with content-based data', example=False)
    })

class EvaluationDto:
    api = Namespace('/recommender/evaluate', description='Model evaluation metrics')
    evaluation = api.model('eval_precision', {
        'model_id': fields.String(required=True, description='target trained model', example='5d76cc181328534d8cb7d17c'),
        'k' : fields.Integer(required=True, description='top position', example=10)
    })   

class RecommendDto:
    api = Namespace('/recommender/request', description='Request item recommendations')
    role_req = api.model('role_req', {
        'role_id': fields.Integer(required=True, description='Unique id of the target user role', example=1),
        'model_id': fields.String(required=True, description='Unique id  of the target model', example='5d76cc181328534d8cb7d17c'),
        'num_items' : fields.Integer(required=False, description='Limit on number of items retrieved', example=10)
    })
    item_res = api.model('item_res', {
        'item_id': fields.String(required=True, description='unique id of the item'),
        'item_name': fields.String(required=True, description='unique name of the item'),
        'rank_value' : fields.Float(required=False, description='rank value of the item')
    })

class ModelDto:
    api = Namespace('/recommender/db/model', description='Database operations for recommendation models')
    model = api.model('model', {
        'id': fields.String(required=True, description='global unique identifier'),
        'name': fields.String(required=True, description='recommender model name or label'),
        'context_iri' : fields.String(required=False, description='json-ld context to provide semantics')
    })    

class CategoryDto:
    api = Namespace('/recommender/db/category', description='Database operations for item categories')
    category = api.model('category', {
        'id': fields.String(required=True, description='item category unique identifier'),
        'name': fields.String(required=True, description='item category name or label')
    }) 
    category_entry = api.model('category', {
        'name': fields.String(required=True, description='item category name or label')
    }) 

class ItemDto:
    api = Namespace('/recommender/db/item', description='Database operations for items')
    item = api.model('item', {
        'id': fields.Integer(required=True, description='local unique id'),
        'model_id': fields.String(required=True, description='recommender model id'),
        'category_id': fields.Integer(required=True, description='category id'),
        'guid': fields.String(required=True, description='global unique identifer'),
        'name': fields.String(required=True, description='name of the item')
    })
    item_entry = api.model('item', {
        'model_id': fields.String(required=True, description='recommender model id'),
        'category_id': fields.Integer(required=True, description='category id'),
        'guid': fields.String(required=True, description='global unique identifer'),
        'name': fields.String(required=True, description='name of the item')
    })

class RoleDto:
    api = Namespace('/recommender/db/role', description='Database operations for user roles')
    role = api.model('role', {
        'id': fields.Integer(required=True, description='role id'),
        'name': fields.String(required=True, description='role name'),
    })
    role_entry = api.model('role', {
        'name': fields.String(required=True, description='role name')
    })

class ImplicitDto:
    api = Namespace('/recommender/db/implicit', description='Database operations for implicit feedback data')
    implicit_log = api.model('implicit_log', {
        'item_id': fields.Integer(required=True, description='local identifier of the viewed item'),
        'user_id': fields.Integer(required=True, description='external user identifer'),
        'run_id': fields.String(required=True, description='external global unique identifer of the related run'),
        'role_id': fields.Integer(required=True, description='local user/role/group identifer'),
    })

class ExplicitDto:
    api = Namespace('/recommender/db/explicit', description='Database operations for explicit feedback data')
    explicit_log = api.model('explicit_log', {
        'item_id': fields.Integer(required=True, description='local identifier of the ranked item'),
        'rank_value' : fields.Integer(required=True, description='value from 1 to 5 that was explicitly assigned by a user'),
        'user_id': fields.Integer(required=True, description='external user identifer'),
        'run_id': fields.String(required=True, description='external global unique identifer of the related run'),
        'role_id': fields.Integer(required=True, description='local user/role/group identifer'),
    })

class ItemKeywordDto:
    api = Namespace('/recommender/db/item-keyword', description='Database operations for item keywords')
    item_keyword = api.model('item_keyword', {
        'id': fields.Integer(required=True, description='item keyword id'),
        'keyword': fields.String(required=True, description='relevant keyword related to an item'),
        'item_id': fields.Integer(required=True, description='local identifier of the related item'),
        'weight': fields.Integer(required=False,  description='raw weight value for keyword as integer')
    })
    item_keyword_entry = api.model('item_keyword', {
        'keyword': fields.String(required=True, description='relevant keyword related to an item'),
        'item_id': fields.Integer(required=True, description='local identifier of the related item'),
        'weight': fields.Integer(required=False,  description='raw weight value for keyword as integer'),
    })

class RoleKeywordDto:
    api = Namespace('/recommender/db/role-keyword', description='Database operations for role keywords')
    role_keyword = api.model('role_keyword', {
        'id': fields.Integer(required=True, description='role keyword id'),
        'keyword': fields.String(required=True, description='relevant keyword related to an item'),
        'role_id': fields.Integer(required=True, description='local identifier of the related role'),
        'weight': fields.Integer(required=False,  description='raw weight value for keyword as integer')
    })
    role_keyword_entry = api.model('role_keyword', {
        'keyword': fields.String(required=True, description='relevant keyword related to an role'),
        'role_id': fields.Integer(required=True, description='local identifier of the related role'),
        'weight' : fields.Integer(required=False, description='raw weight value for keyword as integer')
    })





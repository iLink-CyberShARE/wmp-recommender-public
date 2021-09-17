from flask_restplus import Api
from flask import Blueprint, url_for

from .main.controller.train_controller import api as train_ns
from .main.controller.evaluate_controller import api as evaluate_ns
from .main.controller.recommendation_controller import api as recommendation_ns
from .main.controller.model_controller import api as model_ns
from .main.controller.category_controller import api as category_ns
from .main.controller.item_controller import api as item_ns
from .main.controller.role_controller import api as role_ns
from .main.controller.implicit_controller import api as implicit_ns
from .main.controller.explicit_controller import api as explicit_ns
from .main.controller.item_keyword_controller import api as item_keyword_ns
from .main.controller.role_keyword_controller import api as role_keyword_ns


blueprint = Blueprint('recomms', __name__, url_prefix='/swim-recommender')

class CustomAPI(Api):
    @property
    def specs_url(self):
        '''
        The Swagger specifications absolute url (ie. `swagger.json`)
        This fix will force a relatve url to the specs.json instead of absolute
        :rtype: str
        '''
        return url_for(self.endpoint('specs'), _external=False)

authorizations = {
    'Bearer Auth' : {
        'type' : 'apiKey',
        'in' : 'header',
        'name' : 'Authorization',
        'description': 'Type in the value input box below: Bearer &lt;JWT&gt; where JWT is the token'
    }
}

api = CustomAPI(blueprint,
          title= "SWIM Recommender API",
          version='2.0',
          description='Recommendation service with LightFM',
          doc='/docs/',
          security='Bearer Auth',
          authorizations = authorizations
          )

api.add_namespace(train_ns, path='/recommender/train')
api.add_namespace(evaluate_ns, path='/recommender/evaluate')
api.add_namespace(recommendation_ns, path='/recommender/request')
api.add_namespace(model_ns, path='/recommender/db/model')
api.add_namespace(category_ns, path='/recommender/db/category')
api.add_namespace(item_ns, path='/recommender/db/item')
api.add_namespace(role_ns, path='/recommender/db/role')
api.add_namespace(implicit_ns, path='/recommender/db/implicit')
api.add_namespace(explicit_ns, path='/recommender/db/explicit')
api.add_namespace(item_keyword_ns, path='/recommender/db/item-keyword')
api.add_namespace(role_keyword_ns, path='/recommender/db/role-keyword')


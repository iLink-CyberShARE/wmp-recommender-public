from flask import request
from flask_restplus import Resource
from ..util.dto import TrainDto
from ..service.recommender_service import train_model, get_model_info
from flask_jwt import jwt_required, current_identity

api = TrainDto.api
_train = TrainDto.train

@api.route('/')
class Recommender(Resource):
    @jwt_required()
    @api.response(200, 'The model has been trained successfully.')
    @api.response(500, 'An internal error occured.')
    @api.response(401, 'Not Authorized')
    @api.doc('Trains a recommendation system model')
    @api.expect(_train, validate=True)
    def post(self):
        """ Trains a recommendation system model """
        data = request.json
        if (current_identity.is_contentmanager):
            return train_model(data=data)
        return 'Access Level Not Authorized', 401

    @api.route('/model_id/<model_id>')
    @api.param('model_id', 'The model global unique identifer')
    class ItemByGuid(Resource):
        @api.doc('Gets training information of a model')
        @api.response(200, 'Training metadata was retrived succesfully.')
        @api.response(400, 'Could not find the model.')
        @api.response(500, 'Internal error occurred.')
        def get(self, model_id):
            """Get training information from selected model"""
            return get_model_info(model_id)
    
    

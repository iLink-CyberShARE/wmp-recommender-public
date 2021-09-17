from flask import request
from flask_restplus import Resource
from ..util.dto import ModelDto
from ..service.model_service import get_models, add_model, get_model, delete_model, update_model
from flask_jwt import jwt_required, current_identity

api = ModelDto.api
_model = ModelDto.model

@api.route('/')
class ModelList(Resource):

    @api.doc('Insert new recommender model information on the database')
    @jwt_required()
    @api.response(201, 'Recommender model information successfully added')
    @api.response(400, 'Could not insert recommender model')
    @api.expect(_model, validate=True)
    def post(self):
        """Insert new recommender model information on the database"""
        data = request.json
        if (current_identity.is_contentmanager):
            return add_model(data=data)
        return 'Access Level Not Authorized', 401

    @api.doc('Retrieve recommendation model listing', security=None)
    @api.response(200, 'Model listing has been retrived succesfully.')
    @api.response(404, 'Could not retrive list of models')
    @api.marshal_list_with(_model, envelope='data')
    def get(self):
        """Retrieve recommendation model listing"""
        return get_models()


@api.route('/<guid>')
@api.param('guid', 'Model global unique identifer')
class ModelByGUID(Resource):

    @api.doc('Gets model by GUID', security=None)
    @api.response(200, 'The model was retrived successfully.')
    @api.response(400, 'Could not find the model.')
    def get(self, guid):
        "Retrieve recommender model information by GUID"
        return get_model(guid)

    @api.doc('Updates recommender model information')
    @jwt_required()
    @api.response(200, 'The recommender model was updated succesfully.')
    @api.response(400, 'Could not update the recommender model.')
    @api.expect(_model, validate=True)
    def put(self, guid):
        """Update a recommender model given its unique identifier"""
        data = request.json
        if (current_identity.is_contentmanager):
            return update_model(guid, data)
        return 'Access Level Not Authorized', 401

    @api.doc('Delete model by guid')
    @jwt_required()
    @api.response(200, 'The model was successfully removed.')
    @api.response(400, 'Could not delete model.')
    def delete(self, guid):
        """ Delete recommender model by global unique identifer """
        if (current_identity.is_contentmanager):
            return delete_model(guid)
        return 'Access Level Not Authorized', 401
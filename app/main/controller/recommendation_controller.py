from flask import request
from flask_restplus import Resource
from ..util.dto import RecommendDto
from ..service.recommender_service import role_recommendation

api = RecommendDto.api
_role_req = RecommendDto.role_req
_item_res = RecommendDto.item_res

@api.route('/byrole')
class RoleRecommender(Resource):

    @api.doc('Gets item recommendation by user roles', security=None)
    @api.response(200, 'The request was processed succesfully.')
    @api.response(500, 'An internal error occured.')
    @api.expect(_role_req, validate=True)
    # @api.marshal_list_with(_item_res, envelope='data')
    def post(self):
        """ Gets the item recommendation by user role over a specific model """
        data = request.json
        return role_recommendation(data=data)
        
    
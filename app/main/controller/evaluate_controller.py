from flask import request
from flask_restplus import Resource
from ..util.dto import EvaluationDto
from ..service.recommender_service import evaluate

api = EvaluationDto.api
_evaluation = EvaluationDto.evaluation

@api.route('')
class Recommender(Resource):

    @api.doc('Evaluates a target recommendation model', security=None)
    @api.response(200, 'The request was received succesfully. The selected model was evaluated.')
    @api.response(500, 'Internal error occured')
    @api.expect(_evaluation, validate=True)
    def post(self):
        """ Evaluates a target recommendation model with multiple metrics averaged among all users"""
        data = request.json
        return evaluate(data=data)
    
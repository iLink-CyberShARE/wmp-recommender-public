from flask import request
from flask_restplus import Resource
from ..util.dto import ImplicitDto
from ..service.implicit_service import get_implicit_logs, add_implicit_entry
from flask_jwt import jwt_required

api = ImplicitDto.api
_implicit_log = ImplicitDto.implicit_log

@api.route('/')
class ImplicitList(Resource):
    @api.doc('Retrieve implicit feedback log', security=None)
    @api.response(200, 'Implicit feedback log was retrived succesfully.')
    @api.response(404, 'Could not retrive implicit feedback')
    @api.marshal_list_with(_implicit_log, envelope='data')
    def get(self):
        """Retrieve implicit feedback log from database"""
        return get_implicit_logs()

    @api.doc('Add an implicit feedback entry on the database')
    @jwt_required()
    @api.response(201, 'Implicit entry successfully added')
    @api.response(400, 'Could not add entry')
    @api.expect(_implicit_log, validate=True)
    def post(self):
        """Add an implicit feedback entry on the database"""
        data = request.json
        return add_implicit_entry(data=data)

from flask import request
from flask_restplus import Resource
from ..util.dto import ExplicitDto
from ..service.explicit_service import get_explicit_logs, add_explicit_entry
from flask_jwt import jwt_required

api = ExplicitDto.api
_explicit_log = ExplicitDto.explicit_log

@api.route('/')
class ExplicitList(Resource):
    @api.doc('Retrieve explicit feedback log', security=None)
    @api.response(200, 'Explicit feedback log was retrived succesfully.')
    @api.response(404, 'Could not retrive explicit feedback')
    @api.marshal_list_with(_explicit_log, envelope='data')
    def get(self):
        """Retrieve explicit feedback log from database"""
        return get_explicit_logs()

    @api.doc('Add an explicit feedback entry on the database')
    @jwt_required()
    @api.response(201, 'Explicit feedback entry successfully added')
    @api.response(400, 'Could not add explicit feedback entry')
    @api.expect(_explicit_log, validate=True)
    def post(self):
        """Add an explicit feedback entry on the database"""
        data = request.json
        return add_explicit_entry(data=data)




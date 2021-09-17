from flask import request
from flask_restplus import Resource
from ..util.dto import RoleKeywordDto
from ..service.role_keyword_service import get_keywords_by_role, add_role_keyword, delete_role_keyword
from flask_jwt import jwt_required, current_identity

api = RoleKeywordDto.api
_role_keyword = RoleKeywordDto.role_keyword
_role_keyword_entry = RoleKeywordDto.role_keyword_entry

@api.route('/')
class RoleKeywordList(Resource):
    @api.doc('Insert a new role keyword on the database')
    @jwt_required()
    @api.response(201, 'Keyword successfully added')
    @api.response(400, 'Could not insert keyword')
    @api.expect(_role_keyword_entry, validate=True)
    def post(self):
        """Insert a new role keyword on the database"""
        data = request.json
        if (current_identity.is_contentmanager):
            return add_role_keyword(data=data)
        return 'Access Level Not Authorized', 401

@api.route('/role_id/<role_id>')
@api.param('role_id', 'Role local identifer')
class KeywordsByItem(Resource):
    @api.doc('Gets list of keywords by role')
    @jwt_required()
    @api.response(200, 'The keywords were retrived succesfully.')
    @api.response(400, 'Could not find the item id.')
    @api.response(500, 'Internal error occurred.')
    @api.marshal_list_with(_role_keyword, envelope='data')
    def get(self, role_id):
        """Gets list of keywords by role"""
        return get_keywords_by_role(role_id)

@api.route('/<db_id>')
@api.param('db_id', 'Keyword unique identifier')
class KeywordById(Resource):
    @api.doc('Delete keyword by id')
    @jwt_required()
    @api.response(200, 'The keyword was successfuly removed.')
    @api.response(400, 'Could not delete keyword.')
    def delete(self, db_id):
        """ Delete keyword by identifer """
        if (current_identity.is_contentmanager):
            return delete_role_keyword(db_id)
        return 'Access Level Not Authorized', 401
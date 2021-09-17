from flask import request
from flask_restplus import Resource
from ..util.dto import ItemKeywordDto
from ..service.item_keyword_service import get_keywords_by_item, add_item_keyword, delete_item_keyword
from flask_jwt import jwt_required, current_identity

api = ItemKeywordDto.api
_item_keyword = ItemKeywordDto.item_keyword
_item_keyword_entry = ItemKeywordDto.item_keyword_entry

@api.route('/')
class ItemKeywordList(Resource):
    @api.doc('Insert a new item keyword on the database')
    @jwt_required()
    @api.response(201, 'Keyword successfully added')
    @api.response(400, 'Could not insert keyword')
    @api.expect(_item_keyword_entry, validate=True)
    def post(self):
        """Insert a new item keyword on the database"""
        data = request.json
        if (current_identity.is_contentmanager):
            return add_item_keyword(data=data)
        return 'Access Level Not Authorized', 401

@api.route('/item_id/<item_id>')
@api.param('item_id', 'Item local identifer')
class KeywordsByItem(Resource):
    @api.doc('Gets list of keywords by item')
    @jwt_required()
    @api.response(200, 'The keywords were retrived succesfully.')
    @api.response(400, 'Could not find the item id.')
    @api.response(500, 'Internal error occurred.')
    @api.marshal_list_with(_item_keyword, envelope='data')
    def get(self, item_id):
        """Gets list of keywords by item"""
        return get_keywords_by_item(item_id)

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
            return delete_item_keyword(db_id)
        return 'Access Level Not Authorized', 401

    
from flask import request
from flask_restplus import Resource
from ..util.dto import ItemDto
from ..service.item_service import get_all_items, get_item_by_guid, add_item, delete_item, get_item, update_item
from flask_jwt import jwt_required, current_identity

api = ItemDto.api
_item = ItemDto.item
_item_entry = ItemDto.item_entry

@api.route('/')
class ItemList(Resource):
    @api.doc('Insert a new item on the database')
    @jwt_required()
    @api.response(201, 'Item successfully added')
    @api.response(400, 'Could not insert item')
    @api.expect(_item_entry, validate=True)
    def post(self):
        """Insert a new item on the database"""
        data = request.json
        if (current_identity.is_contentmanager):
            return add_item(data=data)
        return 'Access Level Not Authorized', 401

    @api.doc('List all items')
    @jwt_required()
    @api.response(200, 'The list of items was retrived succesfully.')
    @api.response(500, 'Internal error occurred.')
    @api.marshal_list_with(_item, envelope='data')
    def get(self):
        """Listing of all items available on the database"""
        return get_all_items()

@api.route('/guid/<guid>')
@api.param('guid', 'The global unique identifer')
class ItemByGuid(Resource):
    @api.doc('Gets local identifer by guid')
    @jwt_required()
    @api.response(200, 'The item was retrived succesfully.')
    @api.response(400, 'Could not find the output.')
    @api.response(500, 'Internal error occurred.')
    def get(self, guid):
        """Query item by global unique identifer value"""
        return get_item_by_guid(guid)

@api.route('/<db_id>')
@api.param('db_id', 'Item unique identifier')
class ItemById(Resource):
    @api.doc('Updates an item')
    @jwt_required()
    @api.response(200, 'The item was updated succesfully.')
    @api.response(400, 'Could not update the item')
    @api.expect(_item_entry, validate=True)
    def put(self, db_id):
        """Update an item given its unique identifier"""
        data = request.json
        if (current_identity.is_contentmanager):
            return update_item(db_id, data)
        return 'Access Level Not Authorized', 401

    @api.doc('Gets item by unique id')
    @jwt_required()
    @api.response(200, 'The item was retrived successfully.')
    @api.response(400, 'Could not find the item')
    def get(self, db_id):
        "Retrieve item by unique identifer"
        return get_item(db_id)

    @api.doc('Delete item by id')
    @jwt_required()
    @api.response(200, 'The item was successfuly removed.')
    @api.response(400, 'Could not delete item.')
    def delete(self, db_id):
        """ Delete item by unique identifer """
        if (current_identity.is_contentmanager):
            return delete_item(db_id)
        return 'Access Level Not Authorized', 401
    
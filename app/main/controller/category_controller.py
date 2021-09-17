from flask import request
from flask_restplus import Resource
from ..util.dto import CategoryDto
from ..service.category_service import  get_categories, get_category, add_category, delete_category, update_category
from flask_jwt import jwt_required, current_identity

api = CategoryDto.api
_category = CategoryDto.category
_category_entry = CategoryDto.category_entry

@api.route('/')
class Categories(Resource):
    @api.doc('List of all item categories')
    @jwt_required()
    @api.response(200, 'The list of categories was retrived succesfully.')
    @api.response(500, 'Internal error occured.')
    @api.marshal_list_with(_category, envelope='data')
    def get(self):
        """Listing of all item categories available on the database"""
        return get_categories()

    @api.doc('Insert a new category on the database')
    @jwt_required()
    @api.response(201, 'Category successfully added')
    @api.response(400, 'Could not insert category')
    @api.expect(_category_entry, validate=True)
    def post(self):
        """Insert a new category on the database"""
        data = request.json
        if (current_identity.is_contentmanager):
            return add_category(data=data)
        return 'Access Level Not Authorized', 401

@api.route('/<db_id>')
@api.param('db_id', 'Category unique identifier')
class CategoryById(Resource):
    @api.doc('Gets category by unique id')
    @jwt_required()
    @api.response(200, 'The category was retrived successfully.')
    @api.response(400, 'Could not find the category.')
    def get(self, db_id):
        "Retrieve category by unique identifer"
        return get_category(db_id)

    @api.doc('Updates an item category')
    @jwt_required()
    @api.response(200, 'The category was updated succesfully.')
    @api.response(400, 'Could not category the role.')
    @api.expect(_category_entry, validate=True)
    def put(self, db_id):
        """Update an item category given its unique identifier"""
        data = request.json
        if (current_identity.is_contentmanager):
            return update_category(db_id, data)
        return 'Access Level Not Authorized', 401

    @api.doc('Delete item category by id')
    @jwt_required()
    @api.response(200, 'The category was successfuly removed.')
    @api.response(400, 'Could not delete category.')
    def delete(self, db_id):
        """ Delete category by unique identifer """
        if (current_identity.is_contentmanager):
            return delete_category(db_id)
        return 'Access Level Not Authorized', 401
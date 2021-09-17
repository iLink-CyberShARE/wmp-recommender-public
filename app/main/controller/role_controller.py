from flask import request
from flask_restplus import Resource
from ..util.dto import RoleDto
from ..service.role_service import  get_all_roles, get_role_by_name, add_role, get_role, update_role, delete_role
from flask_jwt import jwt_required, current_identity

api = RoleDto.api
_role = RoleDto.role
_role_entry = RoleDto.role_entry

@api.route('/')
class Roles(Resource):

    @api.doc('List of all roles')
    @jwt_required()
    @api.response(200, 'The list of roles was retrived succesfully.')
    @api.response(500, 'Internal error occured.')
    @api.marshal_list_with(_role, envelope='data')
    def get(self):
        """Listing of all roles available on the database"""
        return get_all_roles()

    @api.doc('Insert a new role on the database')
    @jwt_required()
    @api.response(201, 'Role successfully added')
    @api.response(400, 'Could not insert role')
    @api.expect(_role_entry, validate=True)
    def post(self):
        """Insert a new role on the database"""
        data = request.json
        if (current_identity.is_contentmanager):
            return add_role(data=data)
        return 'Access Level Not Authorized', 401

@api.route('/rolename/<rolename>')
@api.param('rolename', 'The role name')
class RoleByName(Resource):
    @api.doc('Gets the role id  by name')
    @jwt_required()
    @api.response(200, 'The role was retrived succesfully.')
    @api.response(400, 'Could not find the role.')
    @api.response(500, 'Internal error occurred.')
    def get(self, rolename):
        """Query for unique identifier by role name"""
        return get_role_by_name(rolename)

@api.route('/<db_id>')
@api.param('db_id', 'Role unique identifier')
class RoleById(Resource):
    @api.doc('Gets role by unique id')
    @jwt_required()
    @api.response(200, 'The role was retrived successfully.')
    @api.response(400, 'Could not find the role.')
    def get(self, db_id):
        "Retrieve role by unique identifer"
        return get_role(db_id)

    @api.doc('Updates a user role')
    @jwt_required()
    @api.response(200, 'The role was updated succesfully.')
    @api.response(400, 'Could not update the role.')
    @api.expect(_role_entry, validate=True)
    def put(self, db_id):
        """Update a user role given its unique identifier"""
        data = request.json
        if (current_identity.is_contentmanager):
            return update_role(db_id, data)
        return 'Access Level Not Authorized', 401

    @api.doc('Delete role by id')
    @jwt_required()
    @api.response(200, 'The role was successfuly removed.')
    @api.response(400, 'Could not delete role.')
    def delete(self, db_id):
        """ Delete role by unique identifer """
        if (current_identity.is_contentmanager):
            return delete_role(db_id)
        return 'Access Level Not Authorized', 401

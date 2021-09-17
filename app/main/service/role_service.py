from app.main.model.role import Role
from flask import abort
from app.main.database import db_session
from sqlalchemy.exc import SQLAlchemyError

'''
Query and CRUD Operations available for the user role/group table.
'''

#### Query operations ####

def get_all_roles():
    '''
    Gets a listing of all the user roles available on the database.
    '''
    try:
        session = db_session()
        result = db_session.query(Role).all()
        session.close()
        return result

    except SQLAlchemyError as e:
        session.rollback()
        response = {
            'status': 'fail',
            'message': str(e)
        }
        return response, 500  

    except Exception as e:
        response = {
            'status': 'fail',
            'message': str(e)
        }
        return response, 500  
    
def get_role_by_name(name):
    '''
    Returns the identifier of a role with a query by name.
    '''
    try:
        session = db_session()
        role = session.query(Role).filter(Role.name == name).first()
        if role:
            response_object = {
                'status': 'success',
                'id': role.id
            }
            session.close()
            return response_object, 200
        else:
            session.close()
            abort(400, 'Role name not found')

    except SQLAlchemyError as e:
        session.rollback()
        response = {
            'status': 'fail',
            'message': str(e)
        }
        return response, 500  

    except Exception as e:
        response = {
            'status': 'fail',
            'message': str(e)
        }
        return response, 500

def get_role(id):
    '''
    Get role by local id
    '''
    try:
        session = db_session()
        role = session.query(Role).filter(Role.id == id).first()
        if role:
            response_object = {
                'status': 'success',
                'data': {
                    'id' : role.id,
                    'name': role.name
                }
            }
            session.close()
            return response_object, 200
        else:
            session.close()
            abort(400, 'Role does not exist')

    except SQLAlchemyError as e:
        session.rollback()
        response = {
            'status': 'fail',
            'message': str(e)
        }
        return response, 500 

    except Exception as e:
        response = {
            'status': 'fail',
            'message': str(e)
        }
        return response, 500

#### CRUD Operations ####

def add_role(data):
    '''
    Adds a role to the database.
    '''
    try:
        session = db_session()
        role = session.query(Role).filter(Role.name == data['name']).first()
        if not role:
            role = Role(
                name=data['name']
            )
            save_changes(role)
            response_object = {
                'status': 'success',
                'message': 'Role was created succesfully.',
            }
            session.close()
            return response_object, 201
        else:
            session.close()
            abort(409, 'Role name has already been used')

    except SQLAlchemyError as e:
        session.rollback()
        response = {
            'status': 'fail',
            'message': str(e)
        }
        return response, 500  

    except Exception as e:
        response = {
            'status': 'fail',
            'message': str(e)
        }
        return response, 500


def update_role(id, data):
    '''
    Update role row by id
    '''
    try:
        session = db_session()
        role = session.query(Role).filter(Role.id == id).first()
        if role:
            role.name = data['name']
            save_changes(role)
            response_object = {
                'status': 'success',
                'message': 'Role was updated succesfully.'
            }
            session.close()
            return response_object, 200
        else:
            session.close()
            abort(400, 'Role does not exist')

    except SQLAlchemyError as e:
        session.rollback()
        response = {
            'status': 'fail',
            'message': str(e)
        }
        return response, 500

    except Exception as e:
        response = {
            'status': 'fail',
            'message': str(e)
        }
        return response, 500


def delete_role(id):
    '''
    Delete role row by id
    '''
    try:
        session = db_session()
        role = session.query(Role).filter(Role.id == id).first()
        if role:
            delete_changes(role)
            response_object = {
                'status': 'success',
                'message': 'Role was deleted succesfully.'
            }
            session.close()
            return response_object, 200
        else:
            session.close()
            abort(400, 'Role not found')

    except SQLAlchemyError as e:
        session.rollback()
        response = {
            'status': 'fail',
            'message': str(e)
        }
        return response, 500 

    except Exception as e:
        response = {
            'status': 'fail',
            'message': str(e)
        }
        return response, 500

### Database Helper Functions ###

def save_changes(data):
    db_session.add(data)
    db_session.commit()

def delete_changes(data):
    db_session.delete(data)
    db_session.commit()



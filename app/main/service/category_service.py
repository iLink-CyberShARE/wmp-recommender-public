from app.main.model.category import Category
from flask import abort
from app.main.database import db_session
from sqlalchemy.exc import SQLAlchemyError

'''
Query and CRUD Operations available for the item category table
'''

#### Query operations ####

def get_categories():
    '''
    Gets a listing of all item categories available on the database.
    '''
    try:
        session = db_session()
        result = session.query(Category).all()
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


def get_category(id):
    '''
    Get category by local id
    '''
    try:
        session = db_session()
        category = session.query(Category).filter(Category.id == id).first()
        session.close()

        if category:
            response_object = {
                'status': 'success',
                'data': {
                    'id' : category.id,
                    'name': category.name
                }
            }
            return response_object, 200
        else:
            abort(400, 'Category does not exist')

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

def add_category(data):
    '''
    Adds an item category to the database.
    '''
    try:
        session = db_session()
        category = session.query(Category).filter(Category.name == data['name']).first()
        if not category:
            category = Category(
                name=data['name']
            )
            save_changes(category)
            session.close()
            response_object = {
                'status': 'success',
                'message': 'Category was created succesfully.',
            }
            return response_object, 201
        else:
            session.close()
            abort(409, 'Category name has already been used')

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


def update_category(id, data):
    '''
    Update item category row by id
    '''
    try:
        session = db_session()
        category = session.query(Category).filter(Category.id == id).first()
        if category:
            category.name = data['name']
            save_changes(category)
            session.close()
            response_object = {
                'status': 'success',
                'message': 'Category was updated succesfully.'
            }
            
            return response_object, 200
        else:
            session.close()
            abort(400, 'Category does not exist')

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

def delete_category(id):
    '''
    Delete item category row by id
    '''
    try:
        session = db_session()
        category = session.query(Category).filter(Category.id == id).first()
        if category:
            delete_changes(category)
            session.close()
            response_object = {
                'status': 'success',
                'message': 'Category was deleted succesfully.'
            }
            return response_object, 200
        else:
            session.close()
            abort(400, 'Category not found')

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

from flask import abort
from app.main.model.role_keyword import Role_keyword
from app.main.database import db_session
from sqlalchemy.exc import SQLAlchemyError

### Query Operations ###

def get_keywords_by_role(role_id):
    '''
    Get list of keywords by role id
    '''
    try: 
        session = db_session()
        result = session.query(Role_keyword).filter(Role_keyword.role_id == role_id).all()
        if result:
            session.close()
            return result
        else:
            session.close()
            abort(400, 'No keywords found')

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

def add_role_keyword(data):
    '''
    Adds an item keyword to the database.
    '''
    try:
        session = db_session()
        role_keyword = Role_keyword(
            role_id=data['role_id'],
            keyword=data['keyword'],
            weight=data['weight']
        )
        save_changes(role_keyword)
        session.close()
        response_object = {
            'status': 'success',
            'message': 'Role keyword was added succesfully.',
        }
        return response_object, 201

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

def delete_role_keyword(id):
    '''
    Delete role keyword by id
    '''
    try:
        session = db_session()
        role_keyword = session.query(Role_keyword).filter(Role_keyword.id == id).first()
        if role_keyword:
            delete_changes(role_keyword)
            session.close()
            response_object = {
                'status': 'success',
                'message': 'Role keyword was deleted succesfully.'
            }
            return response_object, 200
        else:
            session.close()
            abort(400, 'Keyword id not found')

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

#### Database Utils ####
def save_changes(data):
    db_session.add(data)
    db_session.commit()

def delete_changes(data):
    db_session.delete(data)
    db_session.commit()
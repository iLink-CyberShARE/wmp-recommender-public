from flask import abort
from app.main.database import db_session
from app.main.model.implicit_log import Implicit_log
from sqlalchemy.exc import SQLAlchemyError

#### Query Operations ####

def get_implicit_logs():
    '''
    Get complete log of implicit user interactions
    '''
    try:
        session = db_session()
        result = session.query(Implicit_log).all()
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

#### CRUD Operations ####

def add_implicit_entry(data):
    '''
    Add a user interaction entry to the implicit log table
    '''
    try:
        session = db_session()
        implicit_log = Implicit_log(
            item_id=data['item_id'],
            user_id=data['user_id'],
            run_id=data['run_id'],
            role_id=data['role_id']
        )
        save_changes(implicit_log)
        session.close()
        response_object = {
            'status': 'success',
            'message': 'Implict entry added successfully',
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

#### Database Utils ####

def save_changes(data):
    db_session.add(data)
    db_session.commit()


def delete_changes(data):
    db_session.delete(data)
    db_session.commit()

from flask import abort
from app.main.database import db_session
from app.main.model.explicit_log import Explicit_log
from sqlalchemy.exc import SQLAlchemyError

#### Query Operations ####

def get_explicit_logs():
    '''
    Get complete log of explicit user feedback
    '''
    try:
        session = db_session()
        result = session.query(Explicit_log).all()
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

def add_explicit_entry(data):
    '''
    Add a explicit feedback entry into the log table
    '''
    try:
        session = db_session()
        explicit_log = Explicit_log(
            item_id=data['item_id'],
            rank_value=data['rank_value'],
            user_id=data['user_id'],
            run_id=data['run_id'],
            role_id=data['role_id']
        )
        save_changes(explicit_log)
        session.close()
        response_object = {
            'status': 'success',
            'message': 'Explicit feedback entry added successfully',
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

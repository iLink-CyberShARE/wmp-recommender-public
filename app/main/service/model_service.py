from flask import abort
from app.main.database import db_session
from app.main.model.model import Model
from sqlalchemy.exc import SQLAlchemyError

#### Query Operations ####

def get_models():
    '''
    Get complete listing of registered recommendation model instances
    '''
    try:
        session = db_session()
        result = session.query(Model).all()
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

def get_model(guid):
    '''
    Get model by id
    '''
    try:
        session = db_session()
        model = session.query(Model).filter(Model.id == guid).first()
        if model:
            response_object = {
                'status': 'success',
                'data': {
                    'id' : model.id,
                    'name': model.name,
                    'context_iri' : model.context_iri
                }
            }
            session.close()
            return response_object, 200
        else:
            session.close()
            abort(400, 'Model does not exist')

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

def add_model(data):
    '''
    Add recommender model entry
    '''
    try:
        session = db_session()
        model = Model(
            id=data['id'],
            name=data['name'],
            context_iri=data['context_iri']
        )
        save_changes(model)
        session.close()
        response_object = {
            'status': 'success',
            'message': 'Recommender model information added successfully',
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


def update_model(guid, data):
    '''
    Update recommender model by guid
    '''
    try:
        session = db_session()
        model = session.query(Model).filter(Model.id == guid).first()
        if model:
            model.id = data['id']
            model.name = data['name']
            model.context_iri = data['context_iri']
            save_changes(model)
            session.close()

            response_object = {
                'status': 'success',
                'message': 'Model was updated succesfully.'
            }
            
            return response_object, 200
        else:
            session.close()
            abort(400, 'Model does not exist')

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


def delete_model(guid):
    '''
    Delete model row by id
    '''
    try:
        session = db_session()
        model = session.query(Model).filter(Model.id == guid).first()
        if model:
            delete_changes(model)
            session.close()
            response_object = {
                'status': 'success',
                'message': 'Model was deleted succesfully.'
            }
            return response_object, 200
        else:
            session.close()
            abort(400, 'Model not found')

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

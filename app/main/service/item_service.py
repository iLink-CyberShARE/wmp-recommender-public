from flask import abort
from app.main.model.item import Item
from app.main.database import db_session
from sqlalchemy.exc import SQLAlchemyError

#### Query Operations ####

def get_all_items():
    '''
    Get a listing of all items available on the database
    '''
    try:
        session = db_session()
        result = session.query(Item).all()
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

def get_item_by_guid(guid):
    '''
    Get an item identifier by guid
    '''
    try: 
        session = db_session()
        item = session.query(Item).filter(Item.guid == guid).first()
        if item:
            response_object = {
                'status': 'success',
                'id': item.id
            }
            session.close()
            return response_object, 200
        else:
            session.close()
            abort(400, 'Item not found')

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

def get_item(id):
    '''
    Get item by local id
    '''
    try:
        session = db_session()
        item = session.query(Item).filter(Item.id == id).first()
        if item:
            response_object = {
                'status': 'Success',
                'data': {
                    'id' : item.id,
                    'model_id': item.model_id,
                    'category_id': item.category_id,
                    'guid': item.guid,
                    'name': item.name
                }
            }
            session.close()
            return response_object, 200
        else:
            session.close()
            abort(400, 'Item does not exist')

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

def add_item(data):
    '''
    Adds an item to the database making sure the guid field is unique.
    '''
    try:
        session = db_session()
        item = session.query(Item).filter(Item.guid == data['guid']).first()
        if not item:
            item = Item(
                model_id=data['model_id'],
                category_id=data['category_id'],
                guid= data['guid'],
                name=data['name']
            )
            save_changes(item)
            session.close()
            response_object = {
                'status': 'success',
                'message': 'Item was created succesfully.',
            }
            return response_object, 201
        else:
            session.close()
            abort(409, 'Item guid already exists')

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
    

def delete_item(id):
    '''
    Delete item row by id
    '''
    try:
        session = db_session()
        item = session.query(Item).filter(Item.id == id).first()
        if item:
            delete_changes(item)
            session.close()
            response_object = {
                'status': 'success',
                'message': 'Item was deleted succesfully.'
            }
            return response_object, 200
        else:
            session.close()
            abort(400, 'Item not found')

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


def update_item(id, data):
    '''
    Update item row by id
    '''
    try:
        session = db_session()
        item = db_session.query(Item).filter(Item.id == id).first()

        if item:
            item.model_id = data['model_id']
            item.category_id = data['category_id']
            item.guid = data['guid']
            item.name = data['name']
            save_changes(item)
            session.close()
            
            response_object = {
                'status': 'success',
                'message': 'Item was updated succesfully.'
            }
            
            return response_object, 200
        else:
            session.close()
            abort(400, 'Item does not exist')

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
    

def save_changes(data):
    db_session.add(data)
    db_session.commit()


def delete_changes(data):
    db_session.delete(data)
    db_session.commit()

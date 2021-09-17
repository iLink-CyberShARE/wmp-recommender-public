from flask import abort
from app.main.model.item_keyword import Item_keyword
from app.main.database import db_session
from sqlalchemy.exc import SQLAlchemyError

### Query Operations ###

def get_keywords_by_item(item_id):
    '''
    Get list of keywords by item id
    '''
    try: 
        session = db_session()
        result = session.query(Item_keyword).filter(Item_keyword.item_id == item_id).all()
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

def add_item_keyword(data):
    '''
    Adds an item keyword to the database.
    '''
    try:
        session = db_session()
        item_keyword = Item_keyword(
            item_id=data['item_id'],
            keyword=data['keyword'],
            weight=data['weight']
        )
        save_changes(item_keyword)
        session.close()
        response_object = {
            'status': 'success',
            'message': 'Item keyword was added succesfully.',
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

def delete_item_keyword(id):
    '''
    Delete item keyword by id
    '''
    try:
        session = db_session()
        item_keyword = session.query(Item_keyword).filter(Item_keyword.id == id).first()
        if item_keyword:
            delete_changes(item_keyword)
            session.close()
            response_object = {
                'status': 'success',
                'message': 'Item keyword was deleted succesfully.'
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
import os
import sys
import unittest
import datetime
import uuid
from flask import Flask
from flask_cors import CORS
from flask_script import Manager, Command
from flask_jwt import JWT
from datetime import datetime, timedelta
from app.main.database import db_session
from app import blueprint
from app.main.security import authenticate, identity, getKey
from app.main.optimization.hyper_param_opt import start_opt_studies


class FlagManager(Manager):
    def command(self, capture_all=False):
        def decorator(func):
            command = Command(func)
            command.capture_all_args = capture_all
            self.add_command(func.__name__, command)

            return func
        return decorator

app = Flask(__name__)
app.debug = True
CORS(app)
app.register_blueprint(blueprint)

app.config['JWT_SECRET_KEY'] = getKey(1)
app.config['JWT_VERIFY_CLAIMS'] = ['exp', 'iat']
app.config['JWT_REQUIRED_CLAIMS'] = ['exp', 'iat']
app.config['JWT_AUTH_HEADER_PREFIX'] = 'Bearer'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
jwt = JWT(app, authenticate, identity)

app.app_context().push()
manager = FlagManager(app)

@manager.command()
def run():
    app.run(host='0.0.0.0', port='5000')
   
@manager.command()
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@manager.command()
def optimize():
    """Runs hyperparameter optimization trials."""
    start_opt_studies()

@app.teardown_appcontext
def remove_session(*args, **kwargs):
    """Closes the database session."""
    db_session.remove()

@jwt.jwt_payload_handler
def custom_payload_handler(identity):
    iat = datetime.utcnow()
    exp = iat + app.config.get('JWT_EXPIRATION_DELTA')
    id = getattr(identity, 'uid') or identity['uid']
    email = getattr(identity, 'uemail') or identity['uemail']
    cont = getattr(identity, 'is_contentmanager') or identity['is_contentmanager']
    cont_int = int(cont == True) 
    token = {'email': email, 'id': id, 'cont': cont_int, 'iat': iat, 'exp': exp}
    return token


if __name__ == '__main__':
    manager.run()


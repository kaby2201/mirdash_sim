from flask import Flask, request, make_response
from flask_restplus import Api, Resource, fields
from werkzeug.exceptions import *
from base64 import b64encode
from hashlib import sha256
from functools import wraps

robot_base_url = '/api/v2.0.0'

authorization_username = 'admin'
authorization_password = sha256(b'Password1.').hexdigest()
authorization_token = 'Basic {}'.format(
    b64encode(bytes(
        '{}:{}'.format(authorization_username, authorization_password)
        , 'utf-8'
    )).decode('utf-8')
)
print('Authorization token:', authorization_token)

app = Flask(__name__)
api = Api(app,
          version='1.0',
          title='Robot API',
          description='Simulation API for MiR Robot',
          default_mediatype='application/json',
          authorizations={
              'BasicAuth': {
                  'type': 'basic',
              }
          })

ns = api.namespace('Robot API', description='TODO operations')


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == authorization_username and auth.password == authorization_password:
            return f(*args, **kwargs)
        else:
            api.abort(401, 'Could not authorize')

    return decorated

# app/__init__.py

from flask_restplus import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='MiRDash sim api',
          version='1.0',
          description='Unofficially mobile industrial robots api'
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns)
# merixstudio.com/blog/best-practices-rest-api-development/


from flask import Flask, jsonify, request, redirect
from flask_cors import CORS
from flask import Blueprint, url_for
import mysql.connector
import logging.handlers
import sys, os
from flask_restx import Api, Resource, fields, reqparse, inputs
from werkzeug.datastructures import FileStorage

# logger config
#
LOG_FILENAME = 'Logging.log'
FORMAT = '%(levelname)7s%(name)10s%(filename)15s:%(lineno)4d ' \
         '-%(funcName)8s %(asctime)s, %(msecs)s, %(message)s'

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig(
    filename=LOG_FILENAME,
    filemode='a',
    level=logging.INFO,
    format=FORMAT,
    datefmt='%H:%M:%S')
filehandler = logging.handlers.RotatingFileHandler(
    LOG_FILENAME, maxBytes=5*1024*1024, backupCount=3)
logger.addHandler(filehandler)

# Intializing flask app
app = Flask(__name__, instance_relative_config=True, 
            template_folder='static/templates')

# Intializing CORS
CORS(app)

# root path of the appication
ROOT = app.root_path

URL_PREFIX = '/api/v1'

class MyApi(Api):
    @property
    def specs_url(self):
        """Monkey patch for HTTPS"""
        scheme = 'https' if 'api.hobasa.io' in self.base_url else 'http'
        return url_for(self.endpoint('specs'), _external=True, _scheme=scheme)

blueprint = Blueprint('api', __name__, url_prefix=URL_PREFIX)
api = MyApi(blueprint, title = "Test App", version = "1.0",
    description = "Test API's")
app.register_blueprint(blueprint)

user_model = api.model("create user", {
    "first_name": fields.String(required=True, description="users first name"),
    "last_name": fields.String,
    "status": fields.String(enum=['Approved', 'Rejected', 'Pending'])
})

form_data_model = api.parser()
form_data_model.add_argument("file_name", type=str, 
    location='form',
    help='type of form like i9, direct_deposit, notice_coverage'+\
        ' and drug_and_alcohol_consent ect,.',
     required=True)
form_data_model.add_argument("file", type=FileStorage,
     location='files', required=True)


user_get_model = api.parser()
user_get_model.add_argument("id", type=str, 
    location='args', required=True)

greet_api = api.namespace("greet", description="To send greetings")

@greet_api.route('/hello')
class Greet(Resource):
    def get(self):
        logger.info("Greeting")
        return {"msg": "Hello World!"}
    



@greet_api.route('/holidays')
class GreetOnHolidays(Resource):
    def get(self):
        return {"msg": "Hey, Today is holiday!"}
    
    def post(self):
        return {"msg": "Hey, Today is holiday!"}
    
    def patch(self):
        return {"msg": "Hey, Today is holiday!"}
    
    def delete(self):
        return {"msg": "Hey, Today is holiday!", "success": True}


user_api = api.namespace("user", description="User related APIs")

@user_api.route('')
class Users(Resource):
    @user_api.expect(user_get_model, validate=True)
    def get(self, id=None):
        """Returns users list"""
        return {"data": {"users": []}}

    @user_api.expect(user_model, validate=True)
    def post(self):
        return {}

    @user_api.expect(form_data_model, validate=True)
    def patch(self):
        return {}
@app.route("/")
def index():
    """
    Redirection to swagger home page
    """
    return redirect('/api/v1')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
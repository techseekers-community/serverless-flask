from flask_bcrypt import generate_password_hash, check_password_hash
from util import email_check, generate_confirmation_token, confirm_token
from notification import send_sms, send_email
from schemes import UserLoginSchema, UserRegisterSchema
from dynamodb import User
from werkzeug.exceptions import HTTPException,  BadRequest
import json
from loguru import logger

from flask_cors import CORS, cross_origin
from flask import Flask, jsonify, request, url_for, render_template_string, flash, redirect
from config import SECURITY_PASSWORD_SALT, SECRET_KEY, SENDER, EMAIL_CONFIRMATION_HTML, EMAIL_CONFIRMATION_TEXT, FRONTEND
import random
from webargs.flaskparser import use_args

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager


app = Flask(__name__)
jwt = JWTManager(app)
app.config['SECRET_KEY'] = SECRET_KEY
app.config["JWT_SECRET_KEY"] = "sdfdsfzegsdt343#"
cors = CORS(app, resources={
            r"/api/*": {"origins": ["https://www.apigatewaystage.co.in"]}}, supports_credentials=True)


@app.route("/api/")
def hello():
    return "Hello World!"


@app.route("/api/user")
@jwt_required()
def get_user():
    current_user = get_jwt_identity()
    logger.debug(f"Getting user by id {current_user}")
    item = User.get_user_by_id(current_user)
    if not item:
        raise BadRequest('User does not exist')
    return jsonify({
        'email': item['userId'],
        'firstName': item['fname'],
        'lastName': item['lname'],
        'gender': item['gender'],
        'dob': item['dob'],
    })


user_login_schema = UserLoginSchema()

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.


@app.route("/api/login", methods=["POST"])
@use_args(user_login_schema)
def login(user):
    email = user['email']
    item = User.get_user_by_id(email)
    if item is None:
        raise BadRequest(f"User with email addess {email} does not exist.")
    if not item['confirmed']:
        raise BadRequest(f"User with email addess {email} not confirmed.")
    if not check_password_hash(bytes(item['password']), user['password'] + SECURITY_PASSWORD_SALT):
        raise BadRequest(f"Invalid password.")
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)


user_register_schema = UserRegisterSchema()


@app.route("/api/register", methods=["POST"])
@use_args(user_register_schema)
def create_user(user):

    password = generate_password_hash(
        user['password'] + SECURITY_PASSWORD_SALT)
    token = generate_confirmation_token(user['email'])

    User.put_new_user(user['email'], user['firstName'],
                      user['lastName'], user['dob'], user['gender'], password)

    # confirm_url = url_for('confirm_email', token=token, _external=True)
    confirm_url = f"{FRONTEND}/confirm/{token}"
    subject = "Please confirm your email"
    bodyHtml = render_template_string(
        EMAIL_CONFIRMATION_HTML, confirm_url=confirm_url)
    bodyText = render_template_string(
        EMAIL_CONFIRMATION_TEXT, confirm_url=confirm_url)
    send_email(SENDER, user['email'], bodyHtml, bodyText, subject)
    return jsonify({'message': 'Verification link is sent to your email ' + user['email'] + 'click on the activation link and sign in.'})


@app.route("/api/confirm/<token>", methods=["GET"])
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        raise BadRequest(f"The confirmation link is invalid or has expired.")

    user = User.get_user_by_id(email)
    if user['confirmed']:
        raise BadRequest(f'Account already confirmed. Please login.')
    else:
        User.confirm_user(email)
        return jsonify({'message': 'Thanks! You have confirmed your account. You will be redirected to login page.'})


@ app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()

    # replace the body with JSON
    json_data = {
        "code": e.code,
        "name": e.name,
        "description": e.description,
    }

    if hasattr(e, 'data'):
        json_data['message'] = e.data.get('messages').get('json')
    response.data = json.dumps(json_data)
    response.content_type = "application/json"
    return response


@ app.after_request
def after(response):
    if response.status_code == 200:
        if response.is_json:
            response.data = json.dumps({"success": response.get_json()})
        else:
            response.data = json.dumps(
                {"success": response.data.decode('utf-8')})
    else:
        response.status_code = 200
        if response.is_json:
            response.data = json.dumps({"error": response.get_json()})
        else:
            response.data = json.dumps(
                {"error": response.data.decode('utf-8')})
    return response

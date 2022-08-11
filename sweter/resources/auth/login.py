from cerberus import Validator
from flask import make_response, render_template, url_for, flash
from flask_login import login_user
from flask_restful import Resource
from werkzeug.security import check_password_hash
from werkzeug.utils import redirect

from schemas.utils.errors_list import errors_list
from schemas.utils.error_handler import CustomErrorHandler
from sweter.schemas.login_schema import SCHEMA
from sweter.database.models import User
from sweter import parser

parser.add_argument('login', location='form')
parser.add_argument('password', location='form')


class Login(Resource):
    def get(self):
        return make_response(render_template('auth/login.html'))

    def post(self):
        v = Validator(SCHEMA, error_handler=CustomErrorHandler)
        v.allow_unknown = True

        data = parser.parse_args()

        if v.validate(data):

            login = data['login']
            password = data['password']

            user = User.query.filter_by(acc_login=login).first()
            if user and check_password_hash(user.acc_password, password):
                login_user(user)
                return make_response(redirect(url_for('index')))
            else:
                flash("Не правильний логін чи пароль")
                return make_response(render_template('auth/login.html'))
        else:
            errors = errors_list(v.errors)
            return make_response(render_template('auth/login.html', errors=errors))
from flask import make_response, render_template, url_for, flash
from flask_login import login_user
from flask_restful import Resource
from werkzeug.security import check_password_hash
from werkzeug.utils import redirect

from sweter.database.models import User
from sweter import parser

parser.add_argument('login', location='form')
parser.add_argument('password', location='form')
parser.add_argument('password2', location='form')


class Login(Resource):
    def get(self):
        return make_response(render_template('login.html'))

    def post(self):
        data = parser.parse_args()

        login = data['login']
        password = data['password']

        if login and password:
            user = User.query.filter_by(acc_login=login).first()
            if user and check_password_hash(user.acc_password, password):
                login_user(user)
                return make_response(redirect(url_for('index')))
            else:
                flash("Не правильний логін чи пароль")
                return make_response(render_template('login.html'))
        else:
            flash("Заповніть усі поля")
            return make_response(render_template('login.html'))

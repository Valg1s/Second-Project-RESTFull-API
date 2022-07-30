from flask import make_response, redirect, url_for
from flask_login import logout_user
from flask_restful import Resource


class Logout(Resource):
    def get(self):
        logout_user()
        return make_response(redirect(url_for('index')))
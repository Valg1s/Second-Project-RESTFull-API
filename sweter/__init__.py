from flask import Flask
from flask_admin import Admin, expose, AdminIndexView
from flask_restful import Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user


class MainPage(AdminIndexView):
    @expose('/')
    def main_page(self):
        if current_user.is_authenticated:
            return self.render('/admin/logined.html')
        else:
            return self.render('/admin/unlogined.html')


app = Flask(__name__, template_folder="./templates", static_folder='./templates/static')
api = Api(app)
app.secret_key = 'very hard secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:anton2142@localhost/sport_school"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
manager = LoginManager(app)
manager.login_view = 'login'
manager.login_message = 'Щоб потрапити на цю сторінку спочатку увійдіть в акаунт'
admin = Admin(app, 'Спортивна школа', template_mode='bootstrap4',
              index_view=MainPage(name='Головна', url='/admin', endpoint='/admin/'))
parser = reqparse.RequestParser()

from .database import models
from . import routes

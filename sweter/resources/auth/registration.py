from datetime import datetime
from random import randint

from cerberus import Validator
from dateutil.relativedelta import relativedelta
from werkzeug.security import generate_password_hash
from flask import make_response, render_template, flash, redirect, url_for
from flask_restful import Resource

from schemas.utils.errors_list import errors_list
from schemas.utils.error_handler import CustomErrorHandler
from sweter.schemas.register_schema import SCHEMA
from sweter.database.models import User, Team, Player
from sweter import parser, db

parser.add_argument('login', location='form')
parser.add_argument('password', location='form')
parser.add_argument('password2', location='form')

parser.add_argument('fname', location='form')
parser.add_argument('lname', location='form')
parser.add_argument('patronymic', location='form')
parser.add_argument('position', location='form')
parser.add_argument('weight', location='form')
parser.add_argument('height', location='form')
parser.add_argument('health', location='form')
parser.add_argument('born_date', location='form')
parser.add_argument('date_in_contract', location='form')
parser.add_argument('gender', location='form')


class Registration(Resource):
    """ This class is responsible for handling requests for the Registration page. """
    def get(self):
        return make_response(render_template('auth/registration.html'))

    def post(self):
        validator = Validator(SCHEMA, error_handler=CustomErrorHandler)
        validator.allow_unknown = True

        data = parser.parse_args()

        if validator.validate(data):

            login = data['login']
            password = data['password']
            password2 = data['password2']
            fname = data['fname']
            lname = data['lname']
            patronymic = data['patronymic']
            position = data['position']
            weight = data['weight']
            height = data['height']
            health = data['health']
            born_date = data['born_date']
            date_in_contract = data['date_in_contract']
            gender = data['gender']

            if User.query.filter_by(acc_login=login).all():
                flash("?????????? ???????????????????? ?????? ????????????????????????????")
                return make_response(redirect(url_for("login")))
            else:
                if password != password2:
                    flash("?????????????? ?????????? ????????????")
                    return make_response(redirect(url_for('registration')))
                else:
                    if User.query.filter_by(acc_fname=fname)\
                            .filter_by(acc_lname=lname)\
                            .filter_by(acc_patronymic=patronymic).\
                            filter_by(acc_born_date=born_date).first():
                        flash("?????????????? ?? ???????????? ???????????? ?????? ?????????? ?? ????????")
                        return make_response(redirect(url_for('login')))
                    else:
                        teams = Team.query.all()
                        id_of_team = randint(1, len(teams))

                        date_in_contract = datetime.strptime(date_in_contract, '%Y-%m-%d')
                        date_out_contract = date_in_contract + relativedelta(years=5)

                        hash_password = generate_password_hash(password)

                        user = User(acc_login=login, acc_password=hash_password, acc_status='0',
                                    acc_fname=fname, acc_lname=lname, acc_patronymic=patronymic,
                                    acc_born_date=born_date, acc_date_in_contract=date_in_contract,
                                    acc_date_out_contract=date_out_contract, acc_gender=gender,
                                    id_of_team=id_of_team, acc_win_games=0, acc_odd_games=0,
                                    acc_lose_games=0, name_of_photo="photoPeople1.png")

                        db.session.add(user)
                        db.session.commit()

                        user_id = User.query.filter_by(acc_login=login).first().acc_id

                        player = Player(player_position=position, player_height=height,
                                        player_weight=weight, player_health=health,
                                        player_goals=0, player_assist=0, player_acc=user_id)

                        db.session.add(player)
                        db.session.commit()

                        return make_response(redirect(url_for('login')))
        else:
            errors = errors_list(validator.errors)
            return make_response(render_template('auth/registration.html', errors=errors))

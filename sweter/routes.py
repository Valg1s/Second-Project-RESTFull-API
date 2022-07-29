from datetime import datetime
from random import randint

import calendar
import pymorphy2
import werkzeug.datastructures
from babel.dates import format_datetime

from dateutil.relativedelta import relativedelta
from flask_admin.contrib.sqla import ModelView
from flask_restful import Resource, reqparse
from flask import render_template, make_response, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import extract
from werkzeug.security import check_password_hash, generate_password_hash
from PIL import Image

from sweter import api, db, admin
from sweter.models import Request, User, Team, Player, Coach, Training

parser = reqparse.RequestParser()
parser.add_argument('contacts_name', location='form')
parser.add_argument('contacts_email', location='form')
parser.add_argument('contacts_phone', location='form')
parser.add_argument('contacts_question', location='form')

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

parser.add_argument('photo', type=werkzeug.datastructures.FileStorage, location='files')

parser.add_argument('month', location='args')
parser.add_argument('page', location='args')


def get_user_id():
    try:
        id_of_user = current_user.get_id()
    except AttributeError:
        id_of_user = None
    return id_of_user


class MyModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            id_of_user = get_user_id()

            user_status = User.query.filter_by(acc_id=id_of_user).first().acc_status

            return user_status == "1"
        else:
            return False

admin.add_view(MyModelView(User, db.session, name="Користувач"))
admin.add_view(MyModelView(Player, db.session, name="Гравець"))
admin.add_view(MyModelView(Coach, db.session, name="Тренер"))
admin.add_view(MyModelView(Team, db.session, name="Команда"))
admin.add_view(MyModelView(Training, db.session, name="Тренування"))


class Index(Resource):
    def get(self):
        coaches = User.query.filter_by(acc_status="1").all()
        return make_response(render_template('home.html', coaches=coaches, id_of_user=get_user_id()))


class About(Resource):
    def get(self):
        coaches = (db.session.query(Coach, User, Team)
                   .join(User, Coach.coach_acc == User.acc_id)
                   .join(Team, User.id_of_team == Team.team_id).all())

        return make_response(render_template('about.html', coaches=coaches, id_of_user=get_user_id()))


class Services(Resource):
    def get(self):
        return make_response(render_template('services.html', id_of_user=get_user_id()))


class Contact(Resource):
    def get(self):
        return make_response(render_template('contacts.html', id_of_user=get_user_id()))

    def post(self):
        data = parser.parse_args()

        full_name = data['contacts_name']
        email = data['contacts_email']
        phone = data['contacts_phone']
        question = data['contacts_question']

        if not full_name or not email or not phone or not question:
            flash("Заповніть усі поля")
        else:
            phone = phone.replace('+', '')
            date = datetime.now()

            request = Request(request_full_name=full_name, request_email=email, request_phone=phone,
                              request_question=question, request_date=date)

            db.session.add(request)
            db.session.commit()

            flash("Ваша заявка успішно передана в обробку")

        return make_response(render_template('contacts.html', id_of_user=get_user_id()))


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


class Registration(Resource):
    def get(self):
        return make_response(render_template('registration.html'))

    def post(self):
        data = parser.parse_args()

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

        if not login or not password or not password2 or not fname or not lname or not patronymic or not position or not weight or not height or not health or not born_date or not date_in_contract or not gender:
            flash("Заповніть усі поля")
            return make_response(render_template("registration.html"))
        else:
            if User.query.filter_by(acc_login=login).all():
                flash("Даний користувач вже зареєстрований")
                return make_response(redirect(url_for("login")))
            else:
                if password != password2:
                    flash("Введено різні паролі")
                    return make_response(redirect(url_for('registration')))
                else:
                    if User.query.filter_by(acc_fname=fname).filter_by(acc_lname=lname).filter_by(
                            acc_patronymic=patronymic).filter_by(acc_born_date=born_date).first():
                        flash("Гравець з такими даними вже існує в базі")
                        return make_response(redirect(url_for('login')))
                    else:
                        teams = Team.query.all()
                        id_of_team = randint(1, len(teams))

                        date_in_contract = datetime.strptime(date_in_contract, '%Y-%m-%d')
                        date_out_contract = date_in_contract + relativedelta(years=5)

                        hash_password = generate_password_hash(password)

                        user = User(acc_login=login, acc_password=hash_password, acc_status='0', acc_fname=fname,
                                    acc_lname=lname, acc_patronymic=patronymic, acc_born_date=born_date,
                                    acc_date_in_contract=date_in_contract, acc_date_out_contract=date_out_contract,
                                    acc_gender=gender, id_of_team=id_of_team, acc_win_games=0, acc_odd_games=0,
                                    acc_lose_games=0, name_of_photo="photoPeople1.png")

                        db.session.add(user)
                        db.session.commit()

                        user_id = User.query.filter_by(acc_login=login).first().acc_id

                        player = Player(player_position=position, player_height=height, player_weight=weight,
                                        player_health=health, player_goals=0, player_assist=0, player_acc=user_id)

                        db.session.add(player)
                        db.session.commit()

                        return make_response(redirect(url_for('login')))


class Logout(Resource):
    def get(self):
        logout_user()
        return make_response(redirect(url_for('index')))


class Account(Resource):
    @login_required
    def get(self):
        id_of_user = get_user_id()
        user_status = User.query.filter_by(acc_id=id_of_user).first().acc_status

        if user_status == '0':
            user = (db.session.query(User, Player, Team)
                    .join(Player, User.acc_id == Player.player_acc)
                    .join(Team, User.id_of_team == Team.team_id)).filter(User.acc_id == id_of_user) \
                .first()
        else:
            user = (db.session.query(User, Coach, Team)
                    .join(Coach, User.acc_id == Coach.coach_acc)
                    .join(Team, User.id_of_team == Team.team_id)).filter(User.acc_id == id_of_user) \
                .first()

        all_games = user[0].acc_win_games + user[0].acc_odd_games + user[0].acc_lose_games

        try:
            user_win_rate = user[0].acc_win_games // all_games
        except ZeroDivisionError:
            user_win_rate = 0

        return make_response(
            render_template("account.html", user=user, user_status=user_status, user_win_rate=user_win_rate,
                            all_games=all_games, id_of_user=id_of_user))

    def post(self):
        id_of_user = current_user.get_id()

        photo = parser.parse_args()['photo']
        print(type(photo))

        if not photo:
            flash('Внесіть фото')
            return make_response(redirect(url_for('account')))
        else:
            user = User.query.filter_by(acc_id=id_of_user).first()
            name_of_picture = f"{user.acc_lname}{user.acc_fname}{user.acc_patronymic}.png"

            with Image.open(photo) as img:
                print(img)
                img.save(f"./sweter/templates/static/images/{name_of_picture}", "PNG")

            user.name_of_photo = name_of_picture

            db.session.commit()

            return make_response(redirect(url_for('account')))


class Players(Resource):
    def get(self):
        id_of_user = current_user.get_id()
        user_team = User.query.filter_by(acc_id=id_of_user).first().id_of_team

        team_name = Team.query.filter_by(team_id=user_team).first().team_name
        players_of_team = (db.session.query(User, Player).join(Player, User.acc_id == Player.player_acc).filter(
            User.id_of_team == user_team))

        page = parser.parse_args()['page']

        if page and page.isdigit():
            page = int(page)
        else:
            page = 1

        pages = players_of_team.paginate(page=page, per_page=5)

        return make_response(
            render_template('players.html', id_of_user=id_of_user, team_name=team_name, pages=pages))


class Coaches(Resource):
    def get(self):
        coaches = (db.session.query(User, Coach, Team).join(Coach, User.acc_id == Coach.coach_acc).join(Team,
                                                                                                        User.id_of_team == Team.team_id))

        page = parser.parse_args()['page']

        if page and page.isdigit():
            page = int(page)
        else:
            page = 1

        pages = coaches.paginate(page=page, per_page=5)

        return make_response(render_template('coaches.html', id_of_user=get_user_id(), pages=pages))


class Calendar(Resource):
    def get(self):
        id_of_user = get_user_id()

        try:
            month_ = int(parser.parse_args()['month'])
        except TypeError:
            month_ = 0

        team_of_user = User.query.filter_by(acc_id=id_of_user).first().id_of_team

        date = datetime.today()

        if month_ == 0:

            morph = pymorphy2.MorphAnalyzer()
            name = format_datetime(date, "MMMM", locale='uk_UA')

            name_of_month = morph.parse(name)[0].normal_form.capitalize()
            number_of_month = int(datetime.today().strftime('%m'))

            current_year = datetime.now().year

            days = calendar.monthrange(current_year, number_of_month)[1]



        else:
            morph = pymorphy2.MorphAnalyzer()

            if month_ < 1:
                date -= relativedelta(months=-month_)
            else:
                date += relativedelta(months=month_)

            name = format_datetime(date, "MMMM", locale='uk_UA')

            name_of_month = morph.parse(name)[0].normal_form.capitalize()
            number_of_month = int(date.strftime('%m'))

            current_year = date.year

            days = calendar.monthrange(current_year, number_of_month)[1]

        trainings_ind = Training.query.filter_by(id_player=id_of_user).filter(
            extract('year', Training.training_date) == date.year).filter(
            extract('month', Training.training_date) == date.month).all()
        trainings_team = Training.query.filter_by(id_team=team_of_user).filter(
            extract('year', Training.training_date) == date.year).filter(
            extract('month', Training.training_date) == date.month).all()

        trainings = trainings_ind + trainings_team

        print(trainings)

        calend = {}

        for day in range(1, days + 1):
            calend[day] = None

        for training in trainings:
            if int(training.training_date.strftime('%m')) == number_of_month and int(
                    training.training_date.strftime('%Y')) == current_year:
                calend[int(training.training_date.strftime('%d'))] = training

        return make_response(
            render_template("calendar.html", id_of_user=get_user_id(), name_of_month=name_of_month, calend=calend,
                            month=month_,number_of_month=number_of_month, current_year=current_year))


api.add_resource(Index, "/", "/main")
api.add_resource(About, "/about")
api.add_resource(Services, "/services")
api.add_resource(Contact, '/contacts')
api.add_resource(Login, '/login')
api.add_resource(Registration, "/registration")
api.add_resource(Logout, "/logout")
api.add_resource(Account, "/account")
api.add_resource(Players, '/players')
api.add_resource(Coaches, '/coaches')
api.add_resource(Calendar, '/calendar')

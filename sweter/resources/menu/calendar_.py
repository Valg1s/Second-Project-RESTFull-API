import calendar
from datetime import datetime

import pymorphy2
from babel.dates import format_datetime
from dateutil.relativedelta import relativedelta
from flask import make_response, render_template
from flask_login import current_user
from flask_restful import Resource
from sqlalchemy import extract

from sweter.database.models import User, Training
from sweter import parser

parser.add_argument('month', location='args')


class Calendar(Resource):
    """ This class is responsible for handling requests for the Registration page. """
    def get(self):
        id_of_user = current_user.get_id()

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

        calend = {}

        for day in range(1, days + 1):
            calend[day] = None

        for training in trainings:
            if int(training.training_date.strftime('%m')) == number_of_month and \
               int(training.training_date.strftime('%Y')) == current_year:
                calend[int(training.training_date.strftime('%d'))] = training

        return make_response(
            render_template("calendar.html", name_of_month=name_of_month, calend=calend,
                            month=month_, number_of_month=number_of_month, current_year=current_year))

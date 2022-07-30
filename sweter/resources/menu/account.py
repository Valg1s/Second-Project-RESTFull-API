import werkzeug.datastructures
from PIL import Image
from flask import make_response, render_template, flash, url_for, redirect
from flask_login import current_user
from flask_restful import Resource

from sweter import db, parser

from sweter.database.models import User, Player, Team, Coach

parser.add_argument('photo', type=werkzeug.datastructures.FileStorage, location='files')


class Account(Resource):
    def get(self):
        id_of_user = current_user.get_id()
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
                            all_games=all_games))

    def post(self):
        id_of_user = current_user.get_id()

        photo = parser.parse_args()['photo']

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

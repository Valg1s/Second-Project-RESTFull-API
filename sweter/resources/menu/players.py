from flask import make_response, render_template
from flask_login import current_user
from flask_restful import Resource

from sweter.database.models import User, Team, Player
from sweter import db, parser

parser.add_argument('page', location='args')


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

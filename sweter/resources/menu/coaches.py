from flask import make_response, render_template
from flask_restful import Resource

from sweter.database.models import User, Coach, Team
from sweter import db, parser

parser.add_argument('page', location='args')


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

        return make_response(render_template('coaches.html', pages=pages))

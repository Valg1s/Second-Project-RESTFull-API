from flask import make_response, render_template
from flask_restful import Resource

from sweter.database.models import Coach, User, Team
from sweter import db


class About(Resource):
    """ This class is responsible for handling requests for the About page. """
    def get(self):
        coaches = (db.session.query(Coach, User, Team)
                   .join(User, Coach.coach_acc == User.acc_id)
                   .join(Team, User.id_of_team == Team.team_id).all())

        return make_response(render_template('about.html', coaches=coaches))

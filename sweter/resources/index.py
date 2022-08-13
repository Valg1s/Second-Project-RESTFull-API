from flask import make_response, render_template
from flask_restful import Resource

from sweter.database.models import User


class Index(Resource):
    """ This class is responsible for handling requests for the Index page. """
    def get(self):
        coaches = User.query.filter_by(acc_status="1").all()
        return make_response(render_template('home.html', coaches=coaches))

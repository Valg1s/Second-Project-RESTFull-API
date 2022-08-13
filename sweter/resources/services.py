from flask import make_response, render_template
from flask_restful import Resource


class Services(Resource):
    """ This class is responsible for handling requests for the Services page. """
    def get(self):
        return make_response(render_template('services.html'))

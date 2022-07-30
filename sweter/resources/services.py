from flask import make_response, render_template
from flask_restful import Resource


class Services(Resource):
    def get(self):
        return make_response(render_template('services.html'))
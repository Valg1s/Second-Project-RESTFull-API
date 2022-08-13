from datetime import datetime

from cerberus import Validator
from flask import make_response, render_template, flash
from flask_restful import Resource

from sweter.schemas.contact_schema import SCHEMA
from sweter.schemas.utils.error_handler import CustomErrorHandler
from sweter.schemas.utils.errors_list import errors_list
from sweter.database.models import Request
from sweter import db, parser


class Contact(Resource):
    """ This class is responsible for handling requests for the Contact page. """
    def get(self):
        return make_response(render_template('contacts.html'))

    def post(self):
        v = Validator(SCHEMA, error_handler=CustomErrorHandler)
        v.allow_unknown = True

        data = parser.parse_args()

        if v.validate(data):
            full_name = data['contacts_name']
            email = data['contacts_email']
            phone = data['contacts_phone']
            question = data['contacts_question']

            phone = phone.replace('+', '')
            date = datetime.now()

            request = Request(request_full_name=full_name, request_email=email, request_phone=phone,
                              request_question=question, request_date=date)

            db.session.add(request)
            db.session.commit()

            flash("Ваша заявка успішно передана в обробку")

        else:
            errors = errors_list(v.errors)
            return make_response(render_template('contacts.html', errors=errors))
        return make_response(render_template('contacts.html'))

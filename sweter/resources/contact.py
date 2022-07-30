from datetime import datetime

from flask import make_response, render_template, flash
from flask_restful import Resource

from sweter.database.models import Request
from sweter import parser, db

parser.add_argument('contacts_name', location='form')
parser.add_argument('contacts_email', location='form')
parser.add_argument('contacts_phone', location='form')
parser.add_argument('contacts_question', location='form')

class Contact(Resource):
    def get(self):
        return make_response(render_template('contacts.html'))

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

        return make_response(render_template('contacts.html'))
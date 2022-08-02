from datetime import datetime

from flask import make_response, render_template, flash
from flask_restful import Resource

from sweter.database.models import Request
from sweter import db

from sweter.forms.contacts_form import ContactsForm


class Contact(Resource):
    def __init__(self):
        self.form = ContactsForm()

    def get(self):
        return make_response(render_template('contacts.html', form=self.form))

    def post(self):
        request = Request(request_full_name=self.form.contacts_name.data,
                              request_email=self.form.contacts_email.data,
                              request_phone=self.form.contacts_phone.data,
                              request_question=self.form.contacts_question.data, request_date=datetime.now())

        db.session.add(request)
        db.session.commit()

        flash("Ваша заявка успішно передана в обробку")

        return make_response(render_template('contacts.html', form=self.form))

from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from database.models import User, Player, Coach, Team, Training
from sweter import admin, db


class MyModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            id_of_user = current_user.get_id()

            user_status = User.query.filter_by(acc_id=id_of_user).first().acc_status

            return user_status == "1"
        else:
            return False


admin.add_view(MyModelView(User, db.session, name="Користувач"))
admin.add_view(MyModelView(Player, db.session, name="Гравець"))
admin.add_view(MyModelView(Coach, db.session, name="Тренер"))
admin.add_view(MyModelView(Team, db.session, name="Команда"))
admin.add_view(MyModelView(Training, db.session, name="Тренування"))

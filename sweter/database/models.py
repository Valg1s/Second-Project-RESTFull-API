from sweter import db, manager
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'account'
    acc_id = db.Column(db.Integer(), primary_key=True)
    acc_login = db.Column(db.String(64), nullable=False)
    acc_password = db.Column(db.String(128), nullable=False)
    acc_status = db.Column(db.Enum('0', '1'), nullable=False, default='0')
    acc_fname = db.Column(db.String(32), nullable=False)
    acc_lname = db.Column(db.String(32), nullable=False)
    acc_patronymic = db.Column(db.String(32), nullable=False)
    acc_born_date = db.Column(db.DateTime(), nullable=True)
    acc_date_in_contract = db.Column(db.DateTime(), nullable=True)
    acc_date_out_contract = db.Column(db.DateTime(), nullable=True)
    acc_gender = db.Column(db.Enum('0', '1'), nullable=False)
    id_of_team = db.Column(db.Integer(), db.ForeignKey('team.team_id'))
    acc_win_games = db.Column(db.Integer(), nullable=False)
    acc_odd_games = db.Column(db.Integer(), nullable=False)
    acc_lose_games = db.Column(db.Integer(), nullable=False)
    name_of_photo = db.Column(db.String(128), nullable=False, default="photoPeople1.png")
    fk_player = db.relationship('Player')
    fk_coach = db.relationship('Coach')

    def get_id(self):
        return (self.acc_id)


class Team(db.Model):
    __tablename__ = "team"
    team_id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(32), nullable=False)
    fk_user = db.relationship('User')
    fk_training = db.relationship('Training')
    fk_game = db.relationship('Game')


class Coach(db.Model):
    __tablename__ = "coach"
    coach_id = db.Column(db.Integer(), primary_key=True)
    coach_experience = db.Column(db.Integer(), nullable=False)
    coach_info = db.Column(db.String(256), nullable=False)
    coach_education = db.Column(db.String(64), nullable=False)
    coach_acc = db.Column(db.Integer(), db.ForeignKey('account.acc_id'))


class Player(db.Model):
    __tablename__ = "player"
    player_id = db.Column(db.Integer(), primary_key=True)
    player_position = db.Column(db.String(4), nullable=False)
    player_height = db.Column(db.Integer(), nullable=False)
    player_weight = db.Column(db.Integer(), nullable=False)
    player_health = db.Column(db.String(64), nullable=False)
    player_goals = db.Column(db.Integer(), nullable=False)
    player_assist = db.Column(db.Integer(), nullable=False)
    player_acc = db.Column(db.Integer(), db.ForeignKey('account.acc_id'))
    fk_training = db.relationship('Training')


class Training(db.Model):
    __tablename__ = "training"
    training_id = db.Column(db.Integer(), primary_key=True)
    training_date = db.Column(db.DateTime(), nullable=False)
    training_place = db.Column(db.String(64), nullable=False)
    training_category = db.Column(db.Enum('0', '1', '2'), nullable=False)
    id_player = db.Column(db.Integer(), db.ForeignKey('player.player_id'))
    id_team = db.Column(db.Integer(), db.ForeignKey('team.team_id'))


class Game(db.Model):
    __tablename__ = "game"
    game_id = db.Column(db.Integer(), primary_key=True)
    game_date = db.Column(db.DateTime(), nullable=False)
    game_place = db.Column(db.String(64), nullable=False)
    game_category = db.Column(db.Enum('0', '1', '2'), nullable=False)
    id_team = db.Column(db.Integer(), db.ForeignKey('team.team_id'))


class Request(db.Model):
    __tablename__ = "request"
    request_id = db.Column(db.Integer(), primary_key=True)
    request_full_name = db.Column(db.String(128), nullable=False)
    request_email = db.Column(db.String(128), nullable=False)
    request_phone = db.Column(db.String(32), nullable=False)
    request_question = db.Column(db.String(2048), nullable=False)
    request_date = db.Column(db.DateTime(), nullable=False)


db.create_all()


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

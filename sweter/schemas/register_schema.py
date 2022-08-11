from schemas.utils.validators import name_validator, password_validator
from datetime import date
from dateutil.relativedelta import relativedelta

SCHEMA = {
    "login": {"type": "string", 'empty': False},
    "password": {"type": "string", 'empty': False, "check_with": password_validator},
    "password2": {"type": "string", 'empty': False, "check_with": password_validator},
    "fname": {"type": "string", 'empty': False, "check_with": name_validator},
    "lname": {"type": "string", 'empty': False, "check_with": name_validator},
    "patronymic": {"type": "string", 'empty': False, "check_with": name_validator},
    "position": {"type": "string", "min": 1, "max": 3, 'empty': False},
    "weight": {"type": "integer", "max": 150, 'empty': False},
    "height": {"type": "integer", "max": 220, 'empty': False},
    "health": {"type": "string", "min": 4, 'empty': False},
    "born_date": {"type": "date", "max": date.today() - relativedelta(years=5),
                  "min": date.today() - relativedelta(years=18), 'empty': False},
    "date_in_contract": {"type": "date", "max": date.today(), "min": date.today() - relativedelta(years=5),
                         'empty': False},
    "gender": {"type": "string", 'empty': False, "allowed": ["0", "1"]},
}

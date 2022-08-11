import phonenumbers
from email_validator import validate_email, EmailNotValidError

from password_strength import PasswordPolicy

police = PasswordPolicy.from_names(
    length=8,
    uppercase=1,
    numbers=1,
    special=1
)


def name_validator(field, value, error):
    if not value.isalpha():
        error(field, "Ім'я,прізвище чи ім'я по батькові може містити  лише букви")


def email_validator(field, value, error):
    try:
        validate_email(value).email
    except EmailNotValidError:
        error(field, "Ваша почта повинна відповідати шаблону name@services.com")


def phone_validator(field, value, error):
    try:
        number = phonenumbers.parse(value, "UA")
    except phonenumbers.NumberParseException:
        error(field, "Ваш номер повинен відповідати шаблону xxx xxx xx xx,де x це цифри")

    if not phonenumbers.is_valid_number(number):
        error(field, "Ваш номер повинен відповідати шаблону xxx xxx xx xx,де x це цифри")

def password_validator(field, value,error):
    if police.test(value):
        error(field, "Пароль мусить містити мінімум 8 символів,1 велику літеру , 1 число , 1 спец.символ")
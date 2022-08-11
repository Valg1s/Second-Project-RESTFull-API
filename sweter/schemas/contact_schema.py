from schemas.utils.validators import name_validator, email_validator, phone_validator

SCHEMA = {
    "contacts_name": {"type": "string", 'empty': False, "check_with": name_validator},
    "contacts_email": {"type": "string", 'empty': False, "check_with": email_validator},
    "contacts_phone": {"type": "string", 'empty': False, "check_with": phone_validator},
    "contacts_question": {"type": "string", 'empty': False, "maxlenght": 2048}
}

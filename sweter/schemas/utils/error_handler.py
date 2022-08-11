from cerberus import errors


class CustomErrorHandler(errors.BasicErrorHandler):
    messages = errors.BasicErrorHandler.messages.copy()
    messages[errors.EMPTY_NOT_ALLOWED.code] = "Усі поля повинні бути заповнені"

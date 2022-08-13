def errors_list(errors_dict: dict):
    result = []
    for key in errors_dict.keys():
        if not errors_dict[key] in result:
            result.append(errors_dict[key])
    return result

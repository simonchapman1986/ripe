

BLANK_UUID = '00000000-0000-0000-0000-000000000000'

def get(data, field_name, disallow=None, default=None):
    value = data.get(field_name, default)
    if disallow and value in disallow:
        return default
    return value

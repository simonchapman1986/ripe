from apps.base.models.dimensions.dimension_user import DimensionUser
from apps.base.models.dimensions.dimension_platform import DimensionPlatform
from apps.flags.report import register_flag
from apps.flags.report import MISSING_DATA

def save_user(data, territory, client, event='unknown'):
    res = DimensionUser.insert(
        external_user_id=data.get('external_user_id', None),
        internal_user_id=data.get('internal_user_id', None),
        territory=territory,
        client=client
    ) if any([
        data.get('external_user_id', None),
        data.get('internal_user_id', False),
        territory,
        client
    ]) else None

    if not res:
        register_flag(
            type=MISSING_DATA,
            event=event,
            description='No user information provided in event.'
        )
    return res



def save_platform(data, event='unknown'):
    res = DimensionPlatform.insert(
        os=data.get('platform_os', None),
        name=data.get('platform_name', None),
        version=data.get('platform_version', None)
    ) if any(
        [p in data for p in ['platform_os', 'platform_name', 'platform_version']]
    ) else None

    if not res:
        register_flag(
            type=MISSING_DATA,
            event=event,
            description='No platform information provided in event.'
        )
    return res


def exists(key, data):
    return key in data
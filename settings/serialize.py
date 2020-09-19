from typequery import GenericMethod

from api.models.user import User

serialize = GenericMethod('serialize')


@serialize.of(bool)
@serialize.of(type(None))
@serialize.of(int)
@serialize.of(float)
@serialize.of(str)
def serialize(value, **kwargs):
    return value


@serialize.of(User)
def serialize(user, **kwargs):
    result = {
        'id': user.id,
        'name': user.name
    }

    return result

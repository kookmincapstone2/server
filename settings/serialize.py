from typequery import GenericMethod

from api.models.room import Room, RoomMember
from api.models.user import User

serialize = GenericMethod('serialize')


@serialize.of(bool)
@serialize.of(type(None))
@serialize.of(int)
@serialize.of(float)
@serialize.of(str)
def serialize(value, **kwargs):
    return value


@serialize.of(list)
def serialize(input_list, **kwargs):
    class_name = input_list[0].__class__.__name__
    result_list = list()
    for i in input_list:
        result_list.append(serialize(i))

    result = {
        class_name: result_list
    }
    return result


@serialize.of(User)
def serialize(user, **kwargs):
    result = {
        'user_id': user.id,
        'name': user.name,
        'rank': user.rank,
    }

    return result


@serialize.of(Room)
def serialize(room, **kwargs):
    result = {
        'room_id': room.id,
        'master_id': room.master_id,
        'title': room.title,
        'maximum_population': room.maximum_population,
        'invite_code': room.invite_code,
    }

    return result


@serialize.of(RoomMember)
def serialize(room_member, **kwargs):
    result = {
        'room_id': serialize(room_member.room_id)
    }

    return result

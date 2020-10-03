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
        'id': user.id,
        'name': user.name
    }

    return result


@serialize.of(Room)
def serialize(room, **kwargs):
    result = {
        'id': room.id,
        'master_id': room.master_id,
        'title': room.title,
        'maximum_population': room.maximum_population,
    }

    return result


# @serialize(RoomMember)
# def serialize(room_member, **kwargs):
#     result = {
#         'member': serialize(room_member.member)
#     }
#
#     return result

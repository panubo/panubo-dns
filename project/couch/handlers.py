from .connections import connection
from .dns import Zone


connection = connection('dns')


def save_zone(obj, created):
    if obj.is_valid():
        _id = str(obj.domain_name)

        doc = Zone(connection=connection, _id=_id)
        doc.update(name=obj.domain_name,
                   serial=obj.serial,
                   data=obj.render())
        return doc.save()
    else:
        return False


def delete_zone(obj):
    _id = str(obj.domain_name)
    doc = Zone(connection=connection, _id=_id)
    return doc.delete()
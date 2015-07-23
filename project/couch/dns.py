from squab.base import BaseDocument


class Zone(BaseDocument):
    """ Zone Object """
    type = 'zone'

    def update(self, name, data, serial):
        super(Zone, self).update(
            serial=serial,
            data=data,
            _id=name)

    def parse(self):
        super(Zone, self).update(
            name=self['_id'],
            serial=self['serial'],
            data=self['data'],
            _id=self['_id'],
            _rev=self['_rev'])
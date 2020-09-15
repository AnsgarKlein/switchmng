from . import *

vlans_ports_mapping = Table('vlan_ports', Base.metadata,
    Column('port_id', Integer, ForeignKey('ports.id'), primary_key = True),
    Column('vlan_id', Integer, ForeignKey('vlans.id'), primary_key = True),
)

class Port(Base):
    __tablename__ = 'ports'
    _port_id = Column('id', Integer, primary_key = True, nullable = False)
    _switch_id = Column('switch_id', Integer, ForeignKey('switches.id'),
                       nullable = False)

    _name = Column('name', String, nullable = False)
    _vlans = relationship('Vlan', secondary = vlans_ports_mapping, uselist = True)

    def __init__(self, name = None, vlans = []):
        self.name = name
        self.vlans = vlans

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        Port.check_params(name = name)
        self._name = name

    @property
    def vlans(self):
        return self._vlans

    @vlans.setter
    def vlans(self, vlans):
        Port.check_params(vlans = vlans)
        self._vlans = vlans

    def jsonify(self):
        return { 'name': self.name,
                 'vlans': [ int(str(v)) for v in self.vlans ] }

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def check_params(**kwargs):
        for key, val in kwargs.items():
            if key == 'name':
                if not isinstance(val, str):
                    raise TypeError('Name of vlan has to be of type str')
                if len(val) < 1:
                    raise ValueError('Length of name of vlan cannot be zero')
                continue

            if key == 'vlans':
                if not isinstance(val, list):
                    raise TypeError('List of vlans for port has to be of type list')
                for vlan in val:
                    if not isinstance(vlan, Vlan):
                        raise TypeError('Vlan in list of vlans for port has to be of type Vlan')
                continue

            raise TypeError("Unexpected attribute '{}' for port".format(key))

        return kwargs


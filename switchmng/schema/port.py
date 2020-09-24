from . import *

vlans_ports_mapping = Table(
    'vlan_ports',
    Base.metadata,
    Column(
        'port_id',
        Integer,
        ForeignKey('ports.id'),
        primary_key = True),
    Column(
        'vlan_id',
        Integer,
        ForeignKey('vlans.id'),
        primary_key = True),
)

class Port(Base):
    """
    Represents a port of a switch.

    That is a concrete port of a concrete switch.

    :param name: The identifier of this port. Must be unique for the
        containing :class:`Switch`.
    :type name: str

    :param vlans: A list of vlans that are active on this port
    :type vlans: list

    """

    __tablename__ = 'ports'

    # Database id
    _port_id = Column('id', Integer, primary_key = True, nullable = False)
    _switch_id = Column('switch_id', Integer, ForeignKey('switches.id'),
                       nullable = False)

    # Resource state
    _name = Column('name', String, nullable = False)
    _vlans = relationship('Vlan', secondary = vlans_ports_mapping, uselist = True)
    _target = Column('target', String, nullable = True)

    def __init__(self, name = None, vlans = [], target = None):
        self.name = name
        self.vlans = vlans
        self.target = target

    @property
    def name(self):
        """The identifier of this port. Must be unique for the containing
        :class:`Switch`."""
        return self._name

    @name.setter
    def name(self, name):
        Port.check_params(name = name)
        self._name = name

    @property
    def vlans(self):
        """A list of vlans that are active on this port"""
        return self._vlans

    @vlans.setter
    def vlans(self, vlans):
        Port.check_params(vlans = vlans)
        self._vlans = vlans

    @property
    def target(self):
        """Device that is connected to this port

        Some representation (FQDN / description / ip) of the device that is
        connected to this port.
        """

        return self._target

    @target.setter
    def target(self, target):
        Port.check_params(target = target)
        self._target = target

    def jsonify(self):
        """
        Represent this object as a json-ready dict.

        That is a dict which completely consists of json-compatible structures
        like:

        * dict
        * list
        * string
        * int
        * bool
        * None / null
        """

        return { 'name': self.name,
                 'vlans': [ int(str(v)) for v in self.vlans ],
                 'target': self.target }

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def check_params(**kwargs):
        """
        Check all given parameters.

        Check if all given parameters have the correct type and are valid
        parameters for a object of this class at all as well as other
        basic checks.

        This function gets executed when trying to assign values to object
        variables but can be called when needing to check multiple parameters
        at once in order to prevent half changed states.

        :raises TypeError: When type of given parameter does not match
            expectation
        :raises ValueError: When value of given parameter does not match
            expectation
        """

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

            if key == 'target':
                if val is None:
                    continue
                if not isinstance(val, str):
                    raise TypeError('Target of port has to be of type str')
                if len(val) < 1:
                    raise ValueError('Target of port cannot be empty')
                continue

            raise TypeError("Unexpected attribute '{}' for port".format(key))

        return kwargs

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

    def __init__(self, name, vlans = []):
        self.name = name
        self.vlans = vlans

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if type(name) is not str:
            raise TypeError('Expected name of port to be of type string')
        if len(name) < 1:
            raise ValueError('Length of port name cannot be zero')
        self._name = name

    @property
    def vlans(self):
        return self._vlans

    @vlans.setter
    def vlans(self, vlans):
        if type(vlans) is not list:
            raise TypeError('Expected vlans of port to be a list')
        self._vlans = vlans

    def jsonify(self):
        return { 'name': self.name,
                 'vlans': [ str(v) for v in self.vlans ] }

class Switch(Base):
    """
    Represents a switch resource.

    This resource is uniquely identified by its name.
    All contained id fields are private and only used for storing object in
    database.

    Attributes
    ----------

    name : str
        Name uniquely identifying this switch
    model : SwitchModel
        Model of this switch
    ports : list
        Ports associated with this switch
    location : int
        Location of this switch in server rack
    """

    __tablename__ = 'switches'

    # Database ids
    _switch_id = Column('id', Integer, primary_key = True, nullable = False)
    _model_id = Column('model_id', Integer, ForeignKey('switch_models.id'),
                      nullable = False)

    # Resource identifier
    _name = Column('name', String, nullable = False, unique = True)

    # Resource state
    _model = relationship('SwitchModel', uselist = False)
    _ports = relationship('Port', uselist = True, cascade = 'all, delete-orphan')
    _location = Column('location', Integer, nullable = True)

    def __init__(self, name, model, ports = None, location = None):
        # Assign name from argument
        if type(name) is not str:
            raise TypeError('Expected name of switch to be of type str')
        self.name = name

        # Assign model from argument
        if type(model) is not SwitchModel:
            raise TypeError('Expected switch model of switch to be of type SwitchModel')
        self.model = model

        # Adopt ports from switch model and then assign
        if ports is not None:
            self.ports = ports

        # Assign location from argument
        if location is not None:
            self.location = location

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if type(name) is not str:
            raise TypeError('Expected name of switch to be of type string')
        if len(name) < 1:
            raise ValueError('Length of switch name cannot be zero')
        self._name = name

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model):
        if type(model) is not SwitchModel:
            raise TypeError('Expected model of switch to be of type SwitchModel')
        self._model = model

        # If switch model changed we need to update all
        # ports of this switch to reflect ports from model.
        self._refresh_ports()

    @property
    def ports(self):
        return [ p.jsonify() for p in self._ports ]

    @ports.setter
    def ports(self, port_configs):
        # Check all parameters first without making any changes
        if type(port_configs) is not list:
            raise TypeError('Expected maps from ports to vlans to be of type list')
        for port_config in port_configs:
            if type(port_config) is not dict:
                raise TypeError('Expected map from ports to vlans to be of type dict')
            if 'name' not in port_config or 'vlans' not in port_config:
                raise KeyError('Given map from port to vlan does not contain required keys')

            # Check if port of port map exists
            if self._port_obj(port_config['name']) is None:
                raise ValueError('Port of given map from port to vlan does not exist on this switch')

            # Check if all vlans of port map exist
            for v in port_config['vlans']:
                if type(v) is not Vlan:
                    raise TypeError('Given map from port to vlan contains invalid vlan')

        # Adjust ports
        for port_config in port_configs:
            self._port_obj(port_config['name']).vlans = port_config['vlans']

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location):
        if type(location) is not int:
            raise TypeError('Expected location of switch to be of type int')
        self._location = location

    def _refresh_ports(self):
        # Remove ports that do not exist in switch model
        nports1 = [ p
                    for p in self._ports
                    if self.model._port_obj(p.name) is not None ]

        # Add all ports from switch model
        nports2 = [ Port(name = p.name)
                    for p in self.model._ports
                    if self._port_obj(p.name) is None ]

        self._ports = nports1 + nports2

    def _port_obj(self, port_name):
        if type(port_name) is not str:
            return None

        # Search for port with specified name
        for port in self._ports:
            if port.name == port_name:
                return port

        # Did not find port for given port name
        return None

    def jsonify(self):
        return { 'name': self.name,
                 'location': self.location,
                 'model': str(self.model),
                 'ports': self.ports }

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


from sqlalchemy import Integer, String
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

vlans_ports_mapping = Table('vlan_ports', Base.metadata,
    Column('port_id', Integer, ForeignKey('ports.id'), primary_key = True),
    Column('vlan_id', Integer, ForeignKey('vlans.id'), primary_key = True),
)

class Vlan(Base):
    """
    Represents a VLAN resource consisting of description and VLAN tag id.

    Attributes
    ----------

    tag : int
        Tag uniquely identifying this VLAN
    description : str
        Description of this VLAN
    """

    __tablename__ = 'vlans'

    # Database id
    _vlan_id = Column('id', Integer, primary_key = True, nullable = False)

    # Resource identifier
    tag = Column('tag', Integer, nullable = False, unique = True)

    # Resource state
    description = Column('name', String, nullable = False)

    def __init__(self, tag = None, description = None):
        if type(tag) is not int:
            raise TypeError('Expected vlan id to be of type int')
        else:
            self.tag = tag

        if type(description) is not str:
            raise TypeError('Expected vlan description to be of type string')
        else:
            self.description = description

    def jsonify(self):
        return { 'tag': str(self.tag),
                 'description': self.description }

    def __str__(self):
        return str(self.tag)

    def __repr__(self):
        return self.__str__()

class SwitchModel(Base):
    """
    Represents a switch model resource.

    This resource is uniquely identified by its name.
    All contained id fields are private and only used for storing object in
    database.

    Attributes
    ----------

    name : str
        Name uniquely identifying this switch model
    size : int
        Size (number of rack units) this switch takes up in server rack
    ports : list
        Ports associated with this switch model
    """

    class PortModel(Base):
        __tablename__ = 'port_models'

        # Database id
        _port_model_id = Column('id', Integer, primary_key = True, nullable = False)
        _switch_model_id = Column('switch_model_id', Integer,
                                 ForeignKey('switch_models.id'), nullable = False)
        port_type_id = Column('port_type_id', Integer,
                              ForeignKey('port_types.description'), nullable = True)

        # Attributes
        _name = Column('name', String, nullable = False)
        _port_type = relationship('PortType', uselist = False)

        def __init__(self, name, port_type = None):
            self.name = name

            if port_type is not None:
                self.port_type = port_type

        @property
        def name(self):
            return self._name

        @name.setter
        def name(self, name):
            if type(name) is not str:
                raise TypeError('Expected name of port model to be of type string')
            if len(name) < 1:
                raise ValueError('Length of port name cannot be zero')
            self._name = name

        @property
        def port_type(self):
            return self._port_type

        @port_type.setter
        def port_type(self, port_type):
            if type(port_type) is not PortType:
                raise TypeError('Expected port type of port model to be of type PortType')
            self._port_type = port_type

        def jsonify(self):
            return { 'name': self.name,
                     'port_type': str(self.port_type) }


    __tablename__ = 'switch_models'

    # Database id
    _switch_model_id = Column('id', Integer, primary_key = True, nullable = False)

    # Resource identifier
    _name = Column('name', String, nullable = False, unique = True)

    # Resource state
    _ports = relationship('PortModel', uselist = True)
    _size = Column('size', Integer, nullable = True)

    def __init__(self, name, ports, size = None):
        self.name = name

        # Assign ports from argument
        self.ports = ports

        # Assign size from argument
        if size is not None:
            self.size = size

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if type(name) is not str:
            raise TypeError('Expected name of switch model to be of type string')
        if len(name) < 1:
            raise ValueError('Length of switch model name cannot be zero')

        self._name = name

    @property
    def ports(self):
        return [ p.jsonify() for p in self._ports ]

    @ports.setter
    def ports(self, ports):
        if type(ports) is not list:
            raise TypeError('Expected ports of switch model to be of type list')

        port_list = []

        for port in ports:
            if type(port) is not dict:
                raise TypeError('Expected port of switch model to be of type dict')
            if 'name' not in port:
                raise KeyError('Given port of switch model does not contain key "name"')
            if 'port_type' not in port:
                raise KeyError('Given port of switch model does not contain key "port_type"')

            port_name = port['name']
            port_type = port['port_type']

            if type(port_name) is not str:
                raise TypeError('Given name of port of switch model is not of type str')
            if type(port_type) is not PortType:
                raise TypeError('Given port type of switch model is not of type PortType')

            port_list.append(self.PortModel(name = port_name, port_type = port_type))

        self._ports = port_list

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        if type(size) is not int:
            raise TypeError('Expected size of switch model to be of type int')
        if size < 1:
            raise ValueError('Size of switch model cannot be less than 1')
        self._size = size

    def modify_port(self, port, name = None, port_type = None):
        port = self.port(port)
        if port is None:
            return False

        if name is not None:
            port.name = name

        if port_type is not None:
            port.port_type = port_type

        return True

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
                 #'ports': [ p.jsonify() for p in self.ports ],
                 'ports': self.ports,
                 'size': self.size }

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

class PortType(Base):
    """
    Represents a port type resource.

    This resource is uniquely identified by its description.
    All contained id fields are private and only used for storing object in
    database.

    Attributes
    ----------

    description : str
        Name uniquely identifying this port type
    speed : int
        Speed of this port type in Mb/s
    """

    __tablename__ = 'port_types'

    # Database id
    _port_type_id = Column('id', Integer, primary_key = True, nullable = False)

    # Resource identifier
    description = Column('description', String, nullable = False, unique = True)

    # Resource state
    speed = Column('speed', Integer, nullable = False)

    def __init__(self, description, speed):
        if type(description) is not str:
            raise TypeError('Expected description of port type to be of type string')
        else:
            self.description = description

        if type(speed) is not int:
            raise TypeError('Expected speed of port type to be of type int')
        else:
            self.speed = speed

    def jsonify(self):
        return { 'description': self.description,
                 'speed': self.speed }

    def __str__(self):
        return self.description

    def __repr__(self):
        return self.__str__()

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

    class Port(Base):
        __tablename__ = 'ports'
        _port_id = Column('id', Integer, primary_key = True, nullable = False)
        _switch_id = Column('switch_id', Integer, ForeignKey('switches.id'),
                           nullable = True)

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

    __tablename__ = 'switches'

    # Database ids
    _switch_id = Column('id', Integer, primary_key = True, nullable = False)
    _model_id = Column('model_id', Integer, ForeignKey('switch_models.id'),
                      nullable = False)

    # Resource identifier
    _name = Column('name', String, nullable = False, unique = True)

    # Resource state
    _model = relationship('SwitchModel', uselist = False)
    _ports = relationship('Port', uselist = True)
    _location = Column('location', Integer, nullable = True)

    def __init__(self, name, model, port_maps = None, location = None):
        # Assign name from argument
        self.name = name

        # Assign model from argument
        self.model = model

        # Adopt ports from switch model and then assign
        if port_maps is not None:
            self.ports = port_maps

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
        nports2 = [ self.Port(name = p.name)
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
                 'model': self.model.name,
                 'ports': self.ports }

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


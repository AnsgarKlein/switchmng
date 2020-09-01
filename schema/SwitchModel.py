from . import *

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

    __tablename__ = 'switch_models'

    # Database id
    _switch_model_id = Column('id', Integer, primary_key = True, nullable = False)

    # Resource identifier
    _name = Column('name', String, nullable = False, unique = True)

    # Resource state
    _ports = relationship('PortModel', uselist = True, cascade = 'all, delete-orphan')
    _size = Column('size', Integer, nullable = True)

    def __init__(self, name, ports, size = None):
        # Assign name from argument
        if type(name) is not str:
            raise TypeError('Expected name of switch model to be of type str')
        self.name = name

        # Assign ports from argument
        self.ports = ports

        # Assign size from argument
        if size is not None:
            if type(size) is not int:
                raise TypeError('Expected size of switch model to be of type int')
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

            port_list.append(PortModel(name = port_name, port_type = port_type))

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
                 'ports': self.ports,
                 'size': self.size }

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


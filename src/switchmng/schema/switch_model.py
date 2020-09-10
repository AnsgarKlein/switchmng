from . import *

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

    # Helper relationship to ensure that all switches that have
    # this as a switch model get deleted if this model gets deleted.
    _switches = relationship('Switch', uselist = True, cascade = 'all, delete-orphan')

    def __init__(self, name = None, ports = [], size = None):
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
        SwitchModel.check_params(name = name)
        self._name = name

    @property
    def ports(self):
        # Convert sqlalchemy.orm.collections.InstrumentedList to default
        # python list
        l = [ p for p in self._ports ]

        # Sort list by name of port
        l.sort(key = lambda p: p.name)

        return l

    @ports.setter
    def ports(self, ports):
        """
        Set all ports of this switch model.
        All ports not given but present will be removed.
        """

        SwitchModel.check_params(ports = ports)
        self._ports = ports

        # If ports of this switch model change we need to update
        # the list of ports of all switches that use this switch model.
        for sw in self._switches:
            sw._sync_ports_from_model()

    def modify_ports(self, ports):
        """
        Change only given ports of this switch model.
        All ports not given but present will not be touched.
        """

        # Check ports
        SwitchModel.check_params(ports = ports)

        # Never add or delete any ports only apply changes.
        # Non specified ports will not get touched.
        for new_port in ports:
            for i, old_port in enumerate(self._ports):
                if old_port.name == new_port.name:
                    self._ports[i] = new_port
                    break

        # If ports of this switch model change we need to update
        # the list of ports of all switches that use this switch model.
        for sw in self._switches:
            sw._sync_ports_from_model()

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        SwitchModel.check_params(size = size)
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

    def _port_by_name(self, port_name):
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
                 'ports': [ p.jsonify() for p in self.ports ],
                 'size': self.size }

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def check_params(**kwargs):
        for key, val in kwargs.items():
            if key == 'name':
                if type(val) is not str:
                    raise TypeError('Name of switch model has to be of type string')
                if len(val) < 1:
                    raise ValueError('Length of name of switch model cannot be zero')
                continue

            if key == 'ports':
                if type(val) is not list:
                    raise TypeError('List of ports for switch model has to be of type list')
                for port in val:
                    if type(port) is not PortModel:
                        raise TypeError('Ports in list of ports for switch model has to be of type PortModel')
                continue

            if key == 'size':
                if val is None:
                    continue
                if type(val) is not int:
                    raise TypeError('Size of switch model has to be of type int')
                if val < 1:
                    raise ValueError('Size of switch model cannot be less than 1')
                continue

            raise TypeError("Unexpected attribute '{}' for switch".format(key))

        return kwargs

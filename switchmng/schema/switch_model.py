from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Column
from sqlalchemy.orm import relationship

from .base import Base
from .port_model import PortModel

class SwitchModel(Base):
    """
    Represents a switch model resource.

    This resource is uniquely identified by its name.
    All contained id fields are private and only used for storing object in
    database.

    :param name: Name uniquely identifying this switch model
        Acts as resource identifier.
    :type name: str

    :param ports: Ports associated with this switch model
    :type ports: list

    :param size: Size (number of rack units) this switch takes up in server rack
    :type size: int
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
        self.name = name
        self.ports = ports
        self.size = size

    @property
    def name(self):
        """Name uniquely identifying this switch model"""

        return self._name

    @name.setter
    def name(self, name):
        SwitchModel.check_params(name = name)
        self._name = name

    @property
    def ports(self):
        """Ports associated with this switch model"""

        # Sort list by name of port
        self._ports.sort(key = lambda p: p.name)

        return self._ports

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
        Modify existing ports of this switch model.

        All ports given but not present will not be added.

        All ports not given but present will not be changed.

        :param ports: List of ports to change
        :type ports: list
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
        """Size (number of rack units) this switch takes up in server rack"""

        return self._size

    @size.setter
    def size(self, size):
        SwitchModel.check_params(size = size)
        self._size = size

    def port(self, resource_id):
        """Return port of this switch model identified by resource identifier

        Returns the port for the given resource identifier or None if this
        switch model does not contain a matching port.

        :param resource_id: The resource id of the port to return object of
        :type resource_id: str

        :return: The :class:`PortModel` object identified by given resource id
        """

        if not isinstance(resource_id, str):
            return None

        # Search for port with specified name
        for port in self._ports:
            if port.name == resource_id:
                return port

        # Did not find port for given port name
        return None

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
                 'ports': [ p.jsonify() for p in self.ports ],
                 'size': self.size }

    def __str__(self):
        return str(self.name)

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
                    raise TypeError('Name of switch model has to be of type string')
                if len(val) < 1:
                    raise ValueError('Length of name of switch model cannot be zero')
                continue

            if key == 'ports':
                if not isinstance(val, list):
                    raise TypeError('List of ports for switch model has to be of type list')
                for port in val:
                    if not isinstance(port, PortModel):
                        raise TypeError('Ports in list of ports for switch model has to be of type PortModel')
                continue

            if key == 'size':
                if val is None:
                    continue
                if not isinstance(val, int):
                    raise TypeError('Size of switch model has to be of type int')
                if val < 1:
                    raise ValueError('Size of switch model cannot be less than 1')
                continue

            raise TypeError("Unexpected attribute '{}' for switch".format(key))

        return kwargs

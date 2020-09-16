from . import *

class Switch(Base):
    """
    Represents a switch resource.

    This resource is uniquely identified by its name.
    All contained id fields are private and only used for storing object in
    database.

    :param name: Name uniquely identifying this switch
    :type name: str

    :param model: Model of this switch
    :type model: :class:`SwitchModel`

    :param ports: Ports associated with this switch
    :type ports: list

    :param location: Location of this switch in server rack
    :type location: int
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

    def __init__(self, name = None, model = None, ports = None, location = None):
        # Assign name from argument
        if not isinstance(name, str):
            raise TypeError('Expected name of switch to be of type str')
        self.name = name

        # Assign model from argument
        if not isinstance(model, SwitchModel):
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
        """Name uniquely identifying this switch"""

        return self._name

    @name.setter
    def name(self, name):
        Switch.check_params(name = name)
        self._name = name

    @property
    def model(self):
        """Model of this switch"""

        return self._model

    @model.setter
    def model(self, model):
        Switch.check_params(model = model)
        self._model = model

        # If switch model changed we need to update all
        # ports of this switch to reflect ports from model.
        self._sync_ports_from_model()

    @property
    def ports(self):
        """Ports associated with this switch.

        The list of ports always contains ports for all :class:`PortModel`
        ports of this switches :class:`SwitchModel`.
        If this switches :class:`SwitchModel` gets modified this switches
        list of ports gets modified as well.
        """

        # Sort list by name of port
        self._ports.sort(key = lambda p: p.name)

        return self._ports

    @ports.setter
    def ports(self, ports):
        """
        Set all ports of this switch.
        All ports not given but present will be reset
        """

        # Check ports
        Switch.check_params(ports = ports)

        # Check if given ports exist in the switch model
        for p in ports:
            if self.model._port_by_name(p.name) is None:
                raise ValueError(
                    "Port '{}' does not exist in switch model '{}' of switch '{}'"
                    .format(str(p), str(self.model), str(self)))

        # Apply new port list
        self._ports = ports

        # We changed the port list so we have to make sure all ports of
        # switch model are present.
        self._sync_ports_from_model()

    def modify_ports(self, ports):
        """
        Modify existing ports of this switch.

        This will not add any new ports that are not already present on this
        switch. (Modify ports of :class:`SwitchModel` for that)

        All ports not given but present will not be changed.

        :param ports: List of ports to change
        :type ports: list
        """

        # Check ports
        Switch.check_params(ports = ports)

        # Check if given ports exist in the switch model
        for p in ports:
            if self.model._port_by_name(p.name) is None:
                raise ValueError(
                    "Port '{}' does not exist in switch model '{}' of switch '{}'"
                    .format(str(p), str(self.model), str(self)))

        # Never add or delete any ports only apply changes.
        # Don't touch non specified ports.
        for new_port in ports:
            for i, old_port in enumerate(self._ports):
                if old_port.name == new_port.name:
                    self._ports[i] = new_port
                    break

    @property
    def location(self):
        """Location of this switch in server rack"""

        return self._location

    @location.setter
    def location(self, location):
        if not isinstance(location, int):
            raise TypeError('Expected location of switch to be of type int')
        self._location = location

    def _sync_ports_from_model(self):
        """
        Synchronize ports from switch model.

        All ports that have a name that does not exist in switch model will
        get removed.
        All ports from switch model that do not exist in this object will
        be added.
        """

        # Port list 1: Ports currently set that also exist in switch model
        nports1 = [ p
                    for p in self._ports
                    if self.model._port_by_name(p.name) is not None ]

        # Port list 2: Ports from switch model that do not currently exist
        nports2 = [ Port(name = p.name)
                    for p in self.model._ports
                    if self._port_by_name(p.name) is None ]

        # Set ports of this switch to concatenation of generated two lists
        self._ports = nports1 + nports2

    def _port_by_name(self, port_name):
        """Return port of this switch identified by name

        Returns the port for the given name or None if this switch
        does not contain a port with given name.

        :param port_name: The name of the port to return object of
        :type port_name: str

        :return: The :class:`Port` object identified by given name
        """

        if not isinstance(port_name, str):
            return None

        # Search for port with specified name
        for port in self._ports:
            if port.name == port_name:
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
                 'location': self.location,
                 'model': str(self.model),
                 'ports': [ p.jsonify() for p in self.ports ] }

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
                    raise TypeError('Name of switch has to be of type str')
                if len(val) < 1:
                    raise ValueError('Length of name of switch cannot be zero')
                continue

            if key == 'model':
                if not isinstance(val, SwitchModel):
                    raise TypeError('Switch model of switch has to be of type SwitchModel')
                continue

            if key == 'ports':
                if not isinstance(val, list):
                    raise TypeError('List of ports for switch has to be of type list')
                for port in val:
                    if not isinstance(port, Port):
                        raise TypeError('Ports in list of ports for switch has to be of type Port')
                continue

            if key == 'location':
                if val is None:
                    continue
                if not isinstance(val, int):
                    raise TypeError('Given location of switch has to be of type int')
                continue

            raise TypeError("Unexpected attribute '{}' for switch".format(key))

        return kwargs


import ipaddress

from typing import TYPE_CHECKING
from typing import cast
from typing import List
from typing import Optional

from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from switchmng.typing import JsonDict

from .base import Base
from .switch_model import SwitchModel
from .port import Port

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
    _ip = Column('ip', String, nullable = True)

    def __init__(
            self,
            name: Optional[str] = None,
            model: Optional[SwitchModel] = None,
            ports: Optional[List[Port]] = None,
            location: Optional[int] = None,
            ip: Optional[str] = None) -> None:

        if ports is None:
            ports = []

        # Make type checking happy
        # (property setter makes sure to set only correct type)
        if TYPE_CHECKING:
            name = cast(str, name)
            model = cast(SwitchModel, model)

        self.name = name
        self.model = model
        self.ports = ports
        self.location = location
        self.ip = ip

    @property
    def name(self) -> str:
        """Name uniquely identifying this switch"""

        return self._name

    @name.setter
    def name(self, name: str) -> None:
        Switch.check_params(name = name)
        self._name = name

    @property
    def model(self) -> SwitchModel:
        """Model of this switch"""

        return self._model

    @model.setter
    def model(self, model: SwitchModel) -> None:
        Switch.check_params(model = model)
        self._model = model

        # If switch model changed we need to update all
        # ports of this switch to reflect ports from model.
        self._sync_ports_from_model()

    @property
    def ports(self) -> List[Port]:
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
    def ports(self, ports: List[Port]) -> None:
        """
        Set all ports of this switch.
        All ports not given but present will be reset
        """

        # Check ports
        Switch.check_params(ports = ports)

        # Check if given ports exist in the switch model
        for port in ports:
            if self.model.port(port.name) is None:
                raise ValueError(
                    "Port '{}' does not exist in switch model '{}' of switch '{}'"
                    .format(str(port), str(self.model), str(self)))

        # Apply new port list
        self._ports = ports

        # We changed the port list so we have to make sure all ports of
        # switch model are present.
        self._sync_ports_from_model()

    @property
    def location(self) -> Optional[int]:
        """Location of this switch in server rack"""

        return self._location

    @location.setter
    def location(self, location: int) -> None:
        Switch.check_params(location = location)
        self._location = location

    @property
    def ip(self) -> Optional[str]:
        """Ip of this switch"""

        return self._ip

    @ip.setter
    def ip(self, ip: str) -> None:
        Switch.check_params(ip = ip)
        self._ip = ip

    def _sync_ports_from_model(self) -> None:
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
                    if self.model.port(p.name) is not None ]

        # Port list 2: Ports from switch model that do not currently exist
        nports2 = [ Port(name = p.name)
                    for p in self.model.ports
                    if self.port(p.name) is None ]

        # Set ports of this switch to concatenation of generated two lists
        self._ports = nports1 + nports2

    def port(self, resource_id: str) -> Optional[Port]:
        """Return port of this switch identified by resource identifier

        Returns the port for the given resource identifier or None if this
        switch does not contain a matching port.

        :param resource_id: The resource id of the port to return object of
        :type resource_id: str

        :return: The :class:`Port` object identified by given resource id
        """

        if not isinstance(resource_id, str):
            return None

        # Search for port with specified name
        for port in self._ports:
            if port.name == resource_id:
                return port

        # Did not find port for given port name
        return None

    def jsonify(self) -> JsonDict:
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
                 'model': str(self.model),
                 'ports': [ p.jsonify() for p in self.ports ],
                 'location': self.location,
                 'ip': self.ip }

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return self.__str__()

    @staticmethod
    def check_params(**kwargs) -> None:
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

            elif key == 'model':
                if not isinstance(val, SwitchModel):
                    raise TypeError('Switch model of switch has to be of type SwitchModel')

            elif key == 'ports':
                if not isinstance(val, list):
                    raise TypeError('List of ports for switch has to be of type list')
                for port in val:
                    if not isinstance(port, Port):
                        raise TypeError('Ports in list of ports for switch has to be of type Port')

            elif key == 'location':
                if val is None:
                    continue
                if not isinstance(val, int):
                    raise TypeError('Given location of switch has to be of type int')

            elif key == 'ip':
                if val is None:
                    continue
                if not isinstance(val, str):
                    raise TypeError('Given ip of switch has to be of type int')

                is_ip = True
                try:
                    ipaddress.ip_address(val)
                except ValueError:
                    is_ip = False
                if not is_ip:
                    raise ValueError('Given ip of switch has to be a valid IPv4 address')

            else:
                raise TypeError("Unexpected attribute '{}' for switch".format(key))

from typing import TYPE_CHECKING
from typing import cast
from typing import List
from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship

from switchmng.typing import JsonDict

from .base import Base
from .network_protocol import NetworkProtocol
from .connector import Connector

network_protocols_port_models_mapping = Table(
    'network_protocols_port_models',
    Base.metadata,
    Column(
        'port_model_id',
        Integer,
        ForeignKey('port_models.id'),
        primary_key = True),
    Column(
        'network_protocol_id',
        Integer,
        ForeignKey('network_protocols.id'),
        primary_key = True),
)

class PortModel(Base):
    """
    Represents a port model resource.

    This resource is uniquely identified by the switch model (See
    :class:`SwitchModel`) containing it in combination with its name.
    All contained id fields are private and only used for storing object in
    database.

    :param name: The identifier of this port. Must be unique for the
        containing :class:`SwitchModel`.
    :type name: str

    :param network_protocols: List of possible network protocols of this port
    :type network_protocols: list

    :param connector: Physical connector of this port
    :type connector: :class:`Connector`
    """

    __tablename__ = 'port_models'

    # Database id
    _port_model_id = Column('id', Integer, primary_key = True, nullable = False)
    _switch_model_id = Column('switch_model_id', Integer,
                             ForeignKey('switch_models.id'), nullable = False)
    connector_id = Column('connector_id', Integer,
                          ForeignKey('connectors.id'), nullable = True)

    # Resource state
    _name = Column('name', String, nullable = False)
    _network_protocols = relationship(
        'NetworkProtocol',
        secondary = network_protocols_port_models_mapping,
        uselist = True)
    _connector = relationship('Connector')

    def __init__(
            self,
            name: Optional[str] = None,
            network_protocols: Optional[List[NetworkProtocol]] = None,
            connector: Optional[Connector] = None):

        if network_protocols is None:
            network_protocols = []

        # Make type checking happy
        # (property setter makes sure to set only correct type)
        if TYPE_CHECKING:
            name = cast(str, name)

        self.name = name
        self.network_protocols = network_protocols
        self.connector = connector

    @property
    def name(self) -> str:
        """The identifier of this port.

        Must be unique for the containing :class:`SwitchModel`"""

        return self._name

    @name.setter
    def name(self, name: str) -> None:
        PortModel.check_params(name = name)
        self._name = name

    @property
    def network_protocols(self) -> List[NetworkProtocol]:
        """List of possible network protocols of this port"""

        return self._network_protocols

    @network_protocols.setter
    def network_protocols(self, network_protocols: List[NetworkProtocol]) -> None:
        PortModel.check_params(network_protocols = network_protocols)
        self._network_protocols = network_protocols

    @property
    def connector(self) -> Optional[Connector]:
        """Physical connector of this port"""

        return self._connector

    @connector.setter
    def connector(self, connector: Optional[Connector]) -> None:
        PortModel.check_params(connector = connector)
        self._connector = connector

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
                 'network_protocols': [ str(np) for np in self.network_protocols ],
                 'connector': None if self.connector is None else str(self.connector) }

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
                    raise TypeError('Name of port model has to be of type str')
                if len(val) < 1:
                    raise ValueError('Length of name of port model cannot be zero')

            elif key == 'network_protocols':
                if not isinstance(val, list):
                    raise TypeError(
                        'List of network protocols for port model has to ' + \
                        'be of type list')
                for network_protocol in val:
                    if not isinstance(network_protocol, NetworkProtocol):
                        raise TypeError(
                            'Network protocol in list of network ' + \
                            'protocols for port has to be of type ' + \
                            'NetworkProtocol')

            elif key == 'connector':
                if val is None:
                    continue
                if not isinstance(val, Connector):
                    raise TypeError('Connector of port model has to be of type Connector')

            else:
                raise TypeError("Unexpected attribute '{}' for port model".format(key))

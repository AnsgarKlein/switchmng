from typing import Any
from typing import Dict

from sqlalchemy import Integer, String
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship

from .base import Base
from .base_resource import BaseResource
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

class PortModel(BaseResource, Base):
    """
    Represents a port model resource.

    This resource is uniquely identified by the switch model (See
    :class:`SwitchModel`) containing it in combination with its name.

    :param name: The identifier of this port. Must be unique for the
        containing :class:`SwitchModel`.
    :type name: str

    :param network_protocols: List of possible network protocols of this port
    :type network_protocols: list

    :param connector: Physical connector of this port
    :type connector: :class:`Connector`
    """

    ResourceIdentifier = 'name'
    """*Name* of the attribute that is this resource's identifier"""

    _Attributes: Dict[str, Dict[str, Any]] = {
        'name': {
            'type':     str,
            'list':     False,
            'private':  '_name',
            'checks':   [ lambda cls, n: len(n) > 0 ],
            'optional': False,
        },
        'network_protocols': {
            'type':     NetworkProtocol,
            'list':     True,
            'private':  '_network_protocols',
            'jsonify':  lambda ps: [ str(p) for p in ps ],
            'optional': True,
            'null':     [],
        },
        'connector': {
            'type':     Connector,
            'list':     False,
            'private':  '_connector',
            'jsonify':  lambda c: None if c is None else str(c),
            'optional': True,
            'null':     None,
        },
    }

    __tablename__ = 'port_models'

    # Database id
    _port_model_id = Column('id', Integer, primary_key = True, nullable = False)
    _switch_model_id = Column('switch_model_id', Integer,
                             ForeignKey('switch_models.id'), nullable = False)
    _connector_id = Column('connector_id', Integer,
                          ForeignKey('connectors.id'), nullable = True)

    # Resource state
    _name = Column('name', String, nullable = False)
    _network_protocols = relationship(
        'NetworkProtocol',
        secondary = network_protocols_port_models_mapping,
        uselist = True)
    _connector = relationship('Connector')

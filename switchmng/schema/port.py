from typing import Any
from typing import Dict

from sqlalchemy import Integer, String
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship

from .base import Base
from .base_resource import BaseResource
from .vlan import Vlan

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

class Port(BaseResource, Base):
    """
    Represents a port of a switch.

    That is a concrete port of a concrete switch.
    This resource is uniquely identified by the switch (See
    :class:`Switch`) containing it in combination with its name.

    :param name: The identifier of this port. Must be unique for the
        containing :class:`Switch`.
    :type name: str

    :param vlans: A list of vlans that are active on this port
    :type vlans: list

    :param target: Host that is connected to this port
    :type target: str
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
        'vlans': {
            'type':     Vlan,
            'list':     True,
            'private':  '_vlans',
            'jsonify':  lambda vs: [ int(str(v)) for v in vs ],
            'optional': True,
            'null':     [],
        },
        'target': {
            'type':     str,
            'list':     False,
            'private':  '_target',
            'checks':   [ lambda cls, n: len(n) > 0 ],
            'optional': True,
            'null':     None,
        },
    }

    __tablename__ = 'ports'

    # Database id
    _port_id = Column('id', Integer, primary_key = True, nullable = False)
    _switch_id = Column('switch_id', Integer, ForeignKey('switches.id'),
                       nullable = False)

    # Resource state
    _name = Column('name', String, nullable = False)
    _vlans = relationship('Vlan', secondary = vlans_ports_mapping, uselist = True)
    _target = Column('target', String, nullable = True)

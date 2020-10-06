from typing import Any
from typing import Dict

from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Column

from .base import Base
from .base_resource import BaseResource

class NetworkProtocol(BaseResource, Base):
    """
    Represents a network protocol resource.

    This resource is uniquely identified by its name.

    :param name: Name uniquely identifying this network protocol
    :type name: str

    :param speed: Maximum possible speed of this network protocol in Mb/s
    :type speed: int
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
        'speed': {
            'type':     int,
            'list':     False,
            'private':  '_speed',
            'checks':   [ lambda cls, s: s > 0 ],
            'optional': True,
            'null':     None,
        },
    }

    __tablename__ = 'network_protocols'

    # Database id
    _network_protocol_id = Column('id', Integer, primary_key = True, nullable = False)

    # Resource identifier
    _name = Column('name', String, nullable = False, unique = True)

    # Resource state
    _speed = Column('speed', Integer, nullable = True)

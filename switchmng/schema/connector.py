from typing import Any
from typing import Dict

from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Column

from .base import Base
from .base_resource import BaseResource

class Connector(BaseResource, Base):
    """
    Represents a physical port connector.

    This resource is uniquely identified by its name.

    :param name: Name uniquely identifying this port connector
    :type name: str
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
    }

    __tablename__ = 'connectors'

    # Database id
    _connector_id = Column('id', Integer, primary_key = True, nullable = False)

    # Resource identifier
    _name = Column('name', String, nullable = False, unique = True)

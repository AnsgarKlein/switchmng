from typing import Any
from typing import Dict

from sqlalchemy import Integer, String
from sqlalchemy import Column

from .base import Base
from .base_resource import BaseResource

class Vlan(BaseResource, Base):
    """
    Represents a VLAN resource.

    This resource is uniquely identified by its vlan tag.

    :param tag: Tag uniquely identifying this VLAN
    :type tag: int

    :param description: Description of this VLAN
    :type description: str
    """

    ResourceIdentifier = 'tag'

    _Attributes: Dict[str, Dict[str, Any]] = {
        'tag': {
            'type':     int,
            'list':     False,
            'private':  '_tag',
            'checks':   [ lambda cls, t: t > 0 ],
            'optional': False,
        },
        'description': {
            'type':     str,
            'list':     False,
            'private':  '_description',
            'checks':   [ lambda cls, d: len(d) > 0 ],
            'optional': True,
            'null':     None,
        },
    }

    __tablename__ = 'vlans'

    # Database id
    _vlan_id = Column('id', Integer, primary_key = True, nullable = False)

    # Resource identifier
    _tag = Column('tag', Integer, nullable = False, unique = True)

    # Resource state
    _description = Column('name', String, nullable = True)

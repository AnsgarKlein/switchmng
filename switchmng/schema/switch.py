import ipaddress

from typing import Any
from typing import Dict
from typing import Optional

from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from .base import Base
from .base_resource import BaseResource
from .switch_model import SwitchModel
from .port import Port

def _is_valid_ip(ip) -> bool:
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        return False

    return True

class Switch(BaseResource, Base):
    """
    Represents a switch resource.

    This resource is uniquely identified by its name.

    :param name: Name uniquely identifying this switch
    :type name: str

    :param model: Model of this switch
    :type model: :class:`SwitchModel`

    :param ports: Ports associated with this switch
    :type ports: list

    :param location: Location of this switch in server rack
    :type location: int

    :param ip: IP Address of this switch
    :type ip: str
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
        'model': {
            'type':       SwitchModel,
            'list':       False,
            'private':    '_model',
            'post_hooks': [ lambda obj: obj.sync_ports_from_model() ],
            'jsonify':    str,
            'optional':   False,
        },
        'ports': {
            'type':       Port,
            'list':       True,
            'private':    '_ports',
            'post_hooks': [ lambda obj: obj.sync_ports_from_model() ],
            'jsonify':    lambda ps: [ p.jsonify() for p in ps ],
            'optional':   True,
            'null':       [],
        },
        'location': {
            'type':     int,
            'list':     False,
            'private':  '_location',
            'checks':   [ lambda cls, l: l >= 0 ],
            'optional': True,
            'null':     None,
        },
        'ip': {
            'type':     str,
            'list':     False,
            'private':  '_ip',
            'checks':   [ lambda cls, i: _is_valid_ip(i) ],
            'optional': True,
            'null':     None,
        },
    }

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

    def sync_ports_from_model(self) -> None:
        """
        Synchronize ports from switch model.

        All ports that have a name that does not exist in switch model will
        get removed.
        All ports from switch model that do not exist in this object will
        be added.
        """

        # If model is not yet set do not change any ports
        if self.model is None:
            return

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

from typing import Any
from typing import Dict
from typing import Optional

from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Column
from sqlalchemy.orm import relationship

from .base import Base
from .base_resource import BaseResource
from .port_model import PortModel

class SwitchModel(BaseResource, Base):
    """
    Represents a switch model resource.

    This resource is uniquely identified by its name.

    :param name: Name uniquely identifying this switch model
        Acts as resource identifier.
    :type name: str

    :param ports: Ports associated with this switch model
    :type ports: list

    :param size: Size (number of rack units) this switch takes up in server rack
    :type size: int
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
        'ports': {
            'type':       PortModel,
            'list':       True,
            'private':    '_ports',
            'post_hooks': [ lambda obj: obj.refresh_switches() ],
            'jsonify':    lambda ps: [ p.jsonify() for p in ps ],
            'optional':   True,
            'null':       [],
        },
        'size': {
            'type':     int,
            'list':     False,
            'private':  '_size',
            'checks':   [ lambda obj, s: s > 0 ],
            'optional': True,
            'null':     None,
        },
    }

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

    def refresh_switches(self) -> None:
        """ Refresh ports of all switches using this switch model."""

        for sw in self._switches:
            sw.sync_ports_from_model()

    def port(self, resource_id: str) -> Optional[PortModel]:
        """
        Return port of this switch model identified by resource identifier.

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

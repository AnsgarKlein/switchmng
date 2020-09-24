from sqlalchemy import Integer, String
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship

from .base import Base
from .network_protocol import NetworkProtocol
from .connector import Connector
from .vlan import Vlan
from .port_model import PortModel
from .switch_model import SwitchModel
from .port import Port
from .switch import Switch
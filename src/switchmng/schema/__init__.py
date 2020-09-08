from sqlalchemy import Integer, String
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship

from .base import Base
from .port_type import PortType
from .vlan import Vlan
from .switch_model import SwitchModel
from .switch import Switch

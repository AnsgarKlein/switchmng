from sqlalchemy import Integer, String
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship

from .Base import Base
from .PortType import PortType
from .Vlan import Vlan
from .SwitchModel import SwitchModel
from .Switch import Switch

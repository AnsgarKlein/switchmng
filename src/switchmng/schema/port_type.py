from . import *

class PortType(Base):
    """
    Represents a port type resource.

    This resource is uniquely identified by its description.
    All contained id fields are private and only used for storing object in
    database.

    Attributes
    ----------

    description : str
        Name uniquely identifying this port type
    speed : int
        Speed of this port type in Mb/s
    """

    __tablename__ = 'port_types'

    # Database id
    _port_type_id = Column('id', Integer, primary_key = True, nullable = False)

    # Resource identifier
    _description = Column('description', String, nullable = False, unique = True)

    # Resource state
    _speed = Column('speed', Integer, nullable = True)

    def __init__(self, description = None, speed = None):
        self.description = description
        self.speed = speed

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        PortType.check_params(description = description)
        self._description = description

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed):
        PortType.check_params(speed = speed)
        self._speed = speed

    def jsonify(self):
        return { 'description': self.description,
                 'speed': self.speed }

    def __str__(self):
        return self.description

    def __repr__(self):
        return self.__str__()

    def check_params(**kwargs):
        for key, val in kwargs.items():
            if key == 'description':
                if type(val) is not str:
                    raise TypeError('Description of port type has to be of type str')
                continue

            if key == 'speed':
                if type(val) is not int and val is not None:
                    raise TypeError('Speed of port type has to be of type int')
                if val < 0:
                    raise ValueError('Speed of port type cannot be less than 0')
                continue

            raise TypeError("Unexpected attribute '{}' for port type".format(key))

        return kwargs


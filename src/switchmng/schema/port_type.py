from . import *

class PortType(Base):
    """
    Represents a port type resource.

    This resource is uniquely identified by its description.
    All contained id fields are private and only used for storing object in
    database.

    :param description: Name uniquely identifying this port type
    :type description: str

    :param speed: Speed of this port type in Mb/s
    :type speed: int
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
        """Name uniquely identifying this port type"""
        return self._description

    @description.setter
    def description(self, description):
        PortType.check_params(description = description)
        self._description = description

    @property
    def speed(self):
        """Speed of this port type in Mb/s"""
        return self._speed

    @speed.setter
    def speed(self, speed):
        PortType.check_params(speed = speed)
        self._speed = speed

    def jsonify(self):
        """
        Represent this object as a json-ready dict.

        That is a dict which completely consists of json-compatible structures
        like:

        * dict
        * list
        * string
        * int
        * bool
        * None / null
        """

        return { 'description': self.description,
                 'speed': self.speed }

    def __str__(self):
        return self.description

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def check_params(**kwargs):
        """
        Check all given parameters.

        Check if all given parameters have the correct type and are valid
        parameters for a object of this class at all as well as other
        basic checks.

        This function gets executed when trying to assign values to object
        variables but can be called when needing to check multiple parameters
        at once in order to prevent half changed states.

        :raises TypeError: When type of given parameter does not match
            expectation
        :raises ValueError: When value of given parameter does not match
            expectation
        """

        for key, val in kwargs.items():
            if key == 'description':
                if not isinstance(val, str):
                    raise TypeError('Description of port type has to be of type str')
                continue

            if key == 'speed':
                if not isinstance(val, int) and val is not None:
                    raise TypeError('Speed of port type has to be of type int')
                if val < 0:
                    raise ValueError('Speed of port type cannot be less than 0')
                continue

            raise TypeError("Unexpected attribute '{}' for port type".format(key))

        return kwargs


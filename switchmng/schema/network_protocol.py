from typing import TYPE_CHECKING
from typing import cast
from typing import Optional

from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Column

from switchmng.typing import JsonDict

from .base import Base

class NetworkProtocol(Base):
    """
    Represents a network protocol resource.

    This resource is uniquely identified by its name.
    All contained id fields are private and only used for storing object in
    database.

    :param name: Name uniquely identifying this network protocol
    :type name: str

    :param speed: Maximum possible speed of this network protocol in Mb/s
    :type speed: int
    """

    __tablename__ = 'network_protocols'

    # Database id
    _network_protocol_id = Column('id', Integer, primary_key = True, nullable = False)

    # Resource identifier
    _name = Column('name', String, nullable = False, unique = True)

    # Resource state
    _speed = Column('speed', Integer, nullable = True)

    def __init__(
            self,
            name: Optional[str] = None,
            speed: Optional[int] = None):

        # Make type checking happy
        # (property setter makes sure to set only correct type)
        if TYPE_CHECKING:
            name = cast(str, name)

        self.name = name
        self.speed = speed

    @property
    def name(self) -> str:
        """Name uniquely identifying this network protocol"""

        return self._name

    @name.setter
    def name(self, name: str) -> None:
        NetworkProtocol.check_params(name = name)
        self._name = name

    @property
    def speed(self) -> Optional[int]:
        """Maximum possible speed of this network protocol in Mb/s"""

        return self._speed

    @speed.setter
    def speed(self, speed: int) -> None:
        NetworkProtocol.check_params(speed = speed)
        self._speed = speed

    def jsonify(self) -> JsonDict:
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

        return { 'name': self.name,
                 'speed': self.speed }

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
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
            if key == 'name':
                if not isinstance(val, str):
                    raise TypeError('Name of network protocol has to be of type str')
                if len(val) < 1:
                    raise ValueError('Name of network protocol cannot be empty')

            elif key == 'speed':
                if not isinstance(val, int) and val is not None:
                    raise TypeError('Speed of network protocol has to be of type int')
                if val < 0:
                    raise ValueError('Speed of network protocol cannot be less than 0')

            else:
                raise TypeError("Unexpected attribute '{}' for network protocol".format(key))

        return kwargs

from typing import TYPE_CHECKING
from typing import cast
from typing import Optional

from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Column

from switchmng.typing import JsonDict

from .base import Base

class Connector(Base):
    """
    Represents a physical port connector.

    This resource is uniquely identified by its name.
    All contained id fields are private and only used for storing object in
    database.

    :param name: Name uniquely identifying this port connector
    :type name: str
    """

    __tablename__ = 'connectors'

    # Database id
    _connector_id = Column('id', Integer, primary_key = True, nullable = False)

    # Resource identifier
    _name = Column('name', String, nullable = False, unique = True)

    def __init__(self, name: Optional[str] = None):
        # Make type checking happy
        # (property setter makes sure to set only correct type)
        if TYPE_CHECKING:
            name = cast(str, name)

        self.name = name

    @property
    def name(self) -> str:
        """Name uniquely identifying this connector"""

        return self._name

    @name.setter
    def name(self, name: str) -> None:
        Connector.check_params(name = name)
        self._name = name

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

        return { 'name': self.name }

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return self.__str__()

    @staticmethod
    def check_params(**kwargs) -> None:
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
                    raise TypeError('Name of connector has to be of type str')
                if len(val) < 1:
                    raise ValueError('Name of connector cannot be empty')

            else:
                raise TypeError("Unexpected attribute '{}' for connector".format(key))

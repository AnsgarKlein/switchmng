from typing import TYPE_CHECKING
from typing import cast
from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy import Column

from switchmng.typing import JsonDict

from .base import Base

class Vlan(Base):
    """
    Represents a VLAN resource consisting of description and VLAN tag id.

    :param tag: Tag uniquely identifying this VLAN
    :type tag: int

    :param description: Description of this VLAN
    :type description: str
    """

    __tablename__ = 'vlans'

    # Database id
    _vlan_id = Column('id', Integer, primary_key = True, nullable = False)

    # Resource identifier
    _tag = Column('tag', Integer, nullable = False, unique = True)

    # Resource state
    _description = Column('name', String, nullable = True)

    def __init__(
            self,
            tag: Optional[int] = None,
            description: Optional[str] = None):

        # Make type checking happy
        # (property setter makes sure to set only correct type)
        if TYPE_CHECKING:
            tag = cast(int, tag)

        self.tag = tag
        self.description = description

    @property
    def tag(self) -> int:
        """Tag uniquely identifying this VLAN"""
        return self._tag

    @tag.setter
    def tag(self, tag: int) -> None:
        Vlan.check_params(tag = tag)
        self._tag = tag

    @property
    def description(self) -> Optional[str]:
        """Description of this VLAN"""
        return self._description

    @description.setter
    def description(self, description: str) -> None:
        Vlan.check_params(description = description)
        self._description = description

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

        return { 'tag': self.tag,
                 'description': self.description }

    def __str__(self) -> str:
        return str(self.tag)

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
            if key == 'tag':
                if not isinstance(val, int):
                    raise TypeError('Tag of vlan has to be of type int')
                if val < 1:
                    raise ValueError('Tag of vlan cannot be less than 1')
                continue

            if key == 'description':
                if val is None:
                    continue
                if not isinstance(val, str):
                    raise TypeError('Description of vlan has to be of type str')
                continue

            raise TypeError("Unexpected attribute '{}' for vlan".format(key))

        return kwargs

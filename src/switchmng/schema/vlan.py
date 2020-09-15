from . import *

class Vlan(Base):
    """
    Represents a VLAN resource consisting of description and VLAN tag id.

    Attributes
    ----------

    tag : int
        Tag uniquely identifying this VLAN
    description : str
        Description of this VLAN
    """

    __tablename__ = 'vlans'

    # Database id
    _vlan_id = Column('id', Integer, primary_key = True, nullable = False)

    # Resource identifier
    _tag = Column('tag', Integer, nullable = False, unique = True)

    # Resource state
    _description = Column('name', String, nullable = False)

    def __init__(self, tag = None, description = None):
        self.tag = tag
        self.description = description

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, tag):
        Vlan.check_params(tag = tag)
        self._tag = tag

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        Vlan.check_params(description = description)
        self._description = description

    def jsonify(self):
        return { 'tag': self.tag,
                 'description': self.description }

    def __str__(self):
        return str(self.tag)

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def check_params(**kwargs):
        for key, val in kwargs.items():
            if key == 'tag':
                if not isinstance(val, int):
                    raise TypeError('Tag of vlan has to be of type int')
                if val < 1:
                    raise ValueError('Tag of vlan cannot be less than 1')
                continue

            if key == 'description':
                if not isinstance(val, str):
                    raise TypeError('Description of vlan has to be of type str')
                continue

            raise TypeError("Unexpected attribute '{}' for vlan".format(key))

        return kwargs


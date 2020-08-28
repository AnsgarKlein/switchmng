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
    tag = Column('tag', Integer, nullable = False, unique = True)

    # Resource state
    description = Column('name', String, nullable = False)

    def __init__(self, tag = None, description = None):
        if type(tag) is not int:
            raise TypeError('Expected vlan id to be of type int')
        self.tag = tag

        if type(description) is not str:
            raise TypeError('Expected vlan description to be of type string')
        self.description = description

    def jsonify(self):
        return { 'tag': str(self.tag),
                 'description': self.description }

    def __str__(self):
        return str(self.tag)

    def __repr__(self):
        return self.__str__()


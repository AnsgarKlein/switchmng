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
    description = Column('description', String, nullable = False, unique = True)

    # Resource state
    speed = Column('speed', Integer, nullable = False)

    def __init__(self, description, speed):
        if type(description) is not str:
            raise TypeError('Expected description of port type to be of type string')
        else:
            self.description = description

        if type(speed) is not int:
            raise TypeError('Expected speed of port type to be of type int')
        else:
            self.speed = speed

    def jsonify(self):
        return { 'description': self.description,
                 'speed': self.speed }

    def __str__(self):
        return self.description

    def __repr__(self):
        return self.__str__()


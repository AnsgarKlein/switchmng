from . import *

class PortModel(Base):
    """
    Represents a port of a switch model.

    That is a port not of a concrete switch but a port of a type of
    switch. (See :class:`SwitchModel`)

    :param name: The identifier of this port. Must be unique for the
        containing :class:`SwitchModel`.
    :type name: str

    :param port_type: The port type of this port
    :type port_type: class:`PortType`

    """

    __tablename__ = 'port_models'

    # Database id
    _port_model_id = Column('id', Integer, primary_key = True, nullable = False)
    _switch_model_id = Column('switch_model_id', Integer,
                             ForeignKey('switch_models.id'), nullable = False)
    port_type_id = Column('port_type_id', Integer,
                          ForeignKey('port_types.description'), nullable = True)

    # Attributes
    _name = Column('name', String, nullable = False)
    _port_type = relationship('PortType', uselist = False)

    def __init__(self, name = None, port_type = None):
        self.name = name
        self.port_type = port_type

    @property
    def name(self):
        """The identifier of this port.

        Must be unique for the containing :class:`SwitchModel`"""
        return self._name

    @name.setter
    def name(self, name):
        PortModel.check_params(name = name)
        self._name = name

    @property
    def port_type(self):
        """The port type of this port"""
        return self._port_type

    @port_type.setter
    def port_type(self, port_type):
        PortModel.check_params(port_type = port_type)
        self._port_type = port_type

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

        return { 'name': self.name,
                 'port_type': None if self.port_type is None else str(self.port_type) }

    def __str__(self):
        return self.name

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
            if key == 'name':
                if not isinstance(val, str):
                    raise TypeError('Name of port model has to be of type str')
                if len(val) < 1:
                    raise ValueError('Length of name of port model cannot be zero')
                continue

            if key == 'port_type':
                if val is None:
                    continue
                if not isinstance(val, PortType):
                    raise TypeError('Port type of port model has to be of type PortType')
                continue

            raise TypeError("Unexpected attribute '{}' for port model".format(key))

        return kwargs


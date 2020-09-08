from . import *

class PortModel(Base):
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
        return self._name

    @name.setter
    def name(self, name):
        PortModel.check_params(name = name)
        self._name = name

    @property
    def port_type(self):
        return self._port_type

    @port_type.setter
    def port_type(self, port_type):
        PortModel.check_params(port_type = port_type)
        self._port_type = port_type

    def jsonify(self):
        return { 'name': self.name,
                 'port_type': None if self.port_type is None else str(self.port_type) }

    def check_params(**kwargs):
        for key, val in kwargs.items():
            if key == 'name':
                if type(val) is not str:
                    raise TypeError('Name of port model has to be of type str')
                if len(val) < 1:
                    raise ValueError('Length of name of port model cannot be zero')
                continue

            if key == 'port_type':
                if val is None:
                    continue
                if type(val) is not PortType:
                    raise TypeError('Port type of port model has to be of type PortModel')
                continue

            raise TypeError("Unexpected attribute '{}' for port model".format(key))

        return kwargs


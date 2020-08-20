#!/bin/env python3

from sqlalchemy import Integer, String
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

#vlans_ports_mapping = Table('vlan_ports', Base.metadata,
#    Column('vlan_id', Integer, ForeignKey('vlans.id')),
#    Column('port_id', Integer, ForeignKey('ports.id'))
#)

class Vlan(Base):
    __tablename__ = 'vlans'
    id = Column(Integer, primary_key = True, nullable = False)

    name = Column('name', String, nullable = False)

    def jsonify(self):
        return { 'id': self.id,
                 'name': self.name }

    def __str__(self):
        return str(self.jsonify())

    def __repr__(self):
        return self.__str__()

class PortModel(Base):
    __tablename__ = 'port_models'
    id = Column(Integer, primary_key = True, nullable = False)
    switch_model_id = Column(Integer, ForeignKey('switch_models.id'), nullable = False)
    port_type_id = Column(Integer, ForeignKey('port_types.description'), nullable = False)

    name = Column("name", String, nullable = False)
    port_type = relationship('PortType', uselist = False)

    def jsonify(self):
        return { 'name': self.name,
                 'port_type': self.port_type }

    def __str__(self):
        return str(self.jsonify())

    def __repr__(self):
        return self.__str__()

class SwitchModel(Base):
    __tablename__ = 'switch_models'
    id = Column(Integer, primary_key = True, nullable = False)

    name = Column('name', String, nullable = False)
    ports = relationship('PortModel', uselist = True)

    def __init__(self, name, ports):
        self.name = name
        self.ports = ports

    def jsonify(self):
        ps = []
        for p in self.ports:
            ps.append(p.jsonify())
        return { 'name': self.name,
                 'ports': ps }

    def __str__(self):
        return str(self.jsonify())

    def __repr__(self):
        return self.__str__()

class PortType(Base):
    __tablename__ = 'port_types'

    description = Column("description", String, primary_key = True, nullable = False)
    speed = Column("speed", Integer, nullable = False)

    def jsonify(self):
        return { 'description': self.description,
                 'speed': self.speed }

    def __str__(self):
        return str(self.jsonify())

    def __repr__(self):
        return self.__str__()

#class Port(Base):
#    __tablename__ = 'ports'
#    id = Column(Integer, primary_key = True, nullable = False)
#    switch_id = Column(Integer, ForeignKey('switches.id'), nullable = False)
#    port_type_id = Column(Integer, ForeignKey('port_types.description'), nullable = False)
#
#    name = Column('name', String, nullable = False)
#    vlans = relationship('Vlan', secondary = vlans_ports_mapping, uselist = True)
#    port_type = relationship('PortType', uselist = False)
#
#    def __init__(self, name, vlans, port_type = None):
#        self.name = name
#        self.vlans = vlans
#        if port_type:
#            self.port_type = port_type
#        else:
#            self.port_type = PortType(description = 'generic', speed = 'fast')
#
#    def jsonify(self):
#        vs = []
#        for v in self.vlans:
#            vs.append(v.jsonify())
#
#        return { 'name': self.name,
#                 'port_type': self.port_type,
#                 'vlans': vs }
#
#    def __str__(self):
#        return str(self.jsonify())
#
#    def __repr__(self):
#        return self.__str__()

class Switch(Base):
    __tablename__ = 'switches'
    id = Column(Integer, primary_key = True, nullable = False)
    model_id = Column(Integer, ForeignKey('switch_models.id'), nullable = False)

    name = Column("name", String, nullable = False)
    location = Column('location', Integer, nullable = False)
    model = relationship('SwitchModel', uselist = False)
    #ports = relationship('Port', uselist = True)

    def __init__(self, name, location, model):
        self.name = name
        self.location = location
        self.model = model
        #self.ports = []
        #for model_port in model.ports:
        #    port = Port(name = model_port.name,
        #                port_type = model_port.port_type,
        #                vlans = [])
        #    self.ports.append(port)

    def jsonify(self):
        #ps = []
        #for p in self.ports:
        #    ps.append(p.jsonify())

        return { 'name': self.name,
                 'location': self.location,
                 'model': self.model.jsonify() }
                 #'ports': ps }

    def __str__(self):
        return str(self.jsonify())

    def __repr__(self):
        return self.__str__()

    def set_port_vlan(port_id, vlan_id):
        if ports[port_id].name != port_id:
            print("something went wrong!")
        pass


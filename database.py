from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from schema import *

class Database:

    engine = create_engine('sqlite:///')
    Base.metadata.create_all(engine)
    Base.metadata.bin = engine
    sessionm = sessionmaker()
    sessionm.configure(bind = engine)
    session = sessionm()

    def __init__(self):
        print('setting up database...')

    def query_switch_models(self, **kwargs):
        # Query
        models = self.session.query(SwitchModel)

        # Filter
        for key, val in kwargs.items():
            if key == 'size':
                if type(val) is not int:
                    raise TypeError('Expected size of switch model to be of type int')
                models = models.filter_by(_size = val)
            else:
                raise TypeError(
                    'Cannot query switch models with unexpected filter "{}"'.format(key))

        return models.all()

    def query_switch_model(self, name):
        model = self.session.query(SwitchModel)
        model = model.filter_by(_name = name)

        if len(model.all()) > 1:
            raise TypeError('DB query resulted in multiple elements but only one was requested')

        return model.first()

    def query_switches(self, **kwargs):
        # Query
        sws = self.session.query(Switch)

        # Filter
        for key, val in kwargs.items():
            if key == 'location':
                if type(val) is not int:
                    raise TypeError('Expected location of switch to be of type int')
                sws = sws.filter_by(_location = val)
            elif key == 'model':
                if type(val) is not str:
                    raise TypeError('Expected model of switch to be of type str')
                sws = sws.filter_by(_model = val)
            else:
                raise TypeError(
                    'Cannot query switches with unexpected filter "{}"'.format(key))

        return sws.all()

    def query_switch(self, name):
        sw = self.session.query(Switch)
        sw = sw.filter_by(_name = name)

        if len(sw.all()) > 1:
            raise TypeError('DB query resulted in multiple elements but only one was requested')

        return sw.first()

    def query_port_types(self, **kwargs):
        # Query
        pts = self.session.query(PortType)

        # Filter
        for key, val in kwargs.items():
            if key == 'speed':
                if type(val) is not int:
                    raise TypeError('Expected speed of port type to be of type int')
                pts = pts.filter_by(speed = val)
            else:
                raise TypeError(
                    'Cannot query port types with unexpected filter "{}"'.format(key))

        return pts.all()

    def query_port_type(self, description):
        pt = self.session.query(PortType)
        pt = pt.filter_by(description = description)

        if len(pt.all()) > 1:
            raise TypeError('DB query resulted in multiple elements but only one was requested')

        return pt.first()

    def query_vlans(self, **kwargs):
        # Query
        vls = self.session.query(Vlan)

        # Filter
        for key, val in kwargs.items():
            if key == 'description':
                if type(val) is not str:
                    raise TypeError('Expected description of vlan to be of type str')
                vls = vls.filter_by(description = val)
            else:
                raise TypeError(
                    'Cannot query port types with unexpected filter "{}"'.format(key))

        return vls.all()

    def query_vlan(self, tag):
        vl = self.session.query(Vlan)

        if tag:
            vl = vl.filter_by(tag = tag)

        if len(vl.all()) > 1:
            raise TypeError('DB query resulted in multiple elements but only one was requested')

        return vl.first()

    def modify_switch_model(self, name, **kwargs):
        # Check switch model
        sm = self.query_switch_model(name)
        if sm is None:
            return None

        # Check all arguments before making any changes
        for key, val in kwargs.items():
            if key == 'ports':
                try:
                    kwargs['ports'] = _port_model_maps_to_dict(val)
                except:
                    return None
            elif key == 'size':
                if type(val) is not int and val is not None:
                    return None
            else:
                raise TypeError(
                    'Cannot modify switch model with unexpected attribute "{}"'.format(key))

        # Apply modifications
        if 'ports' in kwargs:
            sm.ports = kwargs['ports']
        if 'size' in kwargs:
            sm.size = kwargs['size']

        return sm

    def add_switch_model(self, name, ports, size = None):
        # Check all arguments before making any changes
        if type(name) is not str:
            return None

        if self.query_switch_model(name) is not None:
            return None

        if ports is not None:
            try:
                ports = self._port_model_maps_to_dict(ports)
            except:
                return None

        if size is not None:
            if type(size) is not int:
                return None

        swm = SwitchModel(name = name, size = size, ports = ports)
        self.session.add(swm)
        self.session.commit()
        return swm

    def modify_switch(self, name, **kwargs):
        # Check switch
        sw = self.query_switch(name)
        if sw is None:
            return None

        # Check all arguments before making any changes
        for key, val in kwargs.items():
            if key == 'model':
                kwargs['model'] = self.query_switch_model(val)
                if type(kwargs['model']) is not SwitchModel:
                    return None
            elif key == 'port_maps':
                try:
                    kwargs['port_maps'] = _port_maps_to_dict(val)
                except:
                    return None
            elif key == 'location':
                if type(val) is not int:
                    return None
            else:
                raise TypeError(
                    'Cannot modify switch with unexpected attribute "{}"'.format(key))

        # Apply modifications
        if 'model' in kwargs:
            sw.model = kwargs['model']
        if 'port_maps' in kwargs:
            sw.ports = kwargs['port_maps']
        if 'location' in kwargs:
            sw.location = kwargs['location']

        return sw

    def add_switch(self, name, model, port_maps = None, location = None):
        # Check all arguments before making any changes
        if type(name) is not str:
            return None

        if self.query_switch(name) is not None:
            return None

        if type(model) is not str:
            return None
        model = self.query_switch_model(model)
        if model is None:
            return None

        if port_maps is not None:
            try:
                port_maps = self._port_maps_to_dict(port_maps)
            except:
                return None

        # Create switch
        sw = Switch(name = name, model = model, port_maps = port_maps, location = location)

        # Commit to database
        self.session.add(sw)
        self.session.commit()
        return sw

    def modify_port_type(self, description, **kwargs):
        # Check port type
        pt = self.query_port_type(description)
        if pt is None:
            return None

        # Check all arguments before making any changes
        for key, value in kwargs.items():
            if key == 'speed':
                if type(val) is not int:
                    return None
            else:
                raise TypeError(
                    'Cannot modify switch with unexpected attribute "{}"'.format(key))

        # Apply modifications
        if 'speed' in kwargs:
            pt.speed = kwargs['speed']

        return pt

    def add_port_type(self, description = None, speed = None):
        pt = PortType(description = description, speed = speed)
        self.session.add(pt)
        self.session.commit()
        return pt

    def modify_vlan(self, tag, description = None):
        vl = self.query_vlan(tag)
        if not vl:
            return None

        if description:
            if type(description) is not str:
                return None
            vl.description = description

        return vl

    def add_vlan(self, tag = None, description = None):
        vl = Vlan(tag = tag, description = description)
        self.session.add(vl)
        self.session.commit()
        return vl

    def _port_model_maps_to_dict(self, port_maps):
        if type(port_maps) is not list:
            raise TypeError('Given list of port maps is not a list')

        # Unpack port maps
        maps = []
        for port_map in port_maps:
            if type(port_map) is not dict:
                raise TypeError('Given port map is not a dict')
            if 'name' not in port_map:
                raise KeyError('Given port map does not contain key "name"')
            if 'port_type' not in port_map:
                raise KeyError('Given port map does not contain key "port_type"')

            name = port_map['name']
            port_type = self.query_port_type(port_map['port_type'])

            if type(name) is not str:
                raise TypeError('Key "name" of given port map is not of type str')
            if type(port_type) is not PortType:
                raise ValueError('Key "port_type" of given port map contains invalid port type')

            maps.append({ 'name': name, 'port_type': port_type })

        return maps

    def _port_maps_to_dict(self, port_maps):
        if type(port_maps) is not list:
            raise TypeError('Given list of port maps is not a list')

        # Unpack port maps
        maps = []
        for port_map in port_maps:
            if type(port_map) is not dict:
                raise TypeError('Given port map is not a dict')
            if 'name' not in port_map:
                raise KeyError('Given port map does not contain key "name"')
            if 'vlans' not in port_map:
                raise KeyError('Given port map does not contain key "vlans"')

            name = port_map['name']
            vlans = [ self.query_vlan(v) for v in port_map['vlans'] ]

            if type(name) is not str:
                raise TypeError('Key "name" of given port map is not of type str')
            if None in vlans:
                raise ValueError('Key "vlans" of given port map contains invalid vlan')

            maps.append({ 'name': name, 'vlans': vlans })

        return maps

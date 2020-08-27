from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

from schema import *

dbtype = 'sqlite'
dbstr = 'example.db'

# Initialize sqlalchemy scoped sessions for multi thread requests
print('Initializing session registry...')

# Initialize db engine
if dbtype != 'sqlite':
    raise NotImplementedError('Databases other than sqlite are not yet supported')
engine = create_engine('sqlite:///' +dbstr)
Base.metadata.create_all(engine)
Base.metadata.bin = engine

# Initialize scoped sessions to support multi thread access to database
sessionm = sessionmaker(bind = engine)
Session = scoped_session(sessionm)

class DatabaseConnection:
    def query_switch_model(self, name):
        if type(name) is not str:
            raise TypeError('Given parameter "name" is not of expected type str')

        session = Session()
        model = session.query(SwitchModel)
        model = model.filter_by(_name = name)

        if len(model.all()) > 1:
            raise TypeError('DB query resulted in multiple elements but only one was requested')

        return model.first()

    def query_switch(self, name):
        if type(name) is not str:
            raise TypeError('Given parameter "name" is not of expected type str')

        session = Session()
        sw = session.query(Switch)
        sw = sw.filter_by(_name = name)

        if len(sw.all()) > 1:
            raise TypeError('DB query resulted in multiple elements but only one was requested')

        return sw.first()

    def query_port_type(self, description):
        if type(description) is not str:
            raise TypeError('Given parameter "description" is not of expected type str')

        session = Session()
        pt = session.query(PortType)
        pt = pt.filter_by(description = description)

        if len(pt.all()) > 1:
            raise TypeError('DB query resulted in multiple elements but only one was requested')

        return pt.first()

    def query_vlan(self, tag):
        if type(tag) is not int:
            raise TypeError('Given parameter "tag" is not of expected type int')

        session = Session()
        vl = session.query(Vlan)
        vl = vl.filter_by(tag = tag)

        if len(vl.all()) > 1:
            raise TypeError('DB query resulted in multiple elements but only one was requested')

        return vl.first()

    def query_switch_models(self, **kwargs):
        # Query
        session = Session()
        models = session.query(SwitchModel)

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

    def query_switches(self, **kwargs):
        # Query
        session = Session()
        sws = session.query(Switch)

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

    def query_port_types(self, **kwargs):
        # Query
        session = Session()
        pts = session.query(PortType)

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

    def query_vlans(self, **kwargs):
        # Query
        session = Session()
        vls = session.query(Vlan)

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

    def modify_switch_model(self, name, **kwargs):
        # Check switch model
        sm = self.query_switch_model(name)
        if sm is None:
            raise ValueError('Given switch model does not exist')

        # Check all arguments before making any changes
        for key, val in kwargs.items():
            if key == 'ports':
                try:
                    kwargs['ports'] = _port_models_to_dict(val)
                except:
                    raise ValueError('Given list of ports of switch model is malformed')
            elif key == 'size':
                if type(val) is not int and val is not None:
                    raise TypeError('Given size of switch model is not of type int')
            else:
                raise TypeError(
                    'Cannot modify switch model with unexpected attribute "{}"'.format(key))

        # Apply modifications
        if 'ports' in kwargs:
            sm.ports = kwargs['ports']
        if 'size' in kwargs:
            sm.size = kwargs['size']

        return sm

    def modify_switch(self, name, **kwargs):
        # Check switch
        sw = self.query_switch(name)
        if sw is None:
            raise ValueError('Given switch does not exist')

        # Check all arguments before making any changes
        for key, val in kwargs.items():
            if key == 'model':
                kwargs['model'] = self.query_switch_model(val)
                if kwargs['model'] is None:
                    raise ValueError('Given switch model of switch does not exist')
            elif key == 'ports':
                try:
                    kwargs['ports'] = self._ports_to_dict(val)
                except:
                    raise ValueError('Given list of ports of switch is malformed')
            elif key == 'location':
                if type(val) is not int:
                    raise TypeError('Given location of switch is not of type int')
            else:
                raise TypeError(
                    'Cannot modify switch with unexpected attribute "{}"'.format(key))

        # Apply modifications
        if 'model' in kwargs:
            sw.model = kwargs['model']
        if 'ports' in kwargs:
            sw.ports = kwargs['ports']
        if 'location' in kwargs:
            sw.location = kwargs['location']

        return sw

    def modify_port_type(self, description, **kwargs):
        # Check port type
        pt = self.query_port_type(description)
        if pt is None:
            raise ValueError('Given port type does not exist')

        # Check all arguments before making any changes
        for key, value in kwargs.items():
            if key == 'speed':
                if type(val) is not int:
                    raise TypeError('Given speed of port type is not of type int')
            else:
                raise TypeError(
                    'Cannot modify switch with unexpected attribute "{}"'.format(key))

        # Apply modifications
        if 'speed' in kwargs:
            pt.speed = kwargs['speed']

        return pt

    def modify_vlan(self, tag, **kwargs):
        # Check if vlan already exists
        vl = self.query_vlan(tag)
        if vl is None:
            raise ValueError('Given VLAN does not exist')

        # Check all arguments before making any changes
        for key, val in kwargs.items():
            if key == 'description':
                if type(val) is not str:
                    raise TypeError('Given description of VLAN is not of type str')
            else:
                raise TypeError(
                    'Cannot modify vlan with unexpeceted attribute "{}"'.format(key))

        # Apply modifications
        if 'description' in kwargs:
            vl.description = kwargs['description']

        return vl

    def add_switch_model(self, **kwargs):
        # Check if switch model already exists
        if 'name' not in kwargs:
            raise KeyError('Missing necessary argument "name" for adding switch model')
        if self.query_switch_model(kwargs['name']) is not None:
            raise ValueError(
                'Cannot add switch model with name {} - switch model already exists'
                .format(kwargs['name']))

        # Check all arguments before making any changes
        for key, val in kwargs.items():
            if key == 'name':
                pass
            elif key == 'ports':
                try:
                    kwargs['ports'] = self._port_models_to_dict(val)
                except:
                    raise ValueError('Given list of ports of switch model is malformed')
            elif key == 'size':
                pass
            else:
                raise TypeError(
                    'Cannot add switch model with unexpected attribute "{}"'.format(key))

        # Create switch model
        swm = SwitchModel(**kwargs)
        session = Session()
        session.add(swm)
        session.commit()
        return swm

    def add_switch(self, **kwargs):
        # Check if switch already exists
        if 'name' not in kwargs:
            raise KeyError('Missing necessary argument "name" for adding switch')
        if self.query_switch(kwargs['name']) is not None:
            raise ValueError(
                'Cannot add switch with name {} - switch already exists'
                .format(kwargs['name']))

        # Check all arguments before making any changes
        for key, val in kwargs.items():
            if key == 'name':
                pass
            elif key == 'model':
                kwargs['model'] = self.query_switch_model(val)
                if kwargs['model'] is None:
                    raise ValueError(
                        'Cannot add switch with switch model {} - switch model does not exist'
                        .format(val))
            elif key == 'ports':
                try:
                    kwargs['ports'] = self._ports_to_dict(val)
                except:
                    raise ValueError('Given list of ports of switch is malformed')
            elif key == 'location':
                pass
            else:
                raise TypeError(
                    'Cannot create switch with unexpected attribute "{}"'.format(key))

        # Create switch
        sw = Switch(**kwargs)
        session = Session()
        session.add(sw)
        session.commit()
        return sw

    def add_port_type(self, **kwargs):
        # Check if port type already exists
        if 'description' not in kwargs:
            raise KeyError('Missing necessary argument "description" for adding port type')
        if self.query_port_type(kwargs['description']) is not None:
            raise ValueError(
                'Cannot add port type with description {} - port type already exists'
                .format(kwargs['description']))

        # Check all arguments before making any changes
        for key, val in kwargs.items():
            if key == 'description':
                pass
            elif key == 'speed':
                pass
            else:
                raise TypeError(
                    'Cannot create port type with unexpected attribute "{}"'.format(key))

        # Add port type
        pt = PortType(**kwargs)
        session = Session()
        session.add(pt)
        session.commit()
        return pt

    def add_vlan(self, **kwargs):
        # Check if vlan already exists
        if 'tag' not in kwargs:
            raise KeyError('Missing necessary argument "tag" for adding vlan')
        if self.query_vlan(kwargs['tag']) is not None:
            raise ValueError(
                'Cannot add vlan with tag {} - vlan already exists'
                .format(kwargs['tag']))


        # Check all arguments before making any changes
        for key, val in kwargs.items():
            if key == 'tag':
                pass
            elif key == 'description':
                pass
            else:
                raise TypeError(
                    'Cannot add vlan with unexpected attribute "{}"'.format(key))

        # Add vlan
        vl = Vlan(**kwargs)
        session = Session()
        session.add(vl)
        session.commit()
        return vl

    def _port_models_to_dict(self, ports):
        if type(ports) is not list:
            raise TypeError('Given list of ports is not a list')

        # Unpack ports
        maps = []
        for port in ports:
            if type(port) is not dict:
                raise TypeError('Given port map is not a dict')
            if 'name' not in port:
                raise KeyError('Given port map does not contain key "name"')
            if 'port_type' not in port:
                raise KeyError('Given port map does not contain key "port_type"')

            name = port['name']
            port_type = self.query_port_type(port['port_type'])

            if type(name) is not str:
                raise TypeError('Element "name" of given port map is not of type str')
            if type(port_type) is not PortType:
                raise ValueError('Element "port_type" of given port map contains invalid port type')

            maps.append({ 'name': name, 'port_type': port_type })

        return maps

    def _ports_to_dict(self, ports):
        if type(ports) is not list:
            raise TypeError('Given list of port is not a list')

        # Unpack ports
        maps = []
        for port in ports:
            if type(port) is not dict:
                raise TypeError('Given port map is not a dict')
            if 'name' not in port:
                raise KeyError('Given port map does not contain key "name"')
            if 'vlans' not in port:
                raise KeyError('Given port map does not contain key "vlans"')

            name = port['name']
            vlans = [ self.query_vlan(v) for v in port['vlans'] ]

            if type(name) is not str:
                raise TypeError('Element "name" of given port map is not of type str')
            if None in vlans:
                raise ValueError('Element "vlans" of given port map contains invalid vlan')

            maps.append({ 'name': name, 'vlans': vlans })

        return maps

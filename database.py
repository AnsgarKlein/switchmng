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
    def query_switch_model(self, resource_id):
        if type(resource_id) is not str:
            raise TypeError('Cannot query switch model with resource id not of type str')

        session = Session()
        model = session.query(SwitchModel)
        model = model.filter_by(_name = resource_id)

        if len(model.all()) > 1:
            raise TypeError('DB query resulted in multiple elements but only one was requested')

        return model.first()

    def query_switch(self, resource_id):
        if type(resource_id) is not str:
            raise TypeError('Cannot query switch with resource id not of type str')

        session = Session()
        sw = session.query(Switch)
        sw = sw.filter_by(_name = resource_id)

        if len(sw.all()) > 1:
            raise TypeError('DB query resulted in multiple elements but only one was requested')

        return sw.first()

    def query_port_type(self, resource_id):
        if type(resource_id) is not str:
            raise TypeError('Cannot query port type with resource id not of type str')

        session = Session()
        pt = session.query(PortType)
        pt = pt.filter_by(description = resource_id)

        if len(pt.all()) > 1:
            raise TypeError('DB query resulted in multiple elements but only one was requested')

        return pt.first()

    def query_vlan(self, resource_id):
        if type(resource_id) is not int:
            raise TypeError('Cannot query vlan with resource id not of type int')

        session = Session()
        vl = session.query(Vlan)
        vl = vl.filter_by(tag = resource_id)

        if len(vl.all()) > 1:
            raise TypeError('DB query resulted in multiple elements but only one was requested')

        return vl.first()

    def query_switch_models(self, **kwargs):
        # Query
        session = Session()
        models = session.query(SwitchModel)

        # Filter with SQL
        for key, val in kwargs.items():
            if key == 'size':
                if type(val) is not int:
                    raise TypeError('Given size of switch model is not of type int')
                models = models.filter_by(_size = val)
            elif key == 'port_type':
                if type(val) is not str:
                    raise TypeError('Given port type of port of switch model is not of type str')
                val = self.query_port_type(val)
                if val is None:
                    raise ValueError('Given port type does not exist')
            else:
                raise TypeError(
                    'Cannot query switch models with unexpected filter "{}"'.format(key))

        models = models.all()

        # TODO: When querying switch models don't filter manually but let database do the work

        # Filter manually
        for key, val in kwargs.items():
            if key == 'size':
                pass
            elif key == 'port_type':
                new_models = list()
                pt = val
                for model in models:
                    for port in model.ports:
                        if port['port_type'] == pt:
                            new_models.append(model)
                            break
                models = new_models
            else:
                raise TypeError(
                    'Cannot query switch models with unexpected filter "{}"'.format(key))

        return models

    def query_switches(self, **kwargs):
        # Query
        session = Session()
        switches = session.query(Switch)

        # Filter with SQL
        for key, val in kwargs.items():
            if key == 'location':
                if type(val) is not int:
                    raise TypeError('Given location of switch is not of type int')
                switches = switches.filter_by(_location = val)
            elif key == 'model':
                kwargs['model'] = self.query_switch_model(val)
                if kwargs['model'] is None:
                    raise ValueError(
                        'Got invalid switch model "{}" - switch model does not exist')
                switches = switches.filter_by(_model = kwargs['model'])
            elif key == 'vlan':
                if type(val) is not int:
                    raise TypeError('Given vlan of port of switch is not of type int')
            else:
                raise TypeError(
                    'Cannot query switches with unexpected filter "{}"'.format(key))

        switches = switches.all()

        # TODO: When querying switches don't filter manually but let database do the work

        # Filter manually
        print('filtering manually...')
        for key, val in kwargs.items():
            if key == 'location':
                pass
            elif key == 'model':
                pass
            elif key == 'vlan':
                new_switches = list()
                vl = val
                for switch in switches:
                    for port in switch.ports:
                        if vl in port['vlans']:
                            new_switches.append(switch)
                            break
                switches = new_switches
            else:
                raise TypeError(
                    'Cannot query switches with unexpected filter "{}"'.format(key))

        print('done filtering')


        return switches

    def query_port_types(self, **kwargs):
        # Query
        session = Session()
        pts = session.query(PortType)

        # Filter
        for key, val in kwargs.items():
            if key == 'speed':
                if type(val) is not int:
                    raise TypeError('Given speed of port type is not of type int')
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
                    raise TypeError('Given description of vlan is not of type str')
                vls = vls.filter_by(description = val)
            else:
                raise TypeError(
                    'Cannot query port types with unexpected filter "{}"'.format(key))

        return vls.all()

    def delete_switch_model(self, resource_id):
        # Check switch model
        sm = self.query_switch_model(resource_id)
        if sm is None:
            raise ValueError('Given switch model does not exist')

        # Check if there are switches still using this model
        affected_sw = self.query_switches(model = resource_id)
        if type(affected_sw) is not list:
            raise TypeError('Expected list of switches to be of type list')
        if len(affected_sw) > 0:
            raise ValueError('Given switch model is still in use')

        # Delete switch model
        session = Session()
        session.delete(sm)
        session.commit()

    def delete_switch(self, resource_id):
        # Check switch
        sw = self.query_switch(resource_id)
        if sw is None:
            raise ValueError('Given switch does not exist')

        # Delete switch
        session = Session()
        session.delete(sw)
        session.commit()

    def delete_port_type(self, resource_id):
        # Check port type
        pt = self.query_port_type(resource_id)
        if pt is None:
            raise ValueError('Given port type does not exist')

        # Check if there are switch models still using this port type
        affected_sm = self.query_switch_models(port_type = resource_id)
        if type(affected_sm) is not list:
            raise TypeError('Expected list of switch models to be of type list')
        if len(affected_sm) > 0:
            raise ValueError('Given port type is still in use')

        # Delete port type
        session = Session()
        session.delete(pt)
        session.commit()

    def delete_vlan(self, resource_id):
        # Check vlan
        vl = self.query_vlan(resource_id)
        if vl is None:
            raise ValueError('Given vlan does not exist')

        # Check if there are switch ports still using this vlan
        affected_sw = self.query_switches(vlan = resource_id)
        if type(affected_sw) is not list:
            raise TypeError('Expected list of switches to be of type list')
        if len(affected_sw) > 0:
            raise ValueError('Given vlan is still in use')

        # Delete vlan
        session = Session()
        session.delete(vl)
        session.commit()

    def modify_switch_model(self, resource_id, **kwargs):
        # Check all arguments before making any changes
        kwargs = self._check_switch_model_parameters(**kwargs)

        # Check switch model
        sm = self.query_switch_model(resource_id)
        if sm is None:
            raise ValueError('Given switch model does not exist')

        # Apply modifications
        for key, val in kwargs.items():
            setattr(sm, key, val)

        session = Session()
        session.add(sm)
        session.commit()

        return sm

    def modify_switch(self, resource_id, **kwargs):
        # Check all arguments before making any changes
        kwargs = self._check_switch_parameters(**kwargs)

        # Check if switch does not exists
        sw = self.query_switch(resource_id)
        if sw is None:
            raise ValueError('Given switch "{}" does not exist'
                .format(resource_id))

        # Apply modifications
        for key, val in kwargs.items():
            setattr(sw, key, val)

        session = Session()
        session.add(sw)
        session.commit()

        return sw

    def modify_port_type(self, resource_id, **kwargs):
        # Check all arguments before making any changes
        kwargs = self._check_port_type_parameters(**kwargs)

        # Check port type
        pt = self.query_port_type(resource_id)
        if pt is None:
            raise ValueError('Given port type does not exist')

        # Apply modifications
        for key, val in kwargs.items():
            setattr(pt, key, val)

        session = Session()
        session.add(pt)
        session.commit()

        return pt

    def modify_vlan(self, resource_id, **kwargs):
        # Check all arguments before making any changes
        kwargs = self._check_vlan_parameters(**kwargs)

        # Check if vlan already exists
        vl = self.query_vlan(resource_id)
        if vl is None:
            raise ValueError('Given VLAN does not exist')

        # Apply modifications
        for key, val in kwargs.items():
            setattr(vl, key, val)

        session = Session()
        session.add(vl)
        session.commit()

        return vl

    def set_switch_model(self, resource_id, **kwargs):
        # Check all arguments before making any changes
        kwargs = self._check_switch_model_parameters(**kwargs)

        # Check if switch model exists
        source_sm = self.query_switch_model(resource_id)

        if source_sm is None:
            # Source switch model does not exist:
            #  We are creating a new switch model

            # Switch model name is either resource specifier or not set at all
            # (in which case it will be set automatically)
            if 'name' in kwargs:
                if kwargs['name'] != resource_id:
                    raise ValueError('Resource identifier "name" of switch model is ambiguous')
            else:
                kwargs.update({'name': resource_id})

            target_sm = SwitchModel(**kwargs)
            session = Session()
            session.add(target_sm)
            session.commit()
            return target_sm
        else:
            # Source switch model exists

            # Source switch model exists so target switch model must not also exist
            if 'name' not in kwargs:
                raise KeyError('Missing necessary argument "name" for setting switch model')
            if resource_id != kwargs['name']:
                if self.query_switch(kwargs['name']) is not None:
                    raise ValueError(
                        'Cannot set switch model with name {} - switch model already exists'
                        .format(kwargs['name']))

            # Create new switch model object with given state
            # and replace old object with it
            target_sm = SwitchModel(**kwargs)

            session = Session()
            session.delete(source_sm)
            session.flush()
            session.add(target_sm)
            session.commit()
            return target_sm

    def set_switch(self, resource_id, **kwargs):
        # Check all arguments before making any changes
        kwargs = self._check_switch_parameters(**kwargs)

        # Check if switch exists
        source_sw = self.query_switch(resource_id)

        if source_sw is None:
            # Source switch does not exist:
            #  We are creating a new switch

            # Switch name is either resource specifier or not set at all
            # (in which case it will be set automatically)
            if 'name' in kwargs:
                if kwargs['name'] != resource_id:
                    raise ValueError('Resource identifier "name" of switch is ambiguous')
            else:
                kwargs.update({'name': resource_id})

            target_sw = Switch(**kwargs)
            session = Session()
            session.add(target_sw)
            session.commit()
            return target_sw
        else:
            # Source switch exists

            # Source switch exists so target switch must not also exist
            if 'name' not in kwargs:
                raise KeyError('Missing necessary argument "name" for setting switch')
            if resource_id != kwargs['name']:
                if self.query_switch(kwargs['name']) is not None:
                    raise ValueError(
                        'Cannot set switch with name {} - switch already exists'
                        .format(kwargs['name']))

            # Create new switch object with given state
            # and replace old object with it
            target_sw = Switch(**kwargs)

            session = Session()
            session.delete(source_sw)
            session.flush()
            session.add(target_sw)
            session.commit()
            return target_sw

    def set_port_type(self, resource_id, **kwargs):
        # Check all arguments before making any changes
        kwargs = self._check_port_type_parameters(**kwargs)

        # Check if source port type exists
        source_pt = self.query_port_type(resource_id)

        if source_pt is None:
            # Source port type does not exist:
            #  We are creating a new port type

            # Port type description is either resource specifier or not set at
            # all (in which case it will be set automatically)
            if 'description' in kwargs:
                if kwargs['description'] != resource_id:
                    raise ValueError('Resource identifier "description" of port type is ambiguous')
            else:
                kwargs.update({'description': resource_id})

            target_pt = PortType(**kwargs)
            session = Session()
            session.add(target_pt)
            session.commit()
            return target_pt
        else:
            # Source port type exists

            # Source port type exists so target port type must not also exist
            if 'description' not in kwargs:
                raise KeyError('Missing necessary argument "description" for setting port type')
            if resource_id != kwargs['description']:
                if self.query_port_type(kwargs['description']) is not None:
                    raise ValueError(
                        'Cannot set port type with description {} - port type already exists'
                        .format(kwargs['description']))

            # Create a new port type object with given state
            # and replace old object with it
            target_pt  = PortType(**kwargs)

            session = Session()
            session.delete(source_pt)
            session.flush()
            session.add(target_pt)
            session.commit()
            return target_pt

    def set_vlan(self, resource_id, **kwargs):
        # Check all arguments before making any changes
        kwargs = self._check_vlan_parameters(**kwargs)

        # Check if source vlan exists
        source_vl = self.query_vlan(resource_id)

        print('source vlan: {}'.format(source_vl))

        if source_vl is None:
            # Source vlan does not exist:
            #  We are creating a new vlan

            # Vlan tag is either resource specifier or not set at all
            # (in which case it will be set automatically)
            if 'tag' in kwargs:
                if kwargs['tag'] != resource_id:
                    raise ValueError('Resource identifier "tag" of vlan is ambiguous')
            else:
                kwargs.update({'tag': resource_id})

            target_vl = Vlan(**kwargs)
            session = Session()
            session.add(target_vl)
            session.commit()
            return target_vl
        else:
            # Source vlan exists

            # Source vlan exists so target vlan must not also exist
            if 'tag' not in kwargs:
                raise KeyError('Missing necessary argument "tag" for setting vlan')
            if resource_id != kwargs['tag']:
                if self.query_vlan(kwargs['tag']) is not None:
                    raise ValueError(
                        'Cannot set vlan with tag {} - vlan already exists'
                        .format(kwargs['tag']))

            # Create a new vlan object with given state
            # and replace old object with it
            target_vl = Vlan(**kwargs)

            session = Session()
            session.delete(source_vl)
            session.flush()
            session.add(target_vl)
            session.commit()
            return target_vl

    def add_switch_model(self, **kwargs):
        # Check all arguments before making any changes
        kwargs = self._check_switch_model_parameters(**kwargs)

        # Check if switch model already exists
        if 'name' not in kwargs:
            raise KeyError('Missing necessary argument "name" for adding switch model')
        if self.query_switch_model(kwargs['name']) is not None:
            raise ValueError(
                'Cannot add switch model with name {} - switch model already exists'
                .format(kwargs['name']))

        # Create switch model
        sm = SwitchModel(**kwargs)
        session = Session()
        session.add(sm)
        session.commit()
        return sm

    def add_switch(self, **kwargs):
        # Check all arguments before making any changes
        kwargs = self._check_switch_parameters(**kwargs)

        # Check if switch already exists
        if 'name' not in kwargs:
            raise KeyError('Missing necessary argument "name" for adding switch')
        if self.query_switch(kwargs['name']) is not None:
            raise ValueError(
                'Cannot add switch with name {} - switch already exists'
                .format(kwargs['name']))

        # Create switch
        sw = Switch(**kwargs)
        session = Session()
        session.add(sw)
        session.commit()
        return sw

    def add_port_type(self, **kwargs):
        # Check all arguments before making any changes
        kwargs = self._check_port_type_parameters(**kwargs)

        # Check if port type already exists
        if 'description' not in kwargs:
            raise KeyError('Missing necessary argument "description" for adding port type')
        if self.query_port_type(kwargs['description']) is not None:
            raise ValueError(
                'Cannot add port type with description {} - port type already exists'
                .format(kwargs['description']))

        # Add port type
        pt = PortType(**kwargs)
        session = Session()
        session.add(pt)
        session.commit()
        return pt

    def add_vlan(self, **kwargs):
        # Check all arguments before making any changes
        kwargs = self._check_vlan_parameters(**kwargs)

        # Check if vlan already exists
        if 'tag' not in kwargs:
            raise KeyError('Missing necessary argument "tag" for adding vlan')
        if self.query_vlan(kwargs['tag']) is not None:
            raise ValueError(
                'Cannot add vlan with tag {} - vlan already exists'
                .format(kwargs['tag']))

        # Add vlan
        vl = Vlan(**kwargs)
        session = Session()
        session.add(vl)
        session.commit()
        return vl

    def _check_switch_model_parameters(self, **kwargs):
        for key, val in kwargs.items():
            if key == 'name':
                if type(val) is not str:
                    raise TypeError('Given name of switch model is not of type str')
            elif key == 'ports':
                try:
                    kwargs['ports'] = self._port_models_to_dict(val)
                except:
                    raise ValueError('Given list of ports of switch model is malformed')
            elif key == 'size':
                if type(val) is not int:
                    raise TypeError('Given size of switch model is not of type int')
            else:
                raise TypeError(
                    'Unexpected attribute "{}" for switch model'.format(key))

        return kwargs

    def _check_switch_parameters(self, **kwargs):
        for key, val in kwargs.items():
            if key == 'name':
                if type(val) is not str:
                    raise TypeError('Given name of switch is not of type str')
            elif key == 'model':
                kwargs['model'] = self.query_switch_model(val)
                if kwargs['model'] is None:
                    raise ValueError(
                        'Got invalid switch model "{}" - switch model does not exist'
                        .format(val))
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
                    'Unexpected attribute "{}" for switch'.format(key))

        return kwargs

    def _check_port_type_parameters(self, **kwargs):
        for key, val in kwargs.items():
            if key == 'description':
                if type(val) is not str:
                    raise TypeError('Given description of port type is not of type str')
            elif key == 'speed':
                if type(val) is not int:
                    raise TypeError('Given speed of port type is not of type int')
            else:
                raise TypeError(
                    'Unexpected attribute "{}" for port type'.format(key))

        return kwargs

    def _check_vlan_parameters(self, **kwargs):
        for key, val in kwargs.items():
            if key == 'tag':
                if type(val) is not int:
                    raise TypeError('Given tag of vlan is not of type int')
            elif key == 'description':
                if type(val) is not str:
                    raise TypeError('Given description of vlan is not of type str')
            else:
                raise TypeError(
                    'Unexpected attribute "{}" for VLAN'.format(key))

        return kwargs

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

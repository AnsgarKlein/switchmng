from . import *

def query_switch_model(resource_id):
    if type(resource_id) is not str:
        raise TypeError('Cannot query switch model with resource id not of type str')

    session = Session()
    model = session.query(SwitchModel)
    model = model.filter_by(_name = resource_id)

    if len(model.all()) > 1:
        raise TypeError('DB query resulted in multiple elements but only one was requested')

    return model.first()

def query_switch(resource_id):
    if type(resource_id) is not str:
        raise TypeError('Cannot query switch with resource id not of type str')

    session = Session()
    sw = session.query(Switch)
    sw = sw.filter_by(_name = resource_id)

    if len(sw.all()) > 1:
        raise TypeError('DB query resulted in multiple elements but only one was requested')

    return sw.first()

def query_port_type(resource_id):
    if type(resource_id) is not str:
        raise TypeError('Cannot query port type with resource id not of type str')

    session = Session()
    pt = session.query(PortType)
    pt = pt.filter_by(_description = resource_id)

    if len(pt.all()) > 1:
        raise TypeError('DB query resulted in multiple elements but only one was requested')

    return pt.first()

def query_vlan(resource_id):
    if type(resource_id) is not int:
        raise TypeError('Cannot query vlan with resource id not of type int')

    session = Session()
    vl = session.query(Vlan)
    vl = vl.filter_by(_tag = resource_id)

    if len(vl.all()) > 1:
        raise TypeError('DB query resulted in multiple elements but only one was requested')

    return vl.first()

def query_switch_models(**kwargs):
    # Check all arguments before querying
    SwitchModel.check_params(**kwargs)

    # Query
    session = Session()
    models = session.query(SwitchModel)

    # Filter with SQL
    for key, val in kwargs.items():
        if key == 'size':
            models = models.filter_by(_size = val)
        elif key == 'port_type':
            val = query_port_type(val)
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

def query_switches(**kwargs):
    # Check all arguments before querying
    Switch.check_params(**kwargs)

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
            kwargs['model'] = query_switch_model(val)
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

    return switches

def query_port_types(**kwargs):
    # Check all arguments before querying
    PortType.check_params(**kwargs)

    # Query
    session = Session()
    pts = session.query(PortType)

    # Filter
    for key, val in kwargs.items():
        if key == 'speed':
            pts = pts.filter_by(_speed = val)
        else:
            raise TypeError(
                'Cannot query port types with unexpected filter "{}"'.format(key))

    return pts.all()

def query_vlans(**kwargs):
    # Check all arguments before querying
    Vlan.check_params(**kwargs)

    # Query
    session = Session()
    vls = session.query(Vlan)

    # Filter
    for key, val in kwargs.items():
        if key == 'description':
            vls = vls.filter_by(_description = val)
        else:
            raise TypeError(
                'Cannot query port types with unexpected filter "{}"'.format(key))

    return vls.all()


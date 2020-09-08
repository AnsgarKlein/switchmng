from . import *
from .helper import *

def modify_switch_model(resource_id, **kwargs):
    # Check if switch model exists
    sm = query_switch_model(resource_id)
    if sm is None:
        raise ValueError('Given switch model does not exist')

    # Replace list of ports with list of port objects
    if 'ports' in kwargs:
        kwargs['ports'] = ports_models_from_dict(kwargs['ports'])

    # Check all arguments before making any changes
    kwargs = SwitchModel.check_params(**kwargs)

    # Apply modifications
    if 'ports' in kwargs:
        ports = kwargs.pop('ports')
        sm.modify_ports(ports)
    for key, val in kwargs.items():
        setattr(sm, key, val)

    session = Session()
    session.add(sm)
    session.commit()

    return sm

def modify_switch(resource_id, **kwargs):
    # Check if switch exists
    sw = query_switch(resource_id)
    if sw is None:
        raise ValueError('Given switch "{}" does not exist'
            .format(resource_id))

    # Replace list of ports with list of port objects
    if 'ports' in kwargs:
        kwargs['ports'] = ports_from_dict(kwargs['ports'])

    # Replace switch model string with switch model object
    if 'model' in kwargs:
        kwargs['model'] = query_switch_model(kwargs['model'])

    # Check all arguments before making any changes
    Switch.check_params(**kwargs)

    # Apply modifications
    if 'ports' in kwargs:
        ports = kwargs.pop('ports')
        sw.modify_ports(ports)
    for key, val in kwargs.items():
        setattr(sw, key, val)

    session = Session()
    session.add(sw)
    session.commit()

    return sw

def modify_port_type(resource_id, **kwargs):
    # Check if port type exists
    pt = query_port_type(resource_id)
    if pt is None:
        raise ValueError('Given port type does not exist')

    # Check all arguments before making any changes
    kwargs = PortType.check_params(**kwargs)

    # Apply modifications
    for key, val in kwargs.items():
        setattr(pt, key, val)

    session = Session()
    session.add(pt)
    session.commit()

    return pt

def modify_vlan(resource_id, **kwargs):
    # Check if vlan exists
    vl = query_vlan(resource_id)
    if vl is None:
        raise ValueError('Given VLAN does not exist')

    # Check all arguments before making any changes
    kwargs = Vlan.check_params(**kwargs)

    # Apply modifications
    for key, val in kwargs.items():
        setattr(vl, key, val)

    session = Session()
    session.add(vl)
    session.commit()

    return vl


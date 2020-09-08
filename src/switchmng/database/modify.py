from . import *
from .helper import *

def modify_switch_model(resource_id, **kwargs):
    # Check all arguments before making any changes
    kwargs = check_switch_model_parameters(**kwargs)

    # Check switch model
    sm = query_switch_model(resource_id)
    if sm is None:
        raise ValueError('Given switch model does not exist')

    # Apply modifications
    for key, val in kwargs.items():
        setattr(sm, key, val)

    session = Session()
    session.add(sm)
    session.commit()

    return sm

def modify_switch(resource_id, **kwargs):
    # Check all arguments before making any changes
    kwargs = check_switch_parameters(**kwargs)

    # Check if switch does not exists
    sw = query_switch(resource_id)
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

def modify_port_type(resource_id, **kwargs):
    # Check all arguments before making any changes
    kwargs = check_port_type_parameters(**kwargs)

    # Check port type
    pt = query_port_type(resource_id)
    if pt is None:
        raise ValueError('Given port type does not exist')

    # Apply modifications
    for key, val in kwargs.items():
        setattr(pt, key, val)

    session = Session()
    session.add(pt)
    session.commit()

    return pt

def modify_vlan(resource_id, **kwargs):
    # Check all arguments before making any changes
    kwargs = check_vlan_parameters(**kwargs)

    # Check if vlan already exists
    vl = query_vlan(resource_id)
    if vl is None:
        raise ValueError('Given VLAN does not exist')

    # Apply modifications
    for key, val in kwargs.items():
        setattr(vl, key, val)

    session = Session()
    session.add(vl)
    session.commit()

    return vl



from . import *
from .helper import *

def add_switch_model(**kwargs):
    # Check if switch model already exists
    if 'name' not in kwargs:
        raise KeyError('Missing necessary argument "name" for adding switch model')
    if query_switch_model(kwargs['name']) is not None:
        raise ValueError(
            'Cannot add switch model with name {} - switch model already exists'
            .format(kwargs['name']))

    # Replace list of port strings with list of port objects
    if 'ports' in kwargs:
        kwargs['ports'] = port_models_from_dict(kwargs['ports'])

    # Create switch model
    sm = SwitchModel(**kwargs)
    session = Session()
    session.add(sm)
    session.commit()
    return sm

def add_switch(**kwargs):
    # Check if switch already exists
    if 'name' not in kwargs:
        raise KeyError('Missing necessary argument "name" for adding switch')
    if query_switch(kwargs['name']) is not None:
        raise ValueError(
            'Cannot add switch with name {} - switch already exists'
            .format(kwargs['name']))

    # Replace list of port strings with list of port objects
    if 'ports' in kwargs:
        kwargs['ports'] = ports_from_dict(kwargs['ports'])

    # Replace switch model string with switch model object
    if 'model' in kwargs:
        kwargs['model'] = query_switch_model(kwargs['model'])

    # Create switch
    sw = Switch(**kwargs)
    session = Session()
    session.add(sw)
    session.commit()
    return sw

def add_port_type(**kwargs):
    # Check if port type already exists
    if 'description' not in kwargs:
        raise KeyError('Missing necessary argument "description" for adding port type')
    if query_port_type(kwargs['description']) is not None:
        raise ValueError(
            'Cannot add port type with description {} - port type already exists'
            .format(kwargs['description']))

    # Add port type
    pt = PortType(**kwargs)
    session = Session()
    session.add(pt)
    session.commit()
    return pt

def add_vlan(**kwargs):
    # Check if vlan already exists
    if 'tag' not in kwargs:
        raise KeyError('Missing necessary argument "tag" for adding vlan')
    if query_vlan(kwargs['tag']) is not None:
        raise ValueError(
            'Cannot add vlan with tag {} - vlan already exists'
            .format(kwargs['tag']))

    # Add vlan
    vl = Vlan(**kwargs)
    session = Session()
    session.add(vl)
    session.commit()
    return vl


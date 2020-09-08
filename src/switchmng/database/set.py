from . import *
from .helper import *

def set_switch_model(resource_id, **kwargs):
    # Check all arguments before making any changes
    kwargs = check_switch_model_parameters(**kwargs)

    # Check if switch model exists
    source_sm = query_switch_model(resource_id)

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
            if query_switch(kwargs['name']) is not None:
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

def set_switch(resource_id, **kwargs):
    # Check all arguments before making any changes
    kwargs = check_switch_parameters(**kwargs)

    # Check if switch exists
    source_sw = query_switch(resource_id)

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
            if query_switch(kwargs['name']) is not None:
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

def set_port_type(resource_id, **kwargs):
    # Check all arguments before making any changes
    kwargs = check_port_type_parameters(**kwargs)

    # Check if source port type exists
    source_pt = query_port_type(resource_id)

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
            if query_port_type(kwargs['description']) is not None:
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

def set_vlan(resource_id, **kwargs):
    # Check all arguments before making any changes
    kwargs = check_vlan_parameters(**kwargs)

    # Check if source vlan exists
    source_vl = query_vlan(resource_id)

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
            if query_vlan(kwargs['tag']) is not None:
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



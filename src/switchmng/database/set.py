from . import *

def set_switch_model(session, resource_id, **kwargs):
    """
    Set a :class:`SwitchModel` corresponding to a given resource identifier
    to a given state.

    :class:`SwitchModel` identified by given resource identifier may already
    exist. If it does not already exist it will be created.

    All attributes of switch model will be set to given values.
    Attributes not given but present in already existing :class:`SwitchModel`
    will be set to None or [] or other representation of "not set".

    :param resource_id: Resource identifier uniquely identifying the
        switch model to modify.
        (See :class:`SwitchModel` for what attribute is the resource identifier)
    :type resouce_id: str

    :param kwargs: Attributes of switch model to change.
        Possible parameters are public attributes of :class:`SwitchModel` object
        but in a json compatible representation (as nested dict structure)

    :return: The modified or created switch model
    :rtype: SwitchModel
    """

    # Replace list of ports with list of port objects
    if 'ports' in kwargs:
        kwargs['ports'] = _port_models_from_dict(session, kwargs['ports'])

    # Check all arguments before making any changes
    SwitchModel.check_params(**kwargs)

    # Check if switch model exists
    source_sm = query_switch_model(session, resource_id)

    if source_sm is None:
        # Source switch model does not exist:
        # We are creating a new switch model

        # Switch model name is either resource specifier or not set at all
        # (in which case it will be set automatically)
        if 'name' in kwargs:
            if kwargs['name'] != resource_id:
                raise ValueError('Resource identifier "name" of switch model is ambiguous')
        else:
            kwargs.update({'name': resource_id})

        target_sm = SwitchModel(**kwargs)
        session.add(target_sm)
        session.commit()
        return target_sm
    else:
        # Source switch model exists

        # Source switch model exists so target switch model must not also exist
        if 'name' not in kwargs:
            raise KeyError('Missing necessary argument "name" for setting switch model')
        if resource_id != kwargs['name']:
            if query_switch(session, kwargs['name']) is not None:
                raise ValueError(
                    'Cannot set switch model with name {} - switch model already exists'
                    .format(kwargs['name']))

        # Create new switch model object with given state
        # and replace old object with it
        target_sm = SwitchModel(**kwargs)

        session.delete(source_sm)
        session.flush()
        session.add(target_sm)
        session.commit()
        return target_sm

def set_switch(session, resource_id, **kwargs):
    """
    Set a :class:`Switch` corresponding to a given resource identifier
    to a given state.

    :class:`Switch` identified by given resource identifier may already
    exist. If it does not already exist it will be created.

    All attributes of switch will be set to given values.
    Attributes not given but present in already existing :class:`Switch`
    will be set to None or [] or other representation of "not set".

    :param resource_id: Resource identifier uniquely identifying the
        switch to modify.
        (See :class:`Switch` for what attribute is the resource identifier)
    :type resouce_id: str

    :param kwargs: Attributes of switch to change.
        Possible parameters are public attributes of :class:`Switch` object
        but in a json compatible representation (as nested dict structure)

    :return: The modified or created switch
    :rtype: Switch
    """

    # Replace list of ports with list of port objects
    if 'ports' in kwargs:
        kwargs['ports'] = _ports_from_dict(session, kwargs['ports'])

    # Replace switch model string with switch model object
    if 'model' in kwargs:
        kwargs['model'] = query_switch_model(session, kwargs['model'])

    # Check all arguments before making any changes
    Switch.check_params(**kwargs)

    # Check if switch exists
    source_sw = query_switch(session, resource_id)

    if source_sw is None:
        # Source switch does not exist:
        # We are creating a new switch

        # Switch name is either resource specifier or not set at all
        # (in which case it will be set automatically)
        if 'name' in kwargs:
            if kwargs['name'] != resource_id:
                raise ValueError('Resource identifier "name" of switch is ambiguous')
        else:
            kwargs.update({'name': resource_id})

        target_sw = Switch(**kwargs)
        session.add(target_sw)
        session.commit()
        return target_sw
    else:
        # Source switch exists

        # Source switch exists so target switch must not also exist
        if 'name' not in kwargs:
            raise KeyError('Missing necessary argument "name" for setting switch')
        if resource_id != kwargs['name']:
            if query_switch(session, kwargs['name']) is not None:
                raise ValueError(
                    'Cannot set switch with name {} - switch already exists'
                    .format(kwargs['name']))

        # Create new switch object with given state
        # and replace old object with it
        target_sw = Switch(**kwargs)

        session.delete(source_sw)
        session.flush()
        session.add(target_sw)
        session.commit()
        return target_sw

def set_port_type(session, resource_id, **kwargs):
    """
    Set a :class:`PortType` corresponding to a given resource identifier
    to a given state.

    :class:`PortType` identified by given resource identifier may already
    exist. If it does not already exist it will be created.

    All attributes of port type will be set to given values.
    Attributes not given but present in already existing :class:`PortType`
    will be set to None or [] or other representation of "not set".

    :param resource_id: Resource identifier uniquely identifying the
        port type to modify.
        (See :class:`PortType` for what attribute is the resource identifier)
    :type resouce_id: str

    :param kwargs: Attributes of port type to change.
        Possible parameters are public attributes of :class:`PortType` object
        but in a json compatible representation (as nested dict structure)

    :return: The modified or created port type
    :rtype: PortType
    """

    # Check all arguments before making any changes
    PortType.check_params(**kwargs)

    # Check if source port type exists
    source_pt = query_port_type(session, resource_id)

    if source_pt is None:
        # Source port type does not exist:
        # We are creating a new port type

        # Port type description is either resource specifier or not set at
        # all (in which case it will be set automatically)
        if 'description' in kwargs:
            if kwargs['description'] != resource_id:
                raise ValueError('Resource identifier "description" of port type is ambiguous')
        else:
            kwargs.update({'description': resource_id})

        target_pt = PortType(**kwargs)
        session.add(target_pt)
        session.commit()
        return target_pt
    else:
        # Source port type exists

        # Source port type exists so target port type must not also exist
        if 'description' not in kwargs:
            raise KeyError('Missing necessary argument "description" for setting port type')
        if resource_id != kwargs['description']:
            if query_port_type(session, kwargs['description']) is not None:
                raise ValueError(
                    'Cannot set port type with description {} - port type already exists'
                    .format(kwargs['description']))

        # Create a new port type object with given state
        # and replace old object with it
        target_pt  = PortType(**kwargs)

        session.delete(source_pt)
        session.flush()
        session.add(target_pt)
        session.commit()
        return target_pt

def set_vlan(session, resource_id, **kwargs):
    """
    Set a :class:`Vlan` corresponding to a given resource identifier
    to a given state.

    :class:`Vlan` identified by given resource identifier may already
    exist. If it does not already exist it will be created.

    All attributes of vlan will be set to given values.
    Attributes not given but present in already existing :class:`Vlan`
    will be set to None or [] or other representation of "not set".

    :param resource_id: Resource identifier uniquely identifying the
        vlan to modify.
        (See :class:`Vlan` for what attribute is the resource identifier)
    :type resouce_id: str

    :param kwargs: Attributes of vlan to change.
        Possible parameters are public attributes of :class:`Vlan` object
        but in a json compatible representation (as nested dict structure)

    :return: The modified or created vlan
    :rtype: Vlan
    """

    # Check all arguments before making any changes
    Vlan.check_params(**kwargs)

    # Check if source vlan exists
    source_vl = query_vlan(session, resource_id)

    if source_vl is None:
        # Source vlan does not exist:
        # We are creating a new vlan

        # Vlan tag is either resource specifier or not set at all
        # (in which case it will be set automatically)
        if 'tag' in kwargs:
            if kwargs['tag'] != resource_id:
                raise ValueError('Resource identifier "tag" of vlan is ambiguous')
        else:
            kwargs.update({'tag': resource_id})

        target_vl = Vlan(**kwargs)
        session.add(target_vl)
        session.commit()
        return target_vl
    else:
        # Source vlan exists

        # Source vlan exists so target vlan must not also exist
        if 'tag' not in kwargs:
            raise KeyError('Missing necessary argument "tag" for setting vlan')
        if resource_id != kwargs['tag']:
            if query_vlan(session, kwargs['tag']) is not None:
                raise ValueError(
                    'Cannot set vlan with tag {} - vlan already exists'
                    .format(kwargs['tag']))

        # Create a new vlan object with given state
        # and replace old object with it
        target_vl = Vlan(**kwargs)

        session.delete(source_vl)
        session.flush()
        session.add(target_vl)
        session.commit()
        return target_vl


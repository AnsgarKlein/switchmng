from . import *

def modify_switch_model(session, resource_id, **kwargs):
    """
    Modify a :class:`SwitchModel` object in the database.

    All given attributes of switch model will be modified.
    Attributes not given will not be changed and will keep their current
    state.

    :param resource_id: Resource identifier uniquely identifying the
        switch model to modify.
        (See :class:`SwitchModel` for what attribute is the resource identifier)
    :type resouce_id: str

    :param kwargs: Attributes of switch model to change.
        Possible parameters are public attributes of :class:`SwitchModel` object
        but in a json compatible representation (as nested dict structure)

    :return: The modified switch model
    :rtype: SwitchModel
    """

    # Check if switch model exists
    sm = query_switch_model(session, resource_id)
    if sm is None:
        raise ValueError("Given switch model '{}' does not exist"
            .format(resource_id))

    # Replace list of ports with list of port objects
    if 'ports' in kwargs:
        kwargs['ports'] = _port_models_from_dict(session, kwargs['ports'])

    # Check all arguments before making any changes
    kwargs = SwitchModel.check_params(**kwargs)

    # Apply modifications
    if 'ports' in kwargs:
        ports = kwargs.pop('ports')
        sm.modify_ports(ports)
    for key, val in kwargs.items():
        setattr(sm, key, val)

    session.add(sm)
    session.commit()

    return sm

def modify_switch(session, resource_id, **kwargs):
    """
    Modify a :class:`Switch` object in the database.

    All given attributes of switch will be modified.
    Attributes not given will not be changed and will keep their current
    state.

    :param resource_id: Resource identifier uniquely identifying the
        switch to modify.
        (See :class:`Switch` for what attribute is the resource identifier)
    :type resouce_id: str

    :param kwargs: Attributes of switch to change.
        Possible parameters are public attributes of :class:`Switch` object
        but in a json compatible representation (as nested dict structure)

    :return: The modified switch
    :rtype: Switch
    """

    # Check if switch exists
    sw = query_switch(session, resource_id)
    if sw is None:
        raise ValueError("Given switch '{}' does not exist"
            .format(resource_id))

    # Replace list of ports with list of port objects
    if 'ports' in kwargs:
        kwargs['ports'] = _ports_from_dict(session, kwargs['ports'])

    # Replace switch model string with switch model object
    if 'model' in kwargs:
        kwargs['model'] = query_switch_model(session, kwargs['model'])

    # Check all arguments before making any changes
    Switch.check_params(**kwargs)

    # Apply modifications
    if 'ports' in kwargs:
        ports = kwargs.pop('ports')
        sw.modify_ports(ports)
    for key, val in kwargs.items():
        setattr(sw, key, val)

    session.add(sw)
    session.commit()

    return sw

def modify_port_type(session, resource_id, **kwargs):
    """
    Modify a :class:`PortType` object in the database.

    All given attributes of port type will be modified.
    Attributes not given will not be changed and will keep their current
    state.

    :param resource_id: Resource identifier uniquely identifying the
        port type to modify.
        (See :class:`PortType` for what attribute is the resource identifier)
    :type resouce_id: str

    :param kwargs: Attributes of port type to change.
        Possible parameters are public attributes of :class:`PortType` object
        but in a json compatible representation (as nested dict structure)

    :return: The modified port type object
    :rtype: PortType
    """

    # Check if port type exists
    pt = query_port_type(session, resource_id)
    if pt is None:
        raise ValueError("Given port type '{}' does not exist"
            .format(resource_id))

    # Check all arguments before making any changes
    kwargs = PortType.check_params(**kwargs)

    # Apply modifications
    for key, val in kwargs.items():
        setattr(pt, key, val)

    session.add(pt)
    session.commit()

    return pt

def modify_vlan(session, resource_id, **kwargs):
    """
    Modify a :class:`Vlan` object in the database.

    All given attributes of vlan will be modified.
    Attributes not given will not be changed and will keep their current
    state.

    :param resource_id: Resource identifier uniquely identifying the
        vlan to modify.
        (See :class:`Vlan` for what attribute is the resource identifier)
    :type resouce_id: str

    :param kwargs: Attributes of vlan to change.
        Possible parameters are public attributes of :class:`Vlan` object
        but in a json compatible representation (as nested dict structure)

    :return: The modified vlan object
    :rtype: Vlan
    """

    # Check if vlan exists
    vl = query_vlan(session, resource_id)
    if vl is None:
        raise ValueError("Given VLAN '{}' does not exist"
            .format(resource_id))

    # Check all arguments before making any changes
    kwargs = Vlan.check_params(**kwargs)

    # Apply modifications
    for key, val in kwargs.items():
        setattr(vl, key, val)

    session.add(vl)
    session.commit()

    return vl


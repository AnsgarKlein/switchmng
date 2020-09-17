from . import *

def add_switch_model(session, **kwargs):
    """
    Create a new switch model and add it to the database.

    :param kwargs: Parameters for new switch model.
        Possible parameters are public attributes of :class:`SwitchModel` object
        but in a json compatible representation (as nested dict structure)

    :return: The newly added switch model
    :rtype: SwitchModel
    """

    # Check if switch model already exists
    if 'name' not in kwargs:
        raise KeyError('Missing necessary argument "name" for adding switch model')
    if query_switch_model(session, kwargs['name']) is not None:
        raise ValueError(
            'Cannot add switch model with name {} - switch model already exists'
            .format(kwargs['name']))

    # Replace list of port strings with list of port objects
    if 'ports' in kwargs:
        kwargs['ports'] = _port_models_from_dict(session, kwargs['ports'])

    # Create switch model
    sm = SwitchModel(**kwargs)
    session.add(sm)
    session.commit()
    return sm

def add_switch(session, **kwargs):
    """
    Create a new switch and add it to the database.

    :param kwargs: Parameters for new switch.
        Possible parameters are public attributes of :class:`Switch` object
        but in a json compatible representation (as nested dict structure)

    :return: The newly added switch
    :rtype: Switch
    """

    # Check if switch already exists
    if 'name' not in kwargs:
        raise KeyError('Missing necessary argument "name" for adding switch')
    if query_switch(session, kwargs['name']) is not None:
        raise ValueError(
            'Cannot add switch with name {} - switch already exists'
            .format(kwargs['name']))

    # Replace list of port strings with list of port objects
    if 'ports' in kwargs:
        kwargs['ports'] = _ports_from_dict(session, kwargs['ports'])

    # Replace switch model string with switch model object
    if 'model' in kwargs:
        kwargs['model'] = query_switch_model(session, kwargs['model'])

    # Create switch
    sw = Switch(**kwargs)
    session.add(sw)
    session.commit()
    return sw

def add_port_type(session, **kwargs):
    """
    Create a new port type and add it to the database.

    :param kwargs: Parameters for new port type.
        Possible parameters are public attributes of :class:`PortType` object
        but in a json compatible representation (as nested dict structure)

    :return: The newly added port tpye
    :rtype: PortType
    """

    # Check if port type already exists
    if 'description' not in kwargs:
        raise KeyError('Missing necessary argument "description" for adding port type')
    if query_port_type(session, kwargs['description']) is not None:
        raise ValueError(
            'Cannot add port type with description {} - port type already exists'
            .format(kwargs['description']))

    # Add port type
    pt = PortType(**kwargs)
    session.add(pt)
    session.commit()
    return pt

def add_vlan(session, **kwargs):
    """
    Create a new vlan and add it to the database.

    :param kwargs: Parameters for new vlan.
        Possible parameters are public attributes of :class:`Vlan` object
        but in a json compatible representation (as nested dict structure)

    :return: The newly added vlan
    :rtype: Vlan
    """

    # Check if vlan already exists
    if 'tag' not in kwargs:
        raise KeyError('Missing necessary argument "tag" for adding vlan')
    if query_vlan(session, kwargs['tag']) is not None:
        raise ValueError(
            'Cannot add vlan with tag {} - vlan already exists'
            .format(kwargs['tag']))

    # Add vlan
    vl = Vlan(**kwargs)
    session.add(vl)
    session.commit()
    return vl


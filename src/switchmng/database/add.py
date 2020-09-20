from switchmng.schema import *

from .query import *
from .helper import *

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
        kwargs['ports'] = port_models_from_dict(session, kwargs['ports'])

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
        kwargs['ports'] = ports_from_dict(session, kwargs['ports'])

    # Replace switch model string with switch model object
    if 'model' in kwargs:
        kwargs['model'] = query_switch_model(session, kwargs['model'])

    # Create switch
    sw = Switch(**kwargs)
    session.add(sw)
    session.commit()
    return sw

def add_network_protocol(session, **kwargs):
    """
    Create a new network protocol and add it to the database.

    :param kwargs: Parameters for new network protocol.
        Possible parameters are public attributes of :class:`NetworkProtocol`
        object but in a json compatible representation (as nested dict structure)

    :return: The newly added network protocol
    :rtype: NetworkProtocol
    """

    # Check if network protocol already exists
    if 'name' not in kwargs:
        raise KeyError("Missing necessary argument 'name' for adding network protocol")
    if query_network_protocol(session, kwargs['name']) is not None:
        raise ValueError(
            'Cannot add network protocol with name {} - network protocol already exists'
            .format(kwargs['name']))

    # Add network protocol
    np = NetworkProtocol(**kwargs)
    session.add(np)
    session.commit()
    return np

def add_connector(session, **kwargs):
    """
    Create a new connector and add it to the database.

    :param kwargs: Parameters for new connector.
        Possible parameters are public attributes of :class:`Connector`
        object but in a json compatible representation (as nested dict structure)

    :return: The newly added connector
    :rtype: Connector
    """

    # Check if connector already exists
    if 'name' not in kwargs:
        raise KeyError("Missing necessary argument 'name' for adding connector")
    if query_connector(session, kwargs['name']) is not None:
        raise ValueError(
            'Cannot add connector with name {} - connector already exists'
            .format(kwargs['name']))

    # Add connector
    cn = Connector(**kwargs)
    session.add(cn)
    session.commit()
    return cn

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


from switchmng.schema import *

from .query import *
from .helper import *

def modify_switch_model(session, resource_id, **kwargs):
    """
    Modify a :class:`SwitchModel` object in the database.

    All given attributes of switch model will be modified.
    Attributes not given will not be changed and will keep their current
    state.

    :param resource_id: Resource identifier uniquely identifying the
        switch model to modify.
        (See :class:`SwitchModel` for what attribute is the resource identifier)
    :type resource_id: str

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
        kwargs['ports'] = port_models_from_dict(session, kwargs['ports'])

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

def modify_port_model(session, switch_model_resource_id, port_model_resource_id, **kwargs):
    """
    Modify a :class:`PortModel` object in the database.

    All given attributes of port model will be modified.
    Attributes not given will not be changed and will keep their current
    state.

    :param switch_model_resource_id: Resource identifier uniquely identifying
        the switch model containing the port model to modify.
        (See :class:`SwitchModel` for what attribute is the resource identifier)
    :type: switch_model_resource_id: str

    :param port_model_resource_id: Resource identifier together with switch model
        uniquely identifying the port model to modify.
        (See :class:`PortModel` for what attribute is the resource identifier)
    :type: port_model_resource_id: str

    :param kwargs: Attributes of port model to change.
        Possible parameters are public attributes of :class:`PortModel` object
        but in a json compatible representation (as nested dict structure)

    :return: The modified port model
    :rtype: PortModel
    """

    # Check if port model exists
    sm = query_switch_model(session, switch_model_resource_id)
    if sm is None:
        raise ValueError("Given switch model '{}' does not exist"
            .format(resource_id))
    pm = sm.port(port_model_resource_id)
    if pm is None:
        raise ValueError(
            "Given port model '{}' of given switch model '{}' does not exist"
            .format(port_model_resource_id, switch_model_resource_id))

    # Replace list of network protocol strings with list of network protocol objects
    if 'network_protocols' in kwargs:
        kwargs['network_protocols'] = [ query_network_protocol(session, proto)
                                        for proto in kwargs['network_protocols'] ]

    # Replace connector string with connector object
    if 'connector' in kwargs:
        kwargs['connector'] = query_connector(session, kwargs['connector'])

    # Check all arguments before making any changes
    PortModel.check_params(**kwargs)

    # Apply modifications
    for key, val in kwargs.items():
        setattr(pm, key, val)

    session.add(pm)
    session.commit()
    return pm

def modify_switch(session, resource_id, **kwargs):
    """
    Modify a :class:`Switch` object in the database.

    All given attributes of switch will be modified.
    Attributes not given will not be changed and will keep their current
    state.

    :param resource_id: Resource identifier uniquely identifying the
        switch to modify.
        (See :class:`Switch` for what attribute is the resource identifier)
    :type resource_id: str

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

    # Replace list of port dicts with list of port objects
    if 'ports' in kwargs:
        kwargs['ports'] = ports_from_dict(session, kwargs['ports'])

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

def modify_network_protocol(session, resource_id, **kwargs):
    """
    Modify a :class:`NetworkProtocol` object in the database.

    All given attributes of network protocol will be modified.
    Attributes not given will not be changed and will keep their current
    state.

    :param resource_id: Resource identifier uniquely identifying the
        network protocol to modify.
        (See :class:`NetworkProtocol` for what attribute is the resource identifier)
    :type resource_id: str

    :param kwargs: Attributes of network protocol to change.
        Possible parameters are public attributes of :class:`NetworkProtocol` object
        but in a json compatible representation (as nested dict structure)

    :return: The modified network protocol object
    :rtype: NetworkProtocol
    """

    # Check if network protocol exists
    np = query_network_protocol(session, resource_id)
    if np is None:
        raise ValueError("Given network protocol '{}' does not exist"
            .format(resource_id))

    # Check all arguments before making any changes
    kwargs = NetworkProtocol.check_params(**kwargs)

    # Apply modifications
    for key, val in kwargs.items():
        setattr(np, key, val)

    session.add(np)
    session.commit()

    return np

def modify_connector(session, resource_id, **kwargs):
    """
    Modify a :class:`Connector` object in the database.

    All given attributes of connector will be modified.
    Attributes not given will not be changed and will keep their
    current state.

    :param resource_id: Resource identifier uniquely identifying the
        connector to modify
    :type resource_id: str

    :param kwargs: Attributes of connector to change.
        Possible parameters are public attributes of :class:`Connector` object
        but in a json compatible representation (as nested dict structure)

    :return: The modified connector object
    :rtype: Connector
    """

    # Check if connector exists
    cn = query_connector(session, resource_id)
    if cn is None:
        raise ValueError("Given connector '{}' does not exist"
            .format(resource_id))

    # Check all arguments before making any changes
    kwargs = Connector.check_params(**kwargs)

    # Apply modifications
    for key, val in kwargs.items():
        setattr(cn, key, val)

    session.add(cn)
    session.commit()

    return cn

def modify_vlan(session, resource_id, **kwargs):
    """
    Modify a :class:`Vlan` object in the database.

    All given attributes of vlan will be modified.
    Attributes not given will not be changed and will keep their current
    state.

    :param resource_id: Resource identifier uniquely identifying the
        vlan to modify.
        (See :class:`Vlan` for what attribute is the resource identifier)
    :type resource_id: str

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


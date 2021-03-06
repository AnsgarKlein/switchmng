from switchmng.schema import *

from .query import *
from .helper import *

def modify_switch_model(session, resource_id: str, **kwargs) -> SwitchModel:
    """
    Modify a :class:`SwitchModel` object in the database.

    All given attributes of switch model will be modified.
    Attributes not given will not be changed and will keep their current
    state.

    :param resource_id: Resource identifier uniquely identifying the
        switch model to modify.
        (See :class:`SwitchModel` for what attribute is the resource identifier)

    :param kwargs: Attributes of switch model to change.
        Possible parameters are public attributes of :class:`SwitchModel` object
        but in a json compatible representation (as nested dict structure)

    :return: The modified switch model
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
    SwitchModel.check_params(**kwargs)

    # Apply modifications
    for key, val in kwargs.items():
        setattr(sm, key, val)

    session.add(sm)
    session.commit()

    return sm

def modify_port_model(session,
                      switch_model_resource_id: str,
                      port_model_resource_id: str,
                      **kwargs) -> PortModel:
    """
    Modify a :class:`PortModel` object in the database.

    All given attributes of port model will be modified.
    Attributes not given will not be changed and will keep their current
    state.

    :param switch_model_resource_id: Resource identifier uniquely identifying
        the switch model containing the port model to modify.
        (See :class:`SwitchModel` for what attribute is the resource identifier)

    :param port_model_resource_id: Resource identifier together with switch model
        uniquely identifying the port model to modify.
        (See :class:`PortModel` for what attribute is the resource identifier)

    :param kwargs: Attributes of port model to change.
        Possible parameters are public attributes of :class:`PortModel` object
        but in a json compatible representation (as nested dict structure)

    :return: The modified port model
    """

    # Check if port model exists
    sm = query_switch_model(session, switch_model_resource_id)
    if sm is None:
        raise ValueError("Given switch model '{}' does not exist"
            .format(switch_model_resource_id))
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
    if 'connector' in kwargs and kwargs['connector'] is not None:
        kwargs['connector'] = query_connector(session, kwargs['connector'])

    # Check all arguments before making any changes
    PortModel.check_params(**kwargs)

    # Apply modifications
    for key, val in kwargs.items():
        setattr(pm, key, val)

    session.add(pm)
    session.commit()
    return pm

def modify_switch(session, resource_id: str, **kwargs) -> Switch:
    """
    Modify a :class:`Switch` object in the database.

    All given attributes of switch will be modified.
    Attributes not given will not be changed and will keep their current
    state.

    :param resource_id: Resource identifier uniquely identifying the
        switch to modify.
        (See :class:`Switch` for what attribute is the resource identifier)

    :param kwargs: Attributes of switch to change.
        Possible parameters are public attributes of :class:`Switch` object
        but in a json compatible representation (as nested dict structure)

    :return: The modified switch
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
    for key, val in kwargs.items():
        setattr(sw, key, val)

    session.add(sw)
    session.commit()
    return sw

def modify_port(
        session,
        switch_resource_id: str,
        port_resource_id: str,
        **kwargs) -> Port:
    """
    Modify a :class:`Port` object in the database.

    All given attributes of port will be modified.
    Attributes not given will not be changed and will keep their current
    state.

    :param switch_resource_id: Resource identifier uniquely identifying the
        switch containing the port to modify.
        (See :class:`Switch` for what attribute is the resource identifier)

    :param port_resource_id: Resource identifier together with switch uniquely
        identifying the port to modify.
        (See :class:`Port` for what attribute is the resource identifier)

    :param kwargs: Attributes of port to change.
        Possible parameters are public attributes of :class:`Port` object
        but in a json compatible representation (as nested dict structure)

    :return: The modified port
    """

    # Check if port exists
    sw = query_switch(session, switch_resource_id)
    if sw is None:
        raise ValueError("Given switch '{}' does not exist"
            .format(switch_resource_id))
    pt = sw.port(port_resource_id)
    if pt is None:
        raise ValueError(
            "Given port '{}' of given switch '{}' does not exist"
            .format(port_resource_id, switch_resource_id))

    # Replace list of vlan strings with list of vlan objects
    if 'vlans' in kwargs:
        kwargs['vlans'] = [ query_vlan(session, v) for v in kwargs['vlans'] ]
        if None in kwargs['vlans']:
            raise ValueError('Given vlan in list of vlans of port does not exist')

    # Check all arguments before making any changes
    Port.check_params(**kwargs)

    # Apply modifications
    for key, val in kwargs.items():
        if key == 'name':
            raise ValueError('Cannot modify attribute "name" of port')
        setattr(pt, key, val)

    # Pseudo-set ports of switch in order to make sure all modify ports
    # exist in switch model.
    sw.ports = sw.ports

    session.add(pt)
    session.commit()
    return pt

def modify_network_protocol(session, resource_id: str, **kwargs) -> NetworkProtocol:
    """
    Modify a :class:`NetworkProtocol` object in the database.

    All given attributes of network protocol will be modified.
    Attributes not given will not be changed and will keep their current
    state.

    :param resource_id: Resource identifier uniquely identifying the
        network protocol to modify.
        (See :class:`NetworkProtocol` for what attribute is the resource identifier)

    :param kwargs: Attributes of network protocol to change.
        Possible parameters are public attributes of :class:`NetworkProtocol` object
        but in a json compatible representation (as nested dict structure)

    :return: The modified network protocol object
    """

    # Check if network protocol exists
    np = query_network_protocol(session, resource_id)
    if np is None:
        raise ValueError("Given network protocol '{}' does not exist"
            .format(resource_id))

    # Check all arguments before making any changes
    NetworkProtocol.check_params(**kwargs)

    # Apply modifications
    for key, val in kwargs.items():
        setattr(np, key, val)

    session.add(np)
    session.commit()

    return np

def modify_connector(session, resource_id: str, **kwargs) -> Connector:
    """
    Modify a :class:`Connector` object in the database.

    All given attributes of connector will be modified.
    Attributes not given will not be changed and will keep their
    current state.

    :param resource_id: Resource identifier uniquely identifying the
        connector to modify

    :param kwargs: Attributes of connector to change.
        Possible parameters are public attributes of :class:`Connector` object
        but in a json compatible representation (as nested dict structure)

    :return: The modified connector object
    """

    # Check if connector exists
    cn = query_connector(session, resource_id)
    if cn is None:
        raise ValueError("Given connector '{}' does not exist"
            .format(resource_id))

    # Check all arguments before making any changes
    Connector.check_params(**kwargs)

    # Apply modifications
    for key, val in kwargs.items():
        setattr(cn, key, val)

    session.add(cn)
    session.commit()

    return cn

def modify_vlan(session, resource_id: str, **kwargs) -> Vlan:
    """
    Modify a :class:`Vlan` object in the database.

    All given attributes of vlan will be modified.
    Attributes not given will not be changed and will keep their current
    state.

    :param resource_id: Resource identifier uniquely identifying the
        vlan to modify.
        (See :class:`Vlan` for what attribute is the resource identifier)

    :param kwargs: Attributes of vlan to change.
        Possible parameters are public attributes of :class:`Vlan` object
        but in a json compatible representation (as nested dict structure)

    :return: The modified vlan object
    """

    # Check if vlan exists
    vl = query_vlan(session, resource_id)
    if vl is None:
        raise ValueError("Given VLAN '{}' does not exist"
            .format(resource_id))

    # Check all arguments before making any changes
    Vlan.check_params(**kwargs)

    # Apply modifications
    for key, val in kwargs.items():
        setattr(vl, key, val)

    session.add(vl)
    session.commit()

    return vl

from switchmng.schema import *

from .query import *
from .helper import *

def set_switch_model(session, resource_id, **kwargs):
    """
    Set a :class:`SwitchModel` in the database to a given state.

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
        kwargs['ports'] = port_models_from_dict(session, kwargs['ports'])

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
            if query_switch_model(session, kwargs['name']) is not None:
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

def set_port_model(session, switch_model_resource_id, port_model_resource_id, **kwargs):
    """
    Set a :class:`PortModel` in the database to a given state.

    :class:`PortModel` identified by given resource identifier on switch model
    identified by given resource identifier may already exist. If it does not
    already exist it will be created.

    All attributes of port model will be set to given values.
    Attributes not given but present in already existing :class:`PortModel`
    will be set to None or [] or other representation of "not set".

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

    :return: The modified or created port model
    :rtype: PortModel
    """

    # Check if switch model exists
    sm = query_switch_model(session, switch_model_resource_id)
    if sm is None:
        raise ValueError('Given switch model does not exist')

    # Replace list of network protocol strings with list of network protocol objects
    if 'network_protocols' in kwargs:
        kwargs['network_protocols'] = [ query_network_protocol(session, proto)
                                        for proto in kwargs['network_protocols'] ]
        if None in kwargs['network_protocols']:
            raise ValueError('Given network protocol in list of network protocols of port does not exist')

    # Replace connector string with connector object
    if 'connector' in kwargs:
        kwargs['connector'] = query_connector(session, kwargs['connector'])
        if kwargs['connector'] is None:
            raise ValueError('Given connector of port does not exist')

    # Check all arguments before making any changes
    PortModel.check_params(**kwargs)

    # Check if port model exists
    source_pm = query_port_model(session, switch_model_resource_id, port_model_resource_id)

    if source_pm is None:
        # Source port model does not exist:
        # We are creating a new port model

        # Port model name is either resource specifier or not set at all
        # (in which case it will be set automatically)
        if 'name' in kwargs:
            if kwargs['name'] != port_model_resource_id:
                raise ValueError('Resource identifier "name" of port model is ambiguous')
        else:
            kwargs.update({'name': port_model_resource_id})

        # Create new port model object and add it
        # to existing ports of switch model
        target_pm = PortModel(**kwargs)

        ports = [ port for port in sm.ports ]
        ports.append(target_pm)
        sm.ports = ports

        session.commit()
        return target_pm
    else:
        # Source port model exists

        # Source port model exists so target port model must not also exist
        if 'name' not in kwargs:
            raise KeyError('Missing necessary argument "name" for setting port model')
        if port_model_resource_id != kwargs['name']:
            if query_port_model(session, switch_model_resource_id, kwargs['name']) is not None:
                raise ValueError(
                    'Cannot set port model with name {} - port model already exists'
                    .format(kwargs['name']))

        # Create new port model object with given state
        # and replace old object with it
        target_pm = PortModel(**kwargs)

        ports = [ port for port in sm.ports if port != source_pm ]
        ports.append(target_pm)
        sm.ports = ports

        session.commit()
        return target_pm

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
        kwargs['ports'] = ports_from_dict(session, kwargs['ports'])

    # Replace switch model string with switch model object
    if 'model' in kwargs:
        kwargs['model'] = query_switch_model(session, kwargs['model'])
        if kwargs['model'] is None:
            raise ValueError('Given switch model of switch does not exist')

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

def set_port(session, switch_resource_id, port_resource_id, **kwargs):
    """
    Set a :class:`Port` in the database to a given state.

    :class:`Port` identified by given resource identifier on switch identified
    by given resource identifier may already exist. If it does not already
    exist it will be created.

    All attributes of port will be set to given values.
    Attributes not given but present in already existing :class:`Port`
    will be set to None or [] or other representation of "not set".

    :param switch_resource_id: Resource identifier uniquely identifying the
        switch containing the port to modify.
        (See :class:`Switch` for what attribute is the resource identifier)
    :type: switch_resource_id: str

    :param port_resource_id: Resource identifier together with switch uniquely
        identifying the port to modify.
        (See :class:`Port` for what attribute is the resource identifier)
    :type: port_resource_id: str

    :param kwargs: Attributes of port to change.
        Possible parameters are public attributes of :class:`Port` object
        but in a json compatible representation (as nested dict structure)

    :return: The modified or created port
    :rtype: Port
    """

    # Check if switch model exists
    sw = query_switch(session, switch_resource_id)
    if sw is None:
        raise ValueError('Given switch does not exist')

    # Replace list of vlan strings with list of vlan objects
    if 'vlans' in kwargs:
        kwargs['vlans'] = [ query_vlan(session, v) for v in kwargs['vlans'] ]
        if None in kwargs['vlans']:
            raise ValueError('Given vlan in list of vlans of port does not exist')

    # Check all arguments before making any changes
    Port.check_params(**kwargs)

    # Check if port model exists
    source_pt = query_port(session, switch_resource_id, port_resource_id)

    if source_pt is None:
        # Source port does not exist:
        # We are creating a new port

        # Port name is either resource specifier or not set at all
        # (in which case it will be set automatically)
        if 'name' in kwargs:
            if kwargs['name'] != port_resource_id:
                raise ValueError('Resource identifier "name" of port is ambiguous')
        else:
            kwargs.update({'name': port_resource_id})

        # Create new port model object and add it
        # to existing ports of switch model
        target_pt = Port(**kwargs)

        ports = [ port for port in sw.ports ]
        ports.append(target_pt)
        sm.ports = ports

        session.commit()
        return target_pt
    else:
        # Source port exists

        # Source port exists so target port must not also exist
        if 'name' not in kwargs:
            raise KeyError('Missing necessary argument "name" for setting port')
        if port_resource_id != kwargs['name']:
            if query_port(session, switch_resource_id, kwargs['name']) is not None:
                raise ValueError(
                    'Cannot set port with name {} - port already exists'
                    .format(kwargs['name']))

        # Create new port object with given state
        # and replace old object with it
        target_pt = Port(**kwargs)

        ports = [ port for port in sw.ports if port != source_pt ]
        ports.append(target_pt)
        sw.ports = ports

        session.commit()
        return target_pt

def set_network_protocol(session, resource_id, **kwargs):
    """
    Set a :class:`NetworkProtocol` in the database to a given state.

    :class:`NetworkProtocol` identified by given resource identifier may already
    exist. If it does not already exist it will be created.

    All attributes of network protocol will be set to given values.
    Attributes not given but present in already existing :class:`NetworkProtocol`
    will be set to None or [] or other representation of "not set".

    :param resource_id: Resource identifier uniquely identifying the
        network protocol to modify.
        (See :class:`NetworkProtocol` for what attribute is the resource identifier)
    :type resouce_id: str

    :param kwargs: Attributes of network protocol to change.
        Possible parameters are public attributes of :class:`NetworkProtocol` object
        but in a json compatible representation (as nested dict structure)

    :return: The modified or created network protocol
    :rtype: NetworkProtocol
    """

    # Check all arguments before making any changes
    NetworkProtocol.check_params(**kwargs)

    # Check if source network protocol exists
    source_np = query_network_protocol(session, resource_id)

    if source_np is None:
        # Source network protocol does not exist:
        # We are creating a new network protocol

        # Network protocol name is either resource specifier or not set at
        # all (in which case it will be set automatically)
        if 'name' in kwargs:
            if kwargs['name'] != resource_id:
                raise ValueError('Resource identifier "name" of network protocol is ambiguous')
        else:
            kwargs.update({'name': resource_id})

        target_np = NetworkProtocol(**kwargs)
        session.add(target_np)
        session.commit()
        return target_np
    else:
        # Source network protocol exists

        # Source network protocol exists so target network protocol must not also exist
        if 'name' not in kwargs:
            raise KeyError('Missing necessary argument "name" for setting network protocol')
        if resource_id != kwargs['name']:
            if query_network_protocol(session, kwargs['name']) is not None:
                raise ValueError(
                        'Cannot set network protocol with name {} ' + \
                        '- network protocol already exists'
                    .format(kwargs['name']))

        # Create a new network protocol object with given state
        # and replace old object with it
        target_np  = NetworkProtocol(**kwargs)

        session.delete(source_np)
        session.flush()
        session.add(target_np)
        session.commit()
        return target_np

def set_connector(session, resource_id, **kwargs):
    """
    Set a :class:`Connector` in the database to a given state.

    :class:`Connector` identified by given resource identifier may already
    exist. If it does not already exist it will be created.

    All attributes of connector will be set to given values.
    Attributes not given but present in already existing :class:`Connector`
    will be set to None or [] or other representation of "not set".

    :param resource_id: Resource identifier uniquely identifying the
        connector to modify.
        (See :class:`Connector` for what attribute is the resource identifier)
    :type resouce_id: str

    :param kwargs: Attributes of connector to change.
        Possible parameters are public attributes of :class:`Connector` object
        but in a json compatible representation (as nested dict structure)

    :return: The modified or created connector
    :rtype: Connector
    """

    # Check all arguments before making any changes
    Connector.check_params(**kwargs)

    # Check if source connector exists
    source_cn = query_connector(session, resource_id)

    if source_cn is None:
        # Source connector does not exist:
        # We are creating a new connector

        # Connector name is either resource specifier or not set at
        # all (in which case it will be set automatically)
        if 'name' in kwargs:
            if kwargs['name'] != resource_id:
                raise ValueError('Resource identifier "name" of connector is ambiguous')
        else:
            kwargs.update({'name': resource_id})

        target_cn = Connector(**kwargs)
        session.add(target_cn)
        session.commit()
        return target_cn
    else:
        # Source connector exists

        # Source connector exists so target connector must not also exist
        if 'name' not in kwargs:
            raise KeyError('Missing necessary argument "name" for setting connector')
        if resource_id != kwargs['name']:
            if query_connector(session, kwargs['name']) is not None:
                raise ValueError(
                        'Cannot set connector with name {} ' + \
                        '- connector already exists'
                    .format(kwargs['name']))

        # Create a new connector object with given state
        # and replace old object with it
        target_cn  = Connector(**kwargs)

        session.delete(source_cn)
        session.flush()
        session.add(target_cn)
        session.commit()
        return target_cn

def set_vlan(session, resource_id, **kwargs):
    """
    Set a :class:`Vlan` in the database to a given state.

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


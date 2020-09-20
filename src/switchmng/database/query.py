from switchmng.schema import *

def query_switch_model(session, resource_id):
    """
    Retrieve :class:`SwitchModel` object from database.

    Query the database for a :class:`SwitchModel` object with given resource
    identifier and return it.

    :param resource_id: Resource identifier uniquely identifying the
        switch model to return.
        (See :class:`SwitchModel` for what attribute is the resource identifier)
    :type resource_id: str

    :return: The switch model object matching the given resource identifier
    :rtype: SwitchModel
    """

    if not isinstance(resource_id, str):
        raise TypeError('Cannot query switch model with resource id not of type str')

    model = session.query(SwitchModel)
    model = model.filter_by(_name = resource_id)

    if len(model.all()) > 1:
        raise TypeError('DB query resulted in multiple elements but only one was requested')

    return model.first()

def query_switch(session, resource_id):
    """
    Retrieve :class:`Switch` object from database.

    Query the database for a :class:`Switch` object with given resource
    identifier and return it.

    :param resource_id: Resource identifier uniquely identifying the
        switch to return.
        (See :class:`Switch` for what attribute is the resource identifier)
    :type resource_id: str

    :return: The switch object matching the given resource identifier
    :rtype: Switch
    """

    if not isinstance(resource_id, str):
        raise TypeError('Cannot query switch with resource id not of type str')

    sw = session.query(Switch)
    sw = sw.filter_by(_name = resource_id)

    if len(sw.all()) > 1:
        raise TypeError('DB query resulted in multiple elements but only one was requested')

    return sw.first()

def query_network_protocol(session, resource_id):
    """
    Retrieve :class:`NetworkProtocol` object from database.

    Query the database for a :class:`NetworkProtocol` object with given
    resource identifier and return it.

    :param resource_id: Resource identifier uniquely identifying the
        network protocol to return.
        (See :class:`NetworkProtocol` for what attribute is the resource identifier)
    :type resource_id: str

    :return: The network protocol object matching the given resource identifier
    :rtype: NetworkProtocol
    """

    if not isinstance(resource_id, str):
        raise TypeError('Cannot query network protocol with resource id not of type str')

    pt = session.query(NetworkProtocol)
    pt = pt.filter_by(_name = resource_id)

    if len(pt.all()) > 1:
        raise TypeError('DB query resulted in multiple elements but only one was requested')

    return pt.first()

def query_connector(session, resource_id):
    """
    Retrieve :class:`Connector` object from database.

    Query the database for a :class:`Connector` object with given
    resource identifier and return it.

    :param resource_id: Resource identifier uniquely identifying the
        connector to return.
        (See :class:`Connector` for what attribute is the resource identifier)
    :type resource_id: str

    :return: The connector object matching the given resource identifier
    :rtype: Connector
    """

    if not isinstance(resource_id, str):
        raise TypeError('Cannot query connector with resource id not of type str')

    cn = session.query(Connector)
    cn = cn.filter_by(_name = resource_id)

    if len(cn.all()) > 1:
        raise TypeError('DB query resulted in multiple elements but only one was requested')

    return cn.first()

def query_vlan(session, resource_id):
    """
    Retrieve :class:`Vlan` object from database.

    Query the database for a :class:`Vlan` object with given resource
    identifier and return it.

    :param resource_id: Resource identifier uniquely identifying the
        vlan to return.
        (See :class:`Vlan` for what attribute is the resource identifier)
    :type resource_id: str

    :return: The vlan object matching the given resource identifier
    :rtype: Vlan
    """

    if not isinstance(resource_id, int):
        raise TypeError('Cannot query vlan with resource id not of type int')

    vl = session.query(Vlan)
    vl = vl.filter_by(_tag = resource_id)

    if len(vl.all()) > 1:
        raise TypeError('DB query resulted in multiple elements but only one was requested')

    return vl.first()

def query_switch_models(session, **kwargs):
    """
    Retrieve multiple :class:`SwitchModel` objects from database.

    # TODO: Implement and document query_switch_models() correctly
    """

    # Check all arguments before querying
    SwitchModel.check_params(**kwargs)

    # Query
    models = session.query(SwitchModel)

    # Filter with SQL
    for key, val in kwargs.items():
        if key == 'size':
            models = models.filter_by(_size = val)
        elif key == 'network_protocol':
            val = self.query_network_protocols(val)
            if val is None:
                raise ValueError('Given network protocol does not exist')
        else:
            raise TypeError(
                "Cannot query switch models with unexpected filter '{}'".format(key))

    models = models.all()

    # TODO: When querying switch models don't filter manually but let database do the work

    # Filter manually
    for key, val in kwargs.items():
        if key == 'size':
            pass
        elif key == 'network_protocol':
            new_models = list()
            np = val
            for model in models:
                for port in model.ports:
                    if np in port['network_protocols']:
                        new_models.append(model)
                        break
            models = new_models
        else:
            raise TypeError(
                "Cannot query switch models with unexpected filter '{}'".format(key))

    return models

def query_switches(session, **kwargs):
    """
    Retrieve multiple :class:`Switch` objects from database.

    # TODO: Implement and document query_switches() correctly
    """

    # Check all arguments before querying
    Switch.check_params(**kwargs)

    # Query
    switches = session.query(Switch)

    # Filter with SQL
    for key, val in kwargs.items():
        if key == 'location':
            if not isinstance(val, int):
                raise TypeError('Given location of switch is not of type int')
            switches = switches.filter_by(_location = val)
        elif key == 'model':
            kwargs['model'] = query_switch_model(session, val)
            if kwargs['model'] is None:
                raise ValueError(
                    "Got invalid switch model '{}' - switch model does not exist")
            switches = switches.filter_by(_model = kwargs['model'])
        elif key == 'vlan':
            if not isinstance(val, int):
                raise TypeError('Given vlan of port of switch is not of type int')
        else:
            raise TypeError(
                "Cannot query switches with unexpected filter '{}'".format(key))

    switches = switches.all()

    # TODO: When querying switches don't filter manually but let database do the work

    # Filter manually
    for key, val in kwargs.items():
        if key == 'location':
            pass
        elif key == 'model':
            pass
        elif key == 'vlan':
            new_switches = list()
            vl = val
            for switch in switches:
                for port in switch.ports:
                    if vl in port['vlans']:
                        new_switches.append(switch)
                        break
            switches = new_switches
        else:
            raise TypeError(
                "Cannot query switches with unexpected filter '{}'".format(key))

    return switches

def query_network_protocols(session, **kwargs):
    """
    Retrieve multiple :class:`NetworkProtocol` objects from database.

    # TODO: Implement and document query_network_protocols() correctly
    """

    # Check all arguments before querying
    NetworkProtocol.check_params(**kwargs)

    # Query
    nps = session.query(NetworkProtocol)

    # Filter
    for key, val in kwargs.items():
        if key == 'speed':
            nps = nps.filter_by(_speed = val)
        else:
            raise TypeError(
                "Cannot query network protocols with unexpected filter '{}'".format(key))

    return nps.all()

def query_connectors(session, **kwargs):
    """
    Retrieve multiple :class:`Connector` objects from database.

    # TODO: Implement and document query_connectors() correctly
    """

    # Check all arguments before querying
    Connector.check_params(**kwargs)

    # Query
    cns = session.query(Connector)

    # Filter
    for key, val in kwargs.items():
        if False:
            pass
        else:
            raise TypeError(
                "Cannot query connectors with unexpected filter '{}'".format(key))

    return cns.all()

def query_vlans(session, **kwargs):
    """
    Retrieve multiple :class:`Vlan` objects from database.

    # TODO: Implement and document query_vlans() correctly
    """

    # Check all arguments before querying
    Vlan.check_params(**kwargs)

    # Query
    vls = session.query(Vlan)

    # Filter
    for key, val in kwargs.items():
        if key == 'description':
            vls = vls.filter_by(_description = val)
        else:
            raise TypeError(
                "Cannot query vlans with unexpected filter '{}'".format(key))

    return vls.all()


from switchmng.schema import *

from .query import *

def delete_switch_model(session, resource_id: str) -> None:
    """
    Delete a switch model from the database.

    Can only delete a switch model from the database if it is not still
    in use by a switch. Will only delete switch model if there is not
    still a switch which uses the given switch model as its model.

    :param resource_id: Resource identifier uniquely identifying the
        switch model to delete.
        (See :class:`SwitchModel` for what attribute is the resource identifier)
    """

    # Check switch model
    sm = query_switch_model(session, resource_id)
    if sm is None:
        raise ValueError('Given switch model does not exist')

    # Check if there are switches still using this model
    affected_sw = sm._switches
    if not isinstance(affected_sw, list):
        raise TypeError('Expected list of switches to be of type list')
    if len(affected_sw) > 0:
        raise ValueError('Given switch model is still in use')

    # Delete switch model
    session.delete(sm)
    session.commit()

def delete_port_model(
        session,
        switch_model_resource_id: str,
        port_model_resource_id: str) -> None:
    """
    Delete a port model from a switch model from the database.

    :param switch_model_resource_id: Resource identifier uniquely identifying
        the switch model containing the port model to delete.
        (See :class:`SwitchModel` for what attribute is the resource identifier)

    :param port_model_resource_id: Resource identifier together with switch model
        uniquely identifying the port model to delete.
        (See :class:`PortModel` for what attribute is the resource identifier)
    """

    # Check switch model
    sm = query_switch_model(session, switch_model_resource_id)
    if sm is None:
        raise ValueError('Given switch model does not exist')

    # Check port model
    pm = sm.port(port_model_resource_id)
    if pm is None:
        raise ValueError('Given port model of given switch model does not exist')

    # Remove port model from switch model.
    # Removing port model from switch model will remove port from all
    # switches using the switch model.
    sm.ports = [ port for port in sm.ports if port is not pm ]

    # Removing port model from switch model will automatically delete orphan
    # port model object. We just have to commit changes in our session.
    session.commit()

def delete_switch(session, resource_id: str) -> None:
    """
    Delete a switch from the database.

    :param resource_id: Resource identifier uniquely identifying the
        switch to delete.
        (See :class:`Switch` for what attribute is the resource identifier)
    """

    # Check switch
    sw = query_switch(session, resource_id)
    if sw is None:
        raise ValueError('Given switch does not exist')

    # Delete switch
    session.delete(sw)
    session.commit()

def delete_network_protocol(session, resource_id: str) -> None:
    """
    Delete a network protocol from the database.

    Can only delete a network protocol from the database if it is not still
    in use by a port of a switch model.
    Will only delete network protocol if there is not still a switch model
    which uses the given network protocol on one of its ports.

    :param resource_id: Resource identifier uniquely identifying the
        network protocol to delete.
        (See :class:`NetworkProtocol` for what attribute is the resource identifier)
    """

    # Check network protocol
    np = query_network_protocol(session, resource_id)
    if np is None:
        raise ValueError('Given network protocol does not exist')

    # Check if there are port models still using this network protocol
    affected_pm = query_port_models(session, None, network_protocols = [ np ])
    if not isinstance(affected_pm, list):
        raise TypeError('Expected list of port models to be of type list')
    if len(affected_pm) > 0:
        raise ValueError('Given network protocol is still in use')

    # Delete network protocol
    session.delete(np)
    session.commit()

def delete_connector(session, resource_id: str) -> None:
    """
    Delete a connector from the database.

    Can only delete a connector from the database if it is not still
    in use by a port of a switch model.
    Will only delete connector if there is not still a switch model
    which uses the given connector on one of its ports.

    :param resource_id: Resource identifier uniquely identifying the
        connector to delete.
        (See :class:`Connector` for what attribute is the resource identifier)
    """

    # Check connector
    cn = query_connector(session, resource_id)
    if cn is None:
        raise ValueError('Given connector does not exist')

    # Check if there are port models still using this connector
    affected_pm = query_port_models(session, None, connector = cn)
    if not isinstance(affected_pm, list):
        raise TypeError('Expected list of port models to be of type list')
    if len(affected_pm) > 0:
        raise ValueError('Given connector is still in use')

    # Delete connector
    session.delete(cn)
    session.commit()

def delete_vlan(session, resource_id: str) -> None:
    """
    Delete a vlan from the database.

    Can only delete a vlan from the database if it is not still in use by a
    port of a switch.
    Will only delete vlan if there is not still a switch which uses the given
    vlan on one of its ports.

    :param resource_id: Resource identifier uniquely identifying the vlan to
        delete.
        (See :class:`Vlan` for what attribute is the resource identifier)
    """

    # Check vlan
    vl = query_vlan(session, resource_id)
    if vl is None:
        raise ValueError('Given vlan does not exist')

    # Check if this vlan is still in use
    affected_pts = query_ports(session, None, vlans = [ vl ])
    if not isinstance(affected_pts, list):
        raise TypeError('Expected list of ports to be of type list')
    if len(affected_pts) > 0:
        raise ValueError('Given vlan is still in use')

    # Delete vlan
    session.delete(vl)
    session.commit()

from . import *

def delete_switch_model(session, resource_id):
    """
    Delete a switch model from the database.

    Can only delete a switch model from the database if it is not still
    in use by a switch. Will only delete switch model if there is not
    still a switch which uses the given switch model as its model.

    :param resource_id: Resource identifier uniquely identifying the
        switch model to delete.
        (See :class:`SwitchModel` for what attribute is the resource identifier)
    :type resouce_id: str
    """

    # Check switch model
    sm = query_switch_model(session, resource_id)
    if sm is None:
        raise ValueError('Given switch model does not exist')

    # Check if there are switches still using this model
    affected_sw = query_switches(session, model = resource_id)
    if not isinstance(affected_sw, list):
        raise TypeError('Expected list of switches to be of type list')
    if len(affected_sw) > 0:
        raise ValueError('Given switch model is still in use')

    # Delete switch model
    session.delete(sm)
    session.commit()

def delete_switch(session, resource_id):
    """
    Delete a switch from the database.

    :param resource_id: Resource identifier uniquely identifying the
        switch to delete.
        (See :class:`Switch` for what attribute is the resource identifier)
    :type resouce_id: str
    """

    # Check switch
    sw = query_switch(session, resource_id)
    if sw is None:
        raise ValueError('Given switch does not exist')

    # Delete switch
    session.delete(sw)
    session.commit()

def delete_port_type(session, resource_id):
    """
    Delete a port type from the database.

    Can only delete a port type from the database if it is not still
    in use by a port of a switch model.
    Will only delete port type if there is not still a switch model which
    uses the given port type on one of its ports.

    :param resource_id: Resource identifier uniquely identifying the
        port type to delete.
        (See :class:`PortType` for what attribute is the resource identifier)
    :type resouce_id: str
    """

    # Check port type
    pt = query_port_type(session, resource_id)
    if pt is None:
        raise ValueError('Given port type does not exist')

    # Check if there are switch models still using this port type
    affected_sm = query_switch_models(session, port_type = resource_id)
    if not isinstance(affected_sm, list):
        raise TypeError('Expected list of switch models to be of type list')
    if len(affected_sm) > 0:
        raise ValueError('Given port type is still in use')

    # Delete port type
    session.delete(pt)
    session.commit()

def delete_vlan(session, resource_id):
    """
    Delete a vlan from the database.

    Can only delete a vlan from the database if it is not still in use by a
    port of a switch.
    Will only delete vlan if there is not still a switch which uses the given
    vlan on one of its ports.

    :param resource_id: Resource identifier uniquely identifying the vlan to
        delete.
        (See :class:`Vlan` for what attribute is the resource identifier)
    :type resouce_id: str
    """

    # Check vlan
    vl = query_vlan(session, resource_id)
    if vl is None:
        raise ValueError('Given vlan does not exist')

    # Check if there are switch ports still using this vlan
    affected_sw = query_switches(session, vlan = resource_id)
    if not isinstance(affected_sw, list):
        raise TypeError('Expected list of switches to be of type list')
    if len(affected_sw) > 0:
        raise ValueError('Given vlan is still in use')

    # Delete vlan
    session.delete(vl)
    session.commit()


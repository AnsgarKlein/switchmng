from switchmng.schema import *

import switchmng.database
from switchmng.database.query import *

def delete_switch_model(resource_id):
    # Check switch model
    sm = query_switch_model(resource_id)
    if sm is None:
        raise ValueError('Given switch model does not exist')

    # Check if there are switches still using this model
    affected_sw = query_switches(model = resource_id)
    if type(affected_sw) is not list:
        raise TypeError('Expected list of switches to be of type list')
    if len(affected_sw) > 0:
        raise ValueError('Given switch model is still in use')

    # Delete switch model
    session = switchmng.database.Session()
    session.delete(sm)
    session.commit()

def delete_switch(resource_id):
    # Check switch
    sw = query_switch(resource_id)
    if sw is None:
        raise ValueError('Given switch does not exist')

    # Delete switch
    session = switchmng.database.Session()
    session.delete(sw)
    session.commit()

def delete_port_type(resource_id):
    # Check port type
    pt = query_port_type(resource_id)
    if pt is None:
        raise ValueError('Given port type does not exist')

    # Check if there are switch models still using this port type
    affected_sm = query_switch_models(port_type = resource_id)
    if type(affected_sm) is not list:
        raise TypeError('Expected list of switch models to be of type list')
    if len(affected_sm) > 0:
        raise ValueError('Given port type is still in use')

    # Delete port type
    session = switchmng.database.Session()
    session.delete(pt)
    session.commit()

def delete_vlan(resource_id):
    # Check vlan
    vl = query_vlan(resource_id)
    if vl is None:
        raise ValueError('Given vlan does not exist')

    # Check if there are switch ports still using this vlan
    affected_sw = query_switches(vlan = resource_id)
    if type(affected_sw) is not list:
        raise TypeError('Expected list of switches to be of type list')
    if len(affected_sw) > 0:
        raise ValueError('Given vlan is still in use')

    # Delete vlan
    session = switchmng.database.Session()
    session.delete(vl)
    session.commit()



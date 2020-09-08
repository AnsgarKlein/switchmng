from . import *

@restbp.route('/switch_models/<string:resource_id>', methods = ['DELETE'])
def delete_switch_model(resource_id):
    # Check if switch model exists
    sm = db.query_switch_model(resource_id)

    if sm is None:
        abort(404)

    # Delete from database
    try:
        db.delete_switch_model(resource_id)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'result': True,
             'data:': None }, 200

@restbp.route('/switches/<string:resource_id>', methods = ['DELETE'])
def delete_switch(resource_id):
    # Check if switch exists
    sw = db.query_switch(resource_id)

    if sw is None:
        abort(404)

    # Delete from database
    try:
        db.delete_switch(resource_id)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'result': True,
             'data:': None }, 200

@restbp.route('/port_types/<string:resource_id>', methods = ['DELETE'])
def delete_port_type(resource_id):
    # Check if port type exists
    pt = db.query_port_type(resource_id)

    if pt is None:
        abort(404)

    # Delete from database
    try:
        db.delete_port_type(resource_id)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'result': True,
             'data:': None }, 200

@restbp.route('/vlans/<int:resource_id>', methods = ['DELETE'])
def delete_vlan(resource_id):
    # Check if vlan exists
    vl = db.query_vlan(resource_id)

    if vl is None:
        abort(404)

    # Delete from database
    try:
        db.delete_vlan(resource_id)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'result': True,
             'data:': None }, 200


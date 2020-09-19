from flask import current_app

from . import *

@restbp.route('/switch_models/<string:resource_id>', methods = ['DELETE'])
def delete_switch_model(resource_id):
    db = current_app.config['SWITCHMNG_DB_CONNECTION']
    session = db.Session()

    # Check if switch model exists
    sm = database.query_switch_model(session, resource_id)

    if sm is None:
        abort(404)

    # Delete from database
    try:
        database.delete_switch_model(session, resource_id)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'result': True,
             'data:': None }, 200

@restbp.route('/switches/<string:resource_id>', methods = ['DELETE'])
def delete_switch(resource_id):
    db = current_app.config['SWITCHMNG_DB_CONNECTION']
    session = db.Session()

    # Check if switch exists
    sw = database.query_switch(session, resource_id)

    if sw is None:
        abort(404)

    # Delete from database
    try:
        database.delete_switch(session, resource_id)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'result': True,
             'data:': None }, 200

@restbp.route('/port_types/<string:resource_id>', methods = ['DELETE'])
def delete_port_type(resource_id):
    db = current_app.config['SWITCHMNG_DB_CONNECTION']
    session = db.Session()

    # Check if port type exists
    pt = database.query_port_type(session, resource_id)

    if pt is None:
        abort(404)

    # Delete from database
    try:
        database.delete_port_type(session, resource_id)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'result': True,
             'data:': None }, 200

@restbp.route('/vlans/<int:resource_id>', methods = ['DELETE'])
def delete_vlan(resource_id):
    db = current_app.config['SWITCHMNG_DB_CONNECTION']
    session = db.Session()

    # Check if vlan exists
    vl = database.query_vlan(session, resource_id)

    if vl is None:
        abort(404)

    # Delete from database
    try:
        database.delete_vlan(session, resource_id)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'result': True,
             'data:': None }, 200


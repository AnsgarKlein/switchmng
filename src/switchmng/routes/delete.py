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

    return { 'status': 200,
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

    return { 'status': 200,
             'data:': None }, 200

@restbp.route('/network_protocols/<string:resource_id>', methods = ['DELETE'])
def delete_network_protocol(resource_id):
    db = current_app.config['SWITCHMNG_DB_CONNECTION']
    session = db.Session()

    # Check if network protocol exists
    np = database.query_network_protocol(session, resource_id)

    if np is None:
        abort(404)

    # Delete from database
    try:
        database.delete_network_protocol(session, resource_id)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'status': 200,
             'data:': None }, 200

@restbp.route('/connectors/<string:resource_id>', methods = ['DELETE'])
def delete_connector(resource_id):
    db = current_app.config['SWITCHMNG_DB_CONNECTION']
    session = db.Session()

    # Check if network protocol exists
    cn = database.query_connector(session, resource_id)

    if cn is None:
        abort(404)

    # Delete from database
    try:
        database.delete_connector(session, resource_id)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'status': 200,
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

    return { 'status': 200,
             'data:': None }, 200


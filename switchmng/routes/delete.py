from flask import abort
from flask import current_app
from flask import request

from switchmng import database
from .blueprint import restbp
from .errors import *

@restbp.route('/switch_models/<string:resource_id>', methods = ['DELETE'])
def delete_switch_model(resource_id):
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

    # Check request
    if not request.accept_mimetypes.accept_json:
        return error_406(message = 'Content-Type application/json is not accepted by client')

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
             'data': None }, 200

@restbp.route('/switch_models/<string:switch_model_resource_id>/ports/<string:port_model_resource_id>', methods = ['DELETE'])
def delete_port_model(switch_model_resource_id, port_model_resource_id):
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

    # Check request
    if not request.accept_mimetypes.accept_json:
        return error_406(message = 'Content-Type application/json is not accepted by client')

    # Check if switch model exists
    sm = database.query_switch_model(session, switch_model_resource_id)
    if sm is None:
        abort(404)

    # Check if port model exists
    pm = sm.port(port_model_resource_id)
    if pm is None:
        abort(404)

    # Delete from database
    try:
        database.delete_port_model(session, switch_model_resource_id, port_model_resource_id)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'status': 200,
             'data': None }, 200

@restbp.route('/switches/<string:resource_id>', methods = ['DELETE'])
def delete_switch(resource_id):
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

    # Check request
    if not request.accept_mimetypes.accept_json:
        return error_406(message = 'Content-Type application/json is not accepted by client')

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
             'data': None }, 200

@restbp.route('/network_protocols/<string:resource_id>', methods = ['DELETE'])
def delete_network_protocol(resource_id):
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

    # Check request
    if not request.accept_mimetypes.accept_json:
        return error_406(message = 'Content-Type application/json is not accepted by client')

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
             'data': None }, 200

@restbp.route('/connectors/<string:resource_id>', methods = ['DELETE'])
def delete_connector(resource_id):
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

    # Check request
    if not request.accept_mimetypes.accept_json:
        return error_406(message = 'Content-Type application/json is not accepted by client')

    # Check if connector exists
    cn = database.query_connector(session, resource_id)
    if cn is None:
        abort(404)

    # Delete from database
    try:
        database.delete_connector(session, resource_id)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'status': 200,
             'data': None }, 200

@restbp.route('/vlans/<int:resource_id>', methods = ['DELETE'])
def delete_vlan(resource_id):
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

    # Check request
    if not request.accept_mimetypes.accept_json:
        return error_406(message = 'Content-Type application/json is not accepted by client')

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
             'data': None }, 200

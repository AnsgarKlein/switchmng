from flask import current_app

from . import *

@restbp.route('/switch_models/<string:resource_id>', methods = ['PATCH'])
def patch_switch_model(resource_id):
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

    # Check request
    if request.content_type != 'application/merge-patch+json':
        return error_415(message = 'Expected Content-Type to be application/merge-patch+json')
    if not request.accept_mimetypes.accept_json:
        return error_406(message = 'Content-Type application/json is not accepted by client')
    try:
        req = request.json
        if not isinstance(req, dict):
            raise BaseException()
    except:
        return error_400(message = 'Request is not a valid json object')

    # Check if switch model exists
    sm = database.query_switch_model(session, resource_id)
    if sm is None:
        abort(404)

    # Modify in database
    try:
        sm = database.modify_switch_model(session, resource_id = resource_id, **req)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'status': 200,
             'data': sm.jsonify() }, 200

@restbp.route('/switch_models/<string:switch_model_resource_id>/ports/<string:port_model_resource_id>', methods = ['PATCH'])
def patch_port_model(switch_model_resource_id, port_model_resource_id):
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

    # Check request
    if request.content_type != 'application/merge-patch+json':
        return error_415(message = 'Expected Content-Type to be application/merge-patch+json')
    if not request.accept_mimetypes.accept_json:
        return error_406(message = 'Content-Type application/json is not accepted by client')
    try:
        req = request.json
        if not isinstance(req, dict):
            raise BaseException()
    except:
        return error_400(message = 'Request is not a valid json object')

    # Check if port model exists
    pm = database.query_port_model(session,
                                   switch_model_resource_id,
                                   port_model_resource_id)
    if sm is None:
        abort(404)

    # Modify in database
    try:
        pm = database.modify_port_model(
            session,
            switch_model_resource_id = switch_model_resource_id,
            port_model_resource_id = port_model_resource_id,
            **req)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'status': 200,
             'data': pm.jsonify() }, 200

@restbp.route('/switches/<string:resource_id>', methods = ['PATCH'])
def patch_switch(resource_id):
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

    # Check request
    if request.content_type != 'application/merge-patch+json':
        return error_415(message = 'Expected Content-Type to be application/merge-patch+json')
    if not request.accept_mimetypes.accept_json:
        return error_406(message = 'Content-Type application/json is not accepted by client')
    try:
        req = request.json
        if not isinstance(req, dict):
            raise BaseException()
    except:
        return error_400(message = 'Request is not a valid json object')

    # Check if switch exists
    sw = database.query_switch(session, resource_id)
    if sw is None:
        abort(404)

    # Modify in database
    try:
        sw = database.modify_switch(session, resource_id = resource_id, **req)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'status': 200,
             'data': sw.jsonify() }, 200

@restbp.route('/switches/<string:switch_resource_id>/ports/<string:port_resource_id>', methods = ['PATCH'])
def patch_port(switch_resource_id, port_resource_id):
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

    # Check request
    if request.content_type != 'application/merge-patch+json':
        return error_415(message = 'Expected Content-Type to be application/merge-patch+json')
    if not request.accept_mimetypes.accept_json:
        return error_406(message = 'Content-Type application/json is not accepted by client')
    try:
        req = request.json
        if not isinstance(req, dict):
            raise BaseException()
    except:
        return error_400(message = 'Request is not a valid json object')

    # Check if port exists
    pt = database.query_port(session,
                             switch_resource_id,
                             port_resource_id)
    if pt is None:
        abort(404)

    # Modify in database
    try:
        pt = database.modify_port(
            session,
            switch_resource_id = switch_resource_id,
            port_resource_id = port_resource_id,
            **req)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'status': 200,
             'data': pt.jsonify() }, 200

@restbp.route('/network_protocols/<string:resource_id>', methods = ['PATCH'])
def patch_network_protocols(resource_id):
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

    # Check request
    if request.content_type != 'application/merge-patch+json':
        return error_415(message = 'Expected Content-Type to be application/merge-patch+json')
    if not request.accept_mimetypes.accept_json:
        return error_406(message = 'Content-Type application/json is not accepted by client')
    try:
        req = request.json
        if not isinstance(req, dict):
            raise BaseException()
    except:
        return error_400(message = 'Request is not a valid json object')

    # Check if network protocol exists
    np = database.query_network_protocol(session, resource_id)
    if np is None:
        abort(404)

    # Modify in database
    try:
        np = database.modify_network_protocol(session, resource_id = resource_id, **req)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'status': 200,
             'data': np.jsonify() }, 200

@restbp.route('/connectors/<string:resource_id>', methods = ['PATCH'])
def patch_connector(resource_id):
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

    # Check request
    if request.content_type != 'application/merge-patch+json':
        return error_415(message = 'Expected Content-Type to be application/merge-patch+json')
    if not request.accept_mimetypes.accept_json:
        return error_406(message = 'Content-Type application/json is not accepted by client')
    try:
        req = request.json
        if not isinstance(req, dict):
            raise BaseException()
    except:
        return error_400(message = 'Request is not a valid json object')

    # Check if connector exists
    cn = database.query_connector(session, resource_id)
    if cn is None:
        abort(404)

    # Modify in database
    try:
        cn = database.modify_connector(session, resource_id = resource_id, **req)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'status': 200,
             'data': cn.jsonify() }, 200

@restbp.route('/vlans/<int:resource_id>', methods = ['PATCH'])
def patch_vlan(resource_id):
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

    # Check request
    if request.content_type != 'application/merge-patch+json':
        return error_415(message = 'Expected Content-Type to be application/merge-patch+json')
    if not request.accept_mimetypes.accept_json:
        return error_406(message = 'Content-Type application/json is not accepted by client')
    try:
        req = request.json
        if not isinstance(req, dict):
            raise BaseException()
    except:
        return error_400(message = 'Request is not a valid json object')

    # Check if vlan exists
    vl = database.query_vlan(session, resource_id)
    if vl is None:
        abort(404)

    # Modify in database
    try:
        vl = database.modify_vlan(session, resource_id = resource_id, **req)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'status': 200,
             'data': vl.jsonify() }, 200


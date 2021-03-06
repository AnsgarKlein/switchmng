from flask import current_app
from flask import request

from switchmng.typing import FlaskResponse

from switchmng import database
from .blueprint import restbp
from .errors import *

@restbp.route('/switch_models/<string:resource_id>', methods = ['PUT'])
def put_switch_model(resource_id: str) -> FlaskResponse:
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

    # Check request
    if request.content_type != 'application/json':
        return error_415(message = 'Expected Content-Type to be application/json')
    if not request.accept_mimetypes.accept_json:
        return error_406(message = 'Content-Type application/json is not accepted by client')
    try:
        req = request.json
        if not isinstance(req, dict):
            raise BaseException()
    except:
        return error_400(message = 'Request is not a valid json object')

    # Set in database
    try:
        sm = database.set_switch_model(session, resource_id = resource_id, **req)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'status': 200,
             'data': sm.jsonify() }, 200

@restbp.route('/switch_models/<string:switch_model_resource_id>/ports/<string:port_model_resource_id>', methods = ['PUT'])
def put_port_model(
        switch_model_resource_id: str,
        port_model_resource_id: str) -> FlaskResponse:
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

    # Check request
    if request.content_type != 'application/json':
        return error_415(message = 'Expected Content-Type to be application/json')
    if not request.accept_mimetypes.accept_json:
        return error_406(message = 'Content-Type application/json is not accepted by client')
    try:
        req = request.json
        if not isinstance(req, dict):
            raise BaseException()
    except:
        return error_400(message = 'Request is not a valid json object')

    # Set in database
    try:
        pm = database.set_port_model(
            session,
            switch_model_resource_id = switch_model_resource_id,
            port_model_resource_id = port_model_resource_id,
            **req)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'status': 200,
             'data': pm.jsonify() }, 200

@restbp.route('/switches/<string:resource_id>', methods = ['PUT'])
def put_switch(resource_id: str) -> FlaskResponse:
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

    # Check request
    if request.content_type != 'application/json':
        return error_415(message = 'Expected Content-Type to be application/json')
    if not request.accept_mimetypes.accept_json:
        return error_406(message = 'Content-Type application/json is not accepted by client')
    try:
        req = request.json
        if not isinstance(req, dict):
            raise BaseException()
    except:
        return error_400(message = 'Request is not a valid json object')

    # Set in database
    try:
        sw = database.set_switch(session, resource_id = resource_id, **req)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'status': 200,
             'data': sw.jsonify() }, 200

@restbp.route('/switches/<string:switch_resource_id>/ports/<string:port_resource_id>', methods = ['PUT'])
def put_port(switch_resource_id: str, port_resource_id: str) -> FlaskResponse:
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

    # Check request
    if request.content_type != 'application/json':
        return error_415(message = 'Expected Content-Type to be application/json')
    if not request.accept_mimetypes.accept_json:
        return error_406(message = 'Content-Type application/json is not accepted by client')
    try:
        req = request.json
        if not isinstance(req, dict):
            raise BaseException()
    except:
        return error_400(message = 'Request is not a valid json object')

    # Set in database
    try:
        pt = database.set_port(
            session,
            switch_resource_id = switch_resource_id,
            port_resource_id = port_resource_id,
            **req)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'status': 200,
             'data': pt.jsonify() }, 200

@restbp.route('/network_protocols/<string:resource_id>', methods = ['PUT'])
def put_network_protocols(resource_id: str) -> FlaskResponse:
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

    # Check request
    if request.content_type != 'application/json':
        return error_415(message = 'Expected Content-Type to be application/json')
    if not request.accept_mimetypes.accept_json:
        return error_406(message = 'Content-Type application/json is not accepted by client')
    try:
        req = request.json
        if not isinstance(req, dict):
            raise BaseException()
    except:
        return error_400(message = 'Request is not a valid json object')

    # Set in database
    try:
        np = database.set_network_protocol(session, resource_id = resource_id, **req)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'status': 200,
             'data': np.jsonify() }, 200

@restbp.route('/connectors/<string:resource_id>', methods = ['PUT'])
def put_connector(resource_id: str) -> FlaskResponse:
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

    # Check request
    if request.content_type != 'application/json':
        return error_415(message = 'Expected Content-Type to be application/json')
    if not request.accept_mimetypes.accept_json:
        return error_406(message = 'Content-Type application/json is not accepted by client')
    try:
        req = request.json
        if not isinstance(req, dict):
            raise BaseException()
    except:
        return error_400(message = 'Request is not a valid json object')

    # Set in database
    try:
        cn = database.set_connector(session, resource_id = resource_id, **req)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'status': 200,
             'data': cn.jsonify() }, 200

@restbp.route('/vlans/<int:resource_id>', methods = ['PUT'])
def put_vlan(resource_id: str) -> FlaskResponse:
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

    # Check request
    if request.content_type != 'application/json':
        return error_415(message = 'Expected Content-Type to be application/json')
    if not request.accept_mimetypes.accept_json:
        return error_406(message = 'Content-Type application/json is not accepted by client')
    try:
        req = request.json
        if not isinstance(req, dict):
            raise BaseException()
    except:
        return error_400(message = 'Request is not a valid json object')

    # Set in database
    try:
        vl = database.set_vlan(session, resource_id = resource_id, **req)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'status': 200,
             'data': vl.jsonify() }, 200

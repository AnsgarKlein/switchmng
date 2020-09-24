from flask import current_app
from flask import abort
from flask import request

from switchmng import database
from .blueprint import restbp
from .errors import *

@restbp.route('/switch_models/<string:resource_id>', methods = ['GET'])
def get_switch_model(resource_id):
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

    # Check if switch model exists
    sm = database.query_switch_model(session, resource_id)
    if sm is None:
        abort(404)

    return { 'status': 200,
             'data': sm.jsonify() }, 200

@restbp.route('/switch_models/<string:switch_model_resource_id>/ports/<string:port_model_resource_id>', methods = ['GET'])
def get_port_model(switch_model_resource_id, port_model_resource_id):
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

    # Check if switch model exists
    sm = database.query_switch_model(session, switch_model_resource_id)
    if sm is None:
        abort(404)

    # Check if port model exists
    pm = sm.port(port_model_resource_id)
    if pm is None:
        abort(404)

    return { 'status': 200,
             'data': pm.jsonify() }, 200

@restbp.route('/switches/<string:resource_id>', methods = ['GET'])
def get_switch(resource_id):
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

    # Check if switch exists
    sw = database.query_switch(session, resource_id)
    if sw is None:
        abort(404)

    return { 'status': 200,
             'data': sw.jsonify() }, 200

@restbp.route('/switches/<string:switch_resource_id>/ports/<string:port_resource_id>', methods = ['GET'])
def get_port(switch_resource_id, port_resource_id):
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

    # Check if switch exists
    sw = database.query_switch(session, switch_resource_id)
    if sw is None:
        abort(404)

    # Check if port exists
    pt = sw.port(port_resource_id)
    if pt is None:
        abort(404)

    return { 'status': 200,
             'data': pt.jsonify() }, 200

@restbp.route('/network_protocols/<string:resource_id>', methods = ['GET'])
def get_network_protocol(resource_id):
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

    # Check if network protocol exists
    np = database.query_network_protocol(session, resource_id)
    if np is None:
        abort(404)

    return { 'status': 200,
             'data': np.jsonify() }, 200

@restbp.route('/connectors/<string:resource_id>', methods = ['GET'])
def get_connector(resource_id):
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

    # Check if connector exists
    cn = database.query_connector(session, resource_id)
    if cn is None:
        abort(404)

    return { 'status': 200,
             'data': cn.jsonify() }, 200

@restbp.route('/vlans/<int:resource_id>', methods = ['GET'])
def get_vlan(resource_id):
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

    # Check if vlan exists
    vl = database.query_vlan(session, resource_id)
    if vl is None:
        abort(404)

    return { 'status': 200,
             'data': vl.jsonify() }, 200

@restbp.route('/switch_models', methods = ['GET'])
def get_switch_models():
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

    return { 'status': 200,
             'data': [ sm.jsonify() for sm in database.query_switch_models(session) ] }, 200

@restbp.route('/switch_models/<string:switch_model_resource_id>/ports', methods = ['GET'])
def get_port_models(switch_model_resource_id):
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

    # Check if switch model exists
    sm = database.query_switch_model(session, switch_model_resource_id)
    if sm is None:
        abort(404)

    return { 'status': 200,
             'data': [ pm.jsonify()
                       for pm in
                       database.query_port_models(session, switch_model_resource_id) ] }, 200

@restbp.route('/switches', methods = ['GET'])
def get_switches():
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

    return { 'status': 200,
             'data': [ sw.jsonify() for sw in database.query_switches(session) ] }, 200

@restbp.route('/switches/<string:switch_resource_id>/ports', methods = ['GET'])
def get_ports(switch_resource_id):
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

    # Check if switch exists
    sw = database.query_switch(session, switch_resource_id)
    if sw is None:
        abort(404)

    return { 'status': 200,
             'data': [ pt.jsonify()
                       for pt in
                       database.query_ports(session, switch_resource_id) ] }, 200

@restbp.route('/network_protocols', methods = ['GET'])
def get_network_protocols():
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

    return { 'status': 200,
             'data': [ np.jsonify() for np in database.query_network_protocols(session) ] }, 200

@restbp.route('/connectors', methods = ['GET'])
def get_connectors():
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

    return { 'status': 200,
             'data': [ cn.jsonify() for cn in database.query_connectors(session) ] }, 200

@restbp.route('/vlans', methods = ['GET'])
def get_vlans():
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

    return { 'status': 200,
             'data': [ vl.jsonify() for vl in database.query_vlans(session) ] }, 200

from flask import current_app

from . import *

@restbp.route('/switch_models/<string:resource_id>', methods = ['GET'])
def get_switch_model(resource_id):
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

    sm = database.query_switch_model(session, resource_id)
    if sm is None:
        abort(404)

    return { 'status': 200,
             'data': sm.jsonify() }, 200

@restbp.route('/switch_models/<string:switch_model_resource_id>/ports/<string:port_model_resource_id>', methods = ['GET'])
def get_port_model(switch_model_resource_id, port_model_resource_id):
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

    sm = database.query_switch_model(session, switch_model_resource_id)
    if sm is None:
        abort(404)
    pm = sm.port(port_model_resource_id)
    if pm is None:
        abort(404)

    return { 'status': 200,
             'data': pm.jsonify() }, 200

@restbp.route('/switches/<string:resource_id>', methods = ['GET'])
def get_switch(resource_id):
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

    sw = database.query_switch(session, resource_id)
    if sw is None:
        abort(404)

    return { 'status': 200,
             'data': sw.jsonify() }, 200

@restbp.route('/network_protocols/<string:resource_id>', methods = ['GET'])
def get_network_protocol(resource_id):
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

    np = database.query_network_protocol(session, resource_id)
    if np is None:
        abort(404)

    return { 'status': 200,
             'data': np.jsonify() }, 200

@restbp.route('/connectors/<string:resource_id>', methods = ['GET'])
def get_connector(resource_id):
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

    cn = database.query_connector(session, resource_id)
    if cn is None:
        abort(404)

    return { 'status': 200,
             'data': cn.jsonify() }, 200

@restbp.route('/vlans/<int:resource_id>', methods = ['GET'])
def get_vlan(resource_id):
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

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

    return { 'status': 200,
             'data': [ pm.jsonify()
                       for pm in
                       database.query_port_models(session, switch_model_resource_id) ] }, 200

@restbp.route('/switches', methods = ['GET'])
def get_switches():
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

    return { 'status': 200,
             'data': [ sw.jsonify() for sw in database.query_switches(session) ] }, 200

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


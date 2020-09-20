from flask import current_app

from . import *

@restbp.route('/switch_models/<string:resource_id>', methods = ['GET'])
def get_switch_model(resource_id):
    db = current_app.config['SWITCHMNG_DB_CONNECTION']
    session = db.Session()

    sm = database.query_switch_model(session, resource_id)
    if sm is None:
        abort(404)

    return { 'status': 200,
             'data': sm.jsonify() }, 200

@restbp.route('/switches/<string:resource_id>', methods = ['GET'])
def get_switch(resource_id):
    db = current_app.config['SWITCHMNG_DB_CONNECTION']
    session = db.Session()

    sw = database.query_switch(session, resource_id)
    if sw is None:
        abort(404)

    return { 'status': 200,
             'data': sw.jsonify() }, 200

@restbp.route('/network_protocols/<string:resource_id>', methods = ['GET'])
def get_network_protocol(resource_id):
    db = current_app.config['SWITCHMNG_DB_CONNECTION']
    session = db.Session()

    np = database.query_network_protocol(session, resource_id)
    if np is None:
        abort(404)

    return { 'status': 200,
             'data': np.jsonify() }, 200

@restbp.route('/connectors/<string:resource_id>', methods = ['GET'])
def get_connector(resource_id):
    db = current_app.config['SWITCHMNG_DB_CONNECTION']
    session = db.Session()

    cn = database.query_connector(session, resource_id)
    if cn is None:
        abort(404)

    return { 'status': 200,
             'data': cn.jsonify() }, 200

@restbp.route('/vlans/<int:resource_id>', methods = ['GET'])
def get_vlan(resource_id):
    db = current_app.config['SWITCHMNG_DB_CONNECTION']
    session = db.Session()

    vl = database.query_vlan(session, resource_id)
    if vl is None:
        abort(404)

    return { 'status': 200,
             'data': vl.jsonify() }, 200

@restbp.route('/switch_models', methods = ['GET'])
def get_switch_models():
    db = current_app.config['SWITCHMNG_DB_CONNECTION']
    session = db.Session()
    return { 'status': 200,
             'data': [ sm.jsonify() for sm in database.query_switch_models(session) ] }, 200

@restbp.route('/switches', methods = ['GET'])
def get_switches():
    db = current_app.config['SWITCHMNG_DB_CONNECTION']
    session = db.Session()
    return { 'status': 200,
             'data': [ sw.jsonify() for sw in database.query_switches(session) ] }, 200

@restbp.route('/network_protocols', methods = ['GET'])
def get_network_protocols():
    db = current_app.config['SWITCHMNG_DB_CONNECTION']
    session = db.Session()
    return { 'status': 200,
             'data': [ np.jsonify() for np in database.query_network_protocols(session) ] }, 200

@restbp.route('/connectors', methods = ['GET'])
def get_connectors():
    db = current_app.config['SWITCHMNG_DB_CONNECTION']
    session = db.Session()
    return { 'status': 200,
             'data': [ cn.jsonify() for cn in database.query_connectors(session) ] }, 200

@restbp.route('/vlans', methods = ['GET'])
def get_vlans():
    db = current_app.config['SWITCHMNG_DB_CONNECTION']
    session = db.Session()
    return { 'status': 200,
             'data': [ vl.jsonify() for vl in database.query_vlans(session) ] }, 200


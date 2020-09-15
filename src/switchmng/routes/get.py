from . import *

@restbp.route('/switch_models/<string:resource_id>', methods = ['GET'])
def get_switch_model(resource_id):
    sm = database.query_switch_model(resource_id)

    if sm is None:
        abort(404)

    return { 'result': True,
             'data': sm.jsonify() }, 200

@restbp.route('/switches/<string:resource_id>', methods = ['GET'])
def get_switch(resource_id):
    sw = database.query_switch(resource_id)

    if sw is None:
        abort(404)

    return { 'result': True,
             'data': sw.jsonify() }, 200

@restbp.route('/port_types/<string:resource_id>', methods = ['GET'])
def get_port_type(resource_id):
    pt = database.query_port_type(resource_id)

    if pt is None:
        abort(404)

    return { 'result': True,
             'data': pt.jsonify() }, 200

@restbp.route('/vlans/<int:resource_id>', methods = ['GET'])
def get_vlan(resource_id):
    vl = database.query_vlan(resource_id)

    if vl is None:
        abort(404)

    return { 'result': True,
             'data': vl.jsonify() }, 200

@restbp.route('/switch_models', methods = ['GET'])
def get_switch_models():
    return { 'result': True,
             'data': [ sm.jsonify() for sm in database.query_switch_models() ] }, 200

@restbp.route('/switches', methods = ['GET'])
def get_switches():
    return { 'result': True,
             'data': [ sw.jsonify() for sw in database.query_switches() ] }, 200

@restbp.route('/port_types', methods = ['GET'])
def get_port_types():
    return { 'result': True,
             'data': [ pt.jsonify() for pt in database.query_port_types() ] }, 200

@restbp.route('/vlans', methods = ['GET'])
def get_vlans():
    return { 'result': True,
             'data': [ vl.jsonify() for vl in database.query_vlans() ] }, 200


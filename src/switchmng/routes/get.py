from flask import current_app

from . import *

def _configure_get(app):
    @app.route('/switch_models/<string:resource_id>', methods = ['GET'])
    def get_switch_model(resource_id):
        db = current_app.config['SWITCHMNG_DB_CONNECTION']
        session = db.Session()

        sm = database.query_switch_model(session, resource_id)
        if sm is None:
            abort(404)

        return { 'result': True,
                 'data': sm.jsonify() }, 200

    @app.route('/switches/<string:resource_id>', methods = ['GET'])
    def get_switch(resource_id):
        db = current_app.config['SWITCHMNG_DB_CONNECTION']
        session = db.Session()

        sw = database.query_switch(session, resource_id)
        if sw is None:
            abort(404)

        return { 'result': True,
                 'data': sw.jsonify() }, 200

    @app.route('/port_types/<string:resource_id>', methods = ['GET'])
    def get_port_type(resource_id):
        db = current_app.config['SWITCHMNG_DB_CONNECTION']
        session = db.Session()

        pt = database.query_port_type(session, resource_id)
        if pt is None:
            abort(404)

        return { 'result': True,
                 'data': pt.jsonify() }, 200

    @app.route('/vlans/<int:resource_id>', methods = ['GET'])
    def get_vlan(resource_id):
        db = current_app.config['SWITCHMNG_DB_CONNECTION']
        session = db.Session()

        vl = database.query_vlan(session, resource_id)
        if vl is None:
            abort(404)

        return { 'result': True,
                 'data': vl.jsonify() }, 200

    @app.route('/switch_models', methods = ['GET'])
    def get_switch_models():
        db = current_app.config['SWITCHMNG_DB_CONNECTION']
        session = db.Session()
        return { 'result': True,
                 'data': [ sm.jsonify() for sm in database.query_switch_models(session) ] }, 200

    @app.route('/switches', methods = ['GET'])
    def get_switches():
        db = current_app.config['SWITCHMNG_DB_CONNECTION']
        session = db.Session()
        return { 'result': True,
                 'data': [ sw.jsonify() for sw in database.query_switches(session) ] }, 200

    @app.route('/port_types', methods = ['GET'])
    def get_port_types():
        db = current_app.config['SWITCHMNG_DB_CONNECTION']
        session = db.Session()
        return { 'result': True,
                 'data': [ pt.jsonify() for pt in database.query_port_types(session) ] }, 200

    @app.route('/vlans', methods = ['GET'])
    def get_vlans():
        db = current_app.config['SWITCHMNG_DB_CONNECTION']
        session = db.Session()
        return { 'result': True,
                 'data': [ vl.jsonify() for vl in database.query_vlans(session) ] }, 200


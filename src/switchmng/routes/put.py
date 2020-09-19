from flask import current_app

from . import *

def _configure_put(app):
    @app.route('/switch_models/<string:resource_id>', methods = ['PUT'])
    def put_switch_model(resource_id):
        db = current_app.config['SWITCHMNG_DB_CONNECTION']
        session = db.Session()

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

        # Modify in database
        try:
            sm = database.set_switch_model(session, resource_id = resource_id, **req)
        except BaseException as e:
            return error_400(message = str(e))

        return { 'result': True,
                 'data:': sm.jsonify() }, 200

    @app.route('/switches/<string:resource_id>', methods = ['PUT'])
    def put_switch(resource_id):
        db = current_app.config['SWITCHMNG_DB_CONNECTION']
        session = db.Session()

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

        # Modify in database
        try:
            sw = database.set_switch(session, resource_id = resource_id, **req)
        except BaseException as e:
            return error_400(message = str(e))

        return { 'result': True,
                 'data:': sw.jsonify() }, 200

    @app.route('/port_types/<string:resource_id>', methods = ['PUT'])
    def put_port_type(resource_id):
        db = current_app.config['SWITCHMNG_DB_CONNECTION']
        session = db.Session()

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

        # Modify in database
        try:
            pt = database.set_port_type(session, resource_id = resource_id, **req)
        except BaseException as e:
            return error_400(message = str(e))

        return { 'result': True,
                 'data:': pt.jsonify() }, 200

    @app.route('/vlans/<int:resource_id>', methods = ['PUT'])
    def put_vlan(resource_id):
        db = current_app.config['SWITCHMNG_DB_CONNECTION']
        session = db.Session()

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

        # Modify in database
        try:
            vl = database.set_vlan(session, resource_id = resource_id, **req)
        except BaseException as e:
            return error_400(message = str(e))

        return { 'result': True,
                 'data:': vl.jsonify() }, 200


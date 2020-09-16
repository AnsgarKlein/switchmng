from . import *

def _configure_patch(app, database):
    @app.route('/switch_models/<string:resource_id>', methods = ['PATCH'])
    def patch_switch_model(resource_id):
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

        # Modify in database
        try:
            sm = database.modify_switch_model(resource_id = resource_id, **req)
        except BaseException as e:
            return error_400(message = str(e))

        return { 'result': True,
                 'data:': sm.jsonify() }, 200

    @app.route('/switches/<string:resource_id>', methods = ['PATCH'])
    def patch_switch(resource_id):
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

        # Modify in database
        try:
            sw = database.modify_switch(resource_id = resource_id, **req)
        except BaseException as e:
            return error_400(message = str(e))

        return { 'result': True,
                 'data:': sw.jsonify() }, 200

    @app.route('/port_types/<string:resource_id>', methods = ['PATCH'])
    def patch_port_type(resource_id):
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

        # Modify in database
        try:
            pt = database.modify_port_type(resource_id = resource_id, **req)
        except BaseException as e:
            return error_400(message = str(e))

        return { 'result': True,
                 'data:': pt.jsonify() }, 200

    @app.route('/vlans/<int:resource_id>', methods = ['PATCH'])
    def patch_vlan(resource_id):
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

        # Modify in database
        try:
            vl = database.modify_vlan(resource_id = resource_id, **req)
        except BaseException as e:
            return error_400(message = str(e))

        return { 'result': True,
                 'data:': vl.jsonify() }, 200


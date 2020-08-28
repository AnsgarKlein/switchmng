from database import DatabaseConnection

from flask import Flask
from flask import abort
from flask import request

app = Flask('REST API')

@app.route('/')
def hello_world():
    str = '''
        Welcome<br>
        <br>
        Menu:<br>
        <ul>
        <li>/switches</li>
        <li>/switch_models</li>
        <li>/port_types</li>
        <li>/vlans</li>
        </ul>
        '''
    return str

@app.errorhandler(404)
def error404(error):
    return { 'data': None,
             'result': False,
             'error': 404,
             'message': 'Not found' }

@app.route('/switch_models/<string:model_id>', methods = ['GET'])
def get_switch_model(model_id):
    db = DatabaseConnection()
    model = db.query_switch_model(model_id)

    if model is None:
        abort(404)

    return { 'result': True,
             'data': model.jsonify() }

@app.route('/switches/<string:switch_id>', methods = ['GET'])
def get_switch(switch_id):
    db = DatabaseConnection()
    switch = db.query_switch(switch_id)

    if switch is None:
        abort(404)

    return { 'result': True,
             'data': switch.jsonify() }

@app.route('/port_types/<string:port_type_id>', methods = ['GET'])
def get_port_type(port_type_id):
    db = DatabaseConnection()
    port_type = db.query_port_type(port_type_id)

    if port_type is None:
        abort(404)

    return { 'result': True,
             'data': port_type.jsonify() }

@app.route('/vlans/<int:vlan_id>')
def get_vlan(vlan_id):
    db = DatabaseConnection()
    vlan = db.query_vlan(vlan_id)

    if vlan is None:
        abort(404)

    return { 'result': True,
             'data': vlan.jsonify() }

@app.route('/switch_models', methods = ['GET'])
def get_switch_models():
    db = DatabaseConnection()
    return { 'result': True,
             'data': [ m.jsonify() for m in db.query_switch_models() ] }

@app.route('/switches', methods = ['GET'])
def get_switches():
    db = DatabaseConnection()
    return { 'result': True,
             'data': [ sw.jsonify() for sw in db.query_switches() ] }

@app.route('/port_types', methods = ['GET'])
def get_port_types():
    db = DatabaseConnection()
    return { 'result': True,
             'data': [ pt.jsonify() for pt in db.query_port_types() ] }

@app.route('/vlans', methods = ['GET'])
def get_vlans():
    db = DatabaseConnection()
    return { 'result': True,
             'data': [ v.jsonify() for v in db.query_vlans() ] }

@app.route('/switches', methods = ['POST'])
def add_switch():
    # Unpack request
    req = request.json
    if req is None or 'name' not in req:
        abort(400)
    name = req.pop('name')

    print('POST: {}  {} '.format(name, req))

    # Add to database
    db = DatabaseConnection()
    #db.

    # TODO: Call add_switch(name, **req)

    pass

if __name__ == '__main__':
    app.run(debug= True, host = '127.0.0.1', port = 8000)


import json

default_headers = {
    'Content-Type': 'application/json',
    'Accept':       'application/json',
}

patch_headers = {
    'Content-Type': 'application/merge-patch+json',
    'Accept':       'application/json',
}

def _add(client, url, data):
    rv = client.post(
        url,
        data = data,
        headers = default_headers)
    assert(rv.status_code == 201)

def setUp_vlans(client):
    vlans = [
        { 'tag': 1, 'description': 'VLAN_ONE' },
        { 'tag': 2, 'description': 'VLAN_TWO' },
    ]
    for vlan in vlans:
        _add(client, '/vlans', json.dumps(vlan))

def setUp_connectors(client):
    connectors = [
        { 'name': 'rj11' },
        { 'name': 'rj45' },
    ]
    for connector in connectors:
        _add(client, '/connectors', json.dumps(connector))

def setUp_network_protocols(client):
    protocols = [
        { 'name': 'proto1', 'speed': 100 },
        { 'name': 'proto2', 'speed': 200 },
    ]
    for protocol in protocols:
        _add(client, '/network_protocols', json.dumps(protocol))

def setUp_switch_models(client):
    models = [
        {
            'name':  'big_switch',
            'size':  4,
            'ports': [
                {
                    'name': 'p1',
                    'network_protocols': [ 'proto1', 'proto2' ],
                    'connector': 'rj45'
                },
                {
                    'name': 'p2',
                    'network_protocols': [ 'proto1' ],
                    'connector': 'rj45'
                },
                {
                    'name': 'p3',
                    'network_protocols': [ 'proto2' ],
                    'connector': 'rj45'
                },
                {
                    'name': 'p4',
                    'network_protocols': [ ],
                    'connector': 'rj45'
                },
            ],
        },
        {
            'name':  'small_switch',
            'size':  1,
            'ports': [
                {
                    'name': 'p1',
                    'network_protocols': [ 'proto1', 'proto2' ],
                    'connector': 'rj11'
                },
            ],
        }
    ]

    for model in models:
        _add(client, '/switch_models', json.dumps(model))

def setUp_switches(client):
    switches = [
        {
            'name':     'switch1',
            'model':    'small_switch',
            'ports':    [
                {
                    'name':   'p1',
                    'target': 'Saturn',
                    'vlans':  [ 1 ],
                },
            ],
            'location': 12,
            'ip':       '192.168.0.50',
        },
        {
            'name':     'switch2',
            'model':    'big_switch',
            'ports':    [
                {
                    'name':   'p1',
                    'target': 'Mars',
                    'vlans':  [ 1, 2 ],
                },
                {
                    'name':   'p3',
                    'target': 'Jupiter',
                    'vlans':  [ ],
                },
                {
                    'name':   'p4',
                    'target': 'Mercury',
                    'vlans':  [ 2 ],
                },
            ],
            'location': 5,
            'ip':       '192.168.0.100',
        },
    ]

    for switch in switches:
        _add(client, '/switches', json.dumps(switch))

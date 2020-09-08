#!/bin/env python3

import pprint

import json

import switchmng.database as db

def input_examples():
    # Create vlans
    db.add_vlan(tag = 1005, description = 'internal')
    db.add_vlan(tag = 107, description = 'guest')

    # Create port types
    pts = [
      { 'description': '100BASE-TX', 'speed': 100  },
      { 'description': '1000BASE-T', 'speed': 1000 },
      { 'description': '1000BASE-X', 'speed': 1000 }
    ]
    for pt in pts:
        db.add_port_type(description = pt['description'], speed = pt['speed'])


    # Create switch model1
    ps = [{ 'name': 'TP{:02}'.format(i + 1), 'port_type': '1000BASE-T' } for i in range(24)]
    for i in range(4):
        ps.append({ 'name': 'F{:02}'.format(i + 1), 'port_type': '1000BASE-X' })
    db.add_switch_model(name = 'ZyXEL GS1910-24', size = 1, ports = ps)


    # Create switch model2
    ps = [{ 'name': 'TP{:02}'.format(i + 1), 'port_type': '1000BASE-T' } for i in range(20)]
    db.add_switch_model(name = 'defect ZyXEL GS1910-24', ports = ps)
    pprint.PrettyPrinter(indent=4).pprint(db.query_switch_model('defect ZyXEL GS1910-24').jsonify())
    db.modify_switch_model(resource_id = 'defect ZyXEL GS1910-24', size = 1)
    pprint.PrettyPrinter(indent=4).pprint(db.query_switch_model('defect ZyXEL GS1910-24').jsonify())


    # Create switch
    ports_str = [
      { 'name': 'TP01', 'vlans': [ 1005 ] },
      { 'name': 'TP02', 'vlans': [ 1005 ] },
      { 'name': 'TP03', 'vlans': [ 107 ] },
      { 'name': 'TP04', 'vlans': [ 1005, 107 ] },
      { 'name': 'TP06', 'vlans': [ 107 ] },
      { 'name': 'F02',  'vlans': [ 107 ] }
    ]
    db.add_switch(name = 'switch1', model = 'ZyXEL GS1910-24', ports = ports_str)

    for sw in db.query_switches():
        pprint.PrettyPrinter(indent=4).pprint(sw.jsonify())


    # Change switch model
    db.modify_switch(resource_id = 'switch1', model = 'defect ZyXEL GS1910-24')

    for sw in db.query_switches():
        pprint.PrettyPrinter(indent=4).pprint(sw.jsonify())


    # Modify switch ports
    ports_str = [
      { 'name': 'TP01', 'vlans': [ ] },
      { 'name': 'TP02', 'vlans': [ ] },
      { 'name': 'TP03', 'vlans': [ ] },
      { 'name': 'TP04', 'vlans': [ ] },
      { 'name': 'TP06', 'vlans': [ ] },
      { 'name': 'TP10', 'vlans': [ 1005 ] },
      { 'name': 'TP11', 'vlans': [ 1005 ] },
      { 'name': 'TP12', 'vlans': [ 107 ] },
      { 'name': 'TP13', 'vlans': [ 1005, 107 ] },
      { 'name': 'TP16', 'vlans': [ 1005 ] }
    ]
    db.modify_switch(resource_id = 'switch1', ports = ports_str)

    for sw in db.query_switches():
        pprint.PrettyPrinter(indent=4).pprint(sw.jsonify())

if __name__ == '__main__':
    input_examples()


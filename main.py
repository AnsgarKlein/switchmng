#!/bin/env python3

import pprint

import json

from database import Database

def input_examples():
    database = Database()

    # Create vlans
    database.add_vlan(tag = 1005, description = 'internal')
    database.add_vlan(tag = 107, description = 'guest')

    # Create port types
    pts = [
      { 'description': '100BASE-TX', 'speed': 100  },
      { 'description': '1000BASE-T', 'speed': 1000 },
      { 'description': '1000BASE-X', 'speed': 1000 }
    ]
    for pt in pts:
        database.add_port_type(description = pt['description'], speed = pt['speed'])


    # Create switch model1
    ps = [{ 'name': 'TP{}'.format(i + 1), 'port_type': '1000BASE-T' } for i in range(24)]
    for i in range(4):
        ps.append({ 'name': 'F{}'.format(i + 1), 'port_type': '1000BASE-X' })
    database.add_switch_model(name = 'ZyXEL GS1910-24', size = 1, ports = ps)


    # Create switch model2
    ps = [{ 'name': 'TP{}'.format(i + 1), 'port_type': '1000BASE-T' } for i in range(20)]
    database.add_switch_model(name = 'defect ZyXEL GS1910-24', ports = ps)
    pprint.PrettyPrinter(indent=4).pprint(database.query_switch_model('defect ZyXEL GS1910-24').jsonify())
    database.modify_switch_model(name = 'defect ZyXEL GS1910-24', size = 1)
    pprint.PrettyPrinter(indent=4).pprint(database.query_switch_model('defect ZyXEL GS1910-24').jsonify())


    # Create switch
    ports_str = [
      { 'name': 'TP1', 'vlans': [ 1005 ] },
      { 'name': 'TP2', 'vlans': [ 1005 ] },
      { 'name': 'TP3', 'vlans': [ 107 ] },
      { 'name': 'TP4', 'vlans': [ 1005, 107 ] },
      { 'name': 'TP6', 'vlans': [ 107 ] },
      { 'name': 'F2',  'vlans': [ 107 ] }
    ]
    database.add_switch(name = 'switch1', model = 'ZyXEL GS1910-24', port_maps = ports_str)

    for sw in database.query_switches():
        pprint.PrettyPrinter(indent=4).pprint(sw.jsonify())


    # Change switch model
    database.modify_switch('switch1', model = 'defect ZyXEL GS1910-24')

    for sw in database.query_switches():
        pprint.PrettyPrinter(indent=4).pprint(sw.jsonify())


    # Modify switch ports
    ports_str = [
      { 'name': 'TP1', 'vlans': [ ] },
      { 'name': 'TP2', 'vlans': [ ] },
      { 'name': 'TP3', 'vlans': [ ] },
      { 'name': 'TP4', 'vlans': [ ] },
      { 'name': 'TP6', 'vlans': [ ] },
      { 'name': 'TP10', 'vlans': [ 1005 ] },
      { 'name': 'TP11', 'vlans': [ 1005 ] },
      { 'name': 'TP12', 'vlans': [ 107 ] },
      { 'name': 'TP13', 'vlans': [ 1005, 107 ] },
      { 'name': 'TP16', 'vlans': [ 1005 ] }
    ]
    database.modify_switch('switch1', port_maps = ports_str)

    for sw in database.query_switches():
        pprint.PrettyPrinter(indent=4).pprint(sw.jsonify())

def main():
    #input_examples()

if __name__ == '__main__':
    main()

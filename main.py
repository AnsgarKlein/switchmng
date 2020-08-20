#!/bin/env python3

import pprint

import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from schema import Base, Switch, SwitchModel, Vlan, PortModel, PortType

def main():
    print('setting up database...')

    engine = create_engine('sqlite:///')
    Base.metadata.create_all(engine)
    Base.metadata.bin = engine

    sessionm = sessionmaker()
    sessionm.configure(bind = engine)
    session = sessionm()


    # Parse port types
    port_type_str = """
    [
      { "description": "100BASE-TX", "speed": "100"  },
      { "description": "1000BASE-T", "speed": "1000" },
      { "description": "1000BASE-X", "speed": "1000" }
    ]
    """
    for item in json.loads(port_type_str):
        port_type = PortType(description = item['description'], speed = item['speed'])
        session.add(port_type)
    session.commit()


    gigabit_tp = session.query(PortType).filter_by(speed = '1000').first()
    gigabit_fiber = session.query(PortType).filter_by(speed = '1000').first()

    # Create switch model
    ps = []
    for i in range(24):
        p = PortModel(name = 'TP{}'.format(i + 1),
                      port_type = gigabit_tp)
        ps.append(p)
    for i in range(4):
        p = PortModel(name = 'F{}'.format(i + 1),
                      port_type = gigabit_fiber)
        ps.append(p)
    model1 = SwitchModel(name = 'ZyXEL GS1910-24', ports = ps)

    switch1 = Switch(name = 'switch1', location = 5, model = model1)
    v1337 = Vlan(id = 1337, name = 'internal net')
    v1338 = Vlan(id = 1338, name = 'guest network')
    #p1 = Port(name = '1', vlans = [ v1337, v1338 ])
    #p2 = Port(name = '2', vlans = [ v1338, v1337 ])
    #p3 = Port(name = '3', vlans = [ v1338 ])
    #p4 = Port(name = '4', vlans = [ v1338 ])
    #switch1.ports = [ p1, p2, p3, p4 ]

    #session.add(p1)
    #session.add(p2)
    #session.add(p3)
    #session.add(p4)
    session.add(switch1)

    session.commit()



    #pprint.PrettyPrinter(indent=4).pprint(session.query(Switch).all())
    #pprint.PrettyPrinter(indent=4).pprint(session.query(SwitchModel).all())

    for switch in session.query(Switch).all():
        print('Switch:')
        pprint.PrettyPrinter().pprint(switch.jsonify())
        print()

if __name__ == '__main__':
    main()

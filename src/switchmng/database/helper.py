from switchmng.schema import *

from .query import *

def port_models_from_dict(session, ports):
    """
    Convert port models from list of dict of strings to list of port model objects.
    """

    # Check structure before doing anything in order to reduce
    # database queries.
    if not isinstance(ports, list):
        raise TypeError('Given list of ports is not of type list')
    for port in ports:
        if not isinstance(port, dict):
            raise TypeError('Given port is not of type dict')

    # Convert
    port_objs = []
    for port in ports:
        # Convert network protocols from list[str] to list[obj]
        if 'network_protocols' in port and port['network_protocols'] is not None:
            if not isinstance(port['network_protocols'], list):
                raise TypeError('Given list of network protocols is not of type list')
            port['network_protocols'] = [ query_network_protocol(session, p)
                                          for p in port['network_protocols'] ]
            if None in port['network_protocols']:
                raise ValueError('Given network protocol in list of network protocols does not exist')

        # Convert connector from str to obj
        if 'connector' in port and port['connector'] is not None:
            port['connector'] = query_connector(session, port['connector'])
            if port['connector'] is None:
                raise ValueError('Given connector of port model does not exist')

        # Create port object with given parameter
        port_obj = PortModel(**port)
        port_objs.append(port_obj)

    return port_objs

def ports_from_dict(session, ports):
    """
    Convert ports from list of dict of strings to list of port objects.
    """

    # Check structure before doing anything in order to reduce
    # database queries.
    if not isinstance(ports, list):
        raise TypeError('Given list of ports is not of type list')
    for port in ports:
        if not isinstance(port, dict):
            raise TypeError('Given port is not of type dict')

    # Convert
    port_objs = []
    for port in ports:
        # Convert vlans from list of str to list of obj
        if 'vlans' in port:
            if not isinstance(port['vlans'], list):
                raise TypeError('Given list of vlans of port is not of type list')
            port['vlans'] = [ query_vlan(session, v) for v in port['vlans'] ]

            if None in port['vlans']:
                raise ValueError('Given vlan in list of vlans of port does not exist')


        # Create port object with given parameter
        port_obj = Port(**port)
        port_objs.append(port_obj)

    return port_objs


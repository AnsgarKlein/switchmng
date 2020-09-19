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
        # Convert port type from str to obj
        if 'port_type' in port and port['port_type'] is not None:
            port['port_type'] = query_port_type(session, port['port_type'])

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


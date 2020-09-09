from .query import *

def port_models_from_dict(ports):
    """
    Convert port models from list of dict of strings to list of port model objects.
    """

    # Check structure before doing anything in order to reduce
    # database queries.
    if type(ports) is not list:
        raise TypeError('Given list of ports is not of type list')
    for port in ports:
        if type(port) is not dict:
            raise TypeError('Given port is not of type dict')

    # Convert
    port_objs = []
    for port in ports:
        # Convert port type from str to obj
        if 'port_type' in port and port['port_type'] is not None:
            port['port_type'] = query_port_type(port['port_type'])

        # Create port object with given parameter
        port_obj = PortModel(**port)
        port_objs.append(port_obj)

    return port_objs

def ports_from_dict(ports):
    """
    Convert ports from list of dict of strings to list of port objects.
    """

    # Check structure before doing anything in order to reduce
    # database queries.
    if type(ports) is not list:
        raise TypeError('Given list of ports is not of type list')
    for port in ports:
        if type(port) is not dict:
            raise TypeError('Given port is not of type dict')

    # Convert
    port_objs = []
    for port in ports:
        # Convert vlans from list of str to list of obj
        if 'vlans' in port:
            if type(port['vlans']) is not list:
                raise TypeError('Given list of vlans of port is not of type list')
            port['vlans'] = [ query_vlan(v) for v in port['vlans'] ]

            if None in port['vlans']:
                raise ValueError('Given vlan in list of vlans of port does not exist')


        # Create port object with given parameter
        port_obj = Port(**port)
        port_objs.append(port_obj)

    return port_objs


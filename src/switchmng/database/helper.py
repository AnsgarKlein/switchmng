from .query import *

def check_switch_model_parameters(**kwargs):
    for key, val in kwargs.items():
        if key == 'name':
            if type(val) is not str:
                raise TypeError('Given name of switch model is not of type str')
        elif key == 'ports':
            kwargs['ports'] = _port_models_to_dict(val)
        elif key == 'size':
            if type(val) is not int:
                raise TypeError('Given size of switch model is not of type int')
        else:
            raise TypeError(
                'Unexpected attribute "{}" for switch model'.format(key))

    return kwargs

def check_switch_parameters(**kwargs):
    for key, val in kwargs.items():
        if key == 'name':
            if type(val) is not str:
                raise TypeError('Given name of switch is not of type str')
        elif key == 'model':
            kwargs['model'] = query_switch_model(val)
            if kwargs['model'] is None:
                raise ValueError(
                    'Got invalid switch model "{}" - switch model does not exist'
                    .format(val))
        elif key == 'ports':
            kwargs['ports'] = _ports_to_dict(val)
        elif key == 'location':
            if type(val) is not int:
                raise TypeError('Given location of switch is not of type int')
        else:
            raise TypeError(
                'Unexpected attribute "{}" for switch'.format(key))

    return kwargs

def check_port_type_parameters(**kwargs):
    for key, val in kwargs.items():
        if key == 'description':
            if type(val) is not str:
                raise TypeError('Given description of port type is not of type str')
        elif key == 'speed':
            if type(val) is not int:
                raise TypeError('Given speed of port type is not of type int')
        else:
            raise TypeError(
                'Unexpected attribute "{}" for port type'.format(key))

    return kwargs

def check_vlan_parameters(**kwargs):
    for key, val in kwargs.items():
        if key == 'tag':
            if type(val) is not int:
                raise TypeError('Given tag of vlan is not of type int')
        elif key == 'description':
            if type(val) is not str:
                raise TypeError('Given description of vlan is not of type str')
        else:
            raise TypeError(
                'Unexpected attribute "{}" for VLAN'.format(key))

    return kwargs

def _port_models_to_dict(ports):
    if type(ports) is not list:
        raise TypeError('Given list of ports is not a list')

    # Unpack ports
    maps = []
    for port in ports:
        if type(port) is not dict:
            raise TypeError('Given port map is not a dict')

        # Check port name
        if 'name' not in port:
            raise KeyError('Given port map does not contain key "name"')
        name = port['name']
        if type(name) is not str:
            raise TypeError('Element "name" of given port map is not of type str')

        # Check port type
        if 'port_type' not in port or port['port_type'] is None:
            port_type = None
        else:
            port_type = query_port_type(port['port_type'])
            if type(port_type) is not PortType:
                raise ValueError('Element "port_type" of given port map contains invalid port type')

        maps.append({ 'name': name, 'port_type': port_type })

    return maps

def _ports_to_dict(ports):
    if type(ports) is not list:
        raise TypeError('Given list of port is not a list')

    # Unpack ports
    maps = []
    for port in ports:
        if type(port) is not dict:
            raise TypeError('Given port map is not a dict')
        if 'name' not in port:
            raise KeyError('Given port map does not contain key "name"')
        if 'vlans' not in port:
            raise KeyError('Given port map does not contain key "vlans"')

        name = port['name']
        vlans = [ query_vlan(v) for v in port['vlans'] ]

        if type(name) is not str:
            raise TypeError('Element "name" of given port map is not of type str')
        if None in vlans:
            raise ValueError('Element "vlans" of given port map contains invalid vlan')

        maps.append({ 'name': name, 'vlans': vlans })

    return maps


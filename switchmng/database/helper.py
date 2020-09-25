from typing import List

from switchmng.schema import *

from .query import *

def port_model_from_dict(session, **kwargs) -> PortModel:
    """
    Create port model.
    """

    # Convert network protocols from list[str] to list[obj]
    if 'network_protocols' in kwargs and kwargs['network_protocols'] is not None:
        if not isinstance(kwargs['network_protocols'], list):
            raise TypeError('Given list of network protocols is not of type list')
        kwargs['network_protocols'] = [ query_network_protocol(session, p)
                                      for p in kwargs['network_protocols'] ]
        if None in kwargs['network_protocols']:
            raise ValueError('Given network protocol in list of network protocols does not exist')

    # Convert connector from str to obj
    if 'connector' in kwargs and kwargs['connector'] is not None:
        kwargs['connector'] = query_connector(session, kwargs['connector'])
        if kwargs['connector'] is None:
            raise ValueError('Given connector of port model does not exist')

    return PortModel(**kwargs)

def port_models_from_dict(session, ports: List[dict]) -> List[PortModel]:
    """
    Convert port models from list of dict of strings to list of port model objects.
    """

    # Check parameter
    if not isinstance(ports, list):
        raise TypeError('Given list of ports is not of type list')
    for port in ports:
        if not isinstance(port, dict):
            raise TypeError('Given port is not of type dict')

    # Convert
    objs = []
    for port in ports:
        obj = port_model_from_dict(session, **port)
        objs.append(obj)

    return objs

def ports_from_dict(session, ports: List[dict]) -> List[Port]:
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
    objs = []
    for port in ports:
        # Convert vlans from list of str to list of obj
        if 'vlans' in port:
            if not isinstance(port['vlans'], list):
                raise TypeError('Given list of vlans of port is not of type list')
            port['vlans'] = [ query_vlan(session, v) for v in port['vlans'] ]

            if None in port['vlans']:
                raise ValueError('Given vlan in list of vlans of port does not exist')


        # Create port object with given parameter
        obj = Port(**port)
        objs.append(obj)

    return objs

import os
import json
from json import JSONDecodeError

from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type

from switchmng import config
from switchmng.schema import *
from switchmng.schema.base import Base
from switchmng.schema.base_resource import BaseResource
from switchmng import database
from switchmng.database import DatabaseConnection

IMPORT_TYPES: Dict[str, Type[BaseResource]] = {
    'switch_model': SwitchModel,
    'switch': Switch,
    'vlan': Vlan,
    'network_protocol': NetworkProtocol,
    'connector': Connector
}

IMPORT_DIR_TYPES: Dict[str, Type[BaseResource]] = {
    'switch_models': SwitchModel,
    'switches': Switch,
    'vlans': Vlan,
    'network_protocols': NetworkProtocol,
    'connectors': Connector
}

IMPORT_ORDER = {
    Connector: 0,
    NetworkProtocol: 0,
    Vlan: 0,
    SwitchModel: 1,
    Switch: 2
}

def import_from_path(
        db: DatabaseConnection,
        path: str,
        resource_type: Optional[Type[BaseResource]]) -> None:
    """
    Add resource(s) from json file(s) to database.

    Given ``path`` can be one of the following:

    1. A file.
       In this case the ``resource_type`` parameter has to be set indicating
       what type of resource this file contains.

    2. A directory named like a resource type containing multiple resources
       of that type.
       In this case no ``resource_type`` has to be given.

    3. A directory with any name containing multiple resources of the same
       type.
       In this case ``resource_type`` parameter has to be set indicating what
       type of resources files in this directory contain.

    4. A directory with any name containing multiple directories which are
       named like resource types containing only resources of those types.
       In this case ``resource_type`` must not be given.

    **Note**: If path is a directory files in this directory starting
    with ``.`` will not be imported!

    :param db: Connection to the database

    :param path: The path to the file or directory containing the
        resource(s) in json format.

    :param resource_type: The type of resource the file or directory
        contains or None for autodetection.
    """

    if path is None:
        raise ValueError('Given path does not exist')
    if not os.path.exists(path):
        raise ValueError(f"Given path '{path}' does not exist")

    # Import from file
    if os.path.isfile(path):
        if resource_type is None:
            raise ValueError(f"Cannot import unknown type from file '{path}'")

        _import_from_file(db, path, resource_type)
        return

    # Import from directory
    if os.path.isdir(path):
        # Import from directory with given resource type
        if resource_type is not None:
            _import_from_directory(db, path, resource_type)
            return

        # Import from directory named like resource type
        dir_name = os.path.basename(path)
        if dir_name in config.IMPORT_DIR_TYPES:
            _import_from_directory(db, path, config.IMPORT_DIR_TYPES[dir_name])
            return

        # Import from directory containg subdirectories named
        # like resource types
        _import_from_directories(db, path)
        return

    raise RuntimeError(f"Path '{path}' is neither file nor directory. " + \
        "Please report this as a bug") #pragma: no cover

def _import_from_file(
        db: DatabaseConnection,
        path: str,
        resource_type: Type[BaseResource]) -> None:
    """
    Add resource from json file to database.

    :param db: Connection to the database

    :param path: Path to the file to read resource from.

    :param resource_type: The type of resource the file contains
    """

    # Read content of file
    with open(path, 'r') as f:
        str_content = f.read()

    # Parse content of file
    try:
        content = json.loads(str_content)
    except JSONDecodeError as e:
        raise ValueError(f'File {path} does not contain valid json') from e

    # TODO: Implement --update command line parameter
    if resource_type is SwitchModel:
        database.add_switch_model(db.Session(), **content)
        #database.set_switch_model(db.Session(), None, **content)
    elif resource_type is Switch:
        database.add_switch(db.Session(), **content)
        #database.set_switch(db.Session(), None, **content)
    elif resource_type is Vlan:
        database.add_vlan(db.Session(), **content)
        #database.set_vlan(db.Session(), None, **content)
    elif resource_type is NetworkProtocol:
        database.add_network_protocol(db.Session(), **content)
        #database.set_network_protocol(db.Session(), None, **content)
    elif resource_type is Connector:
        database.add_connector(db.Session(), **content)
        #database.set_connector(db.Session(), None, **content)
    else:
        raise ValueError(f"Cannot import resource of unknown type '{resource_type}'")

    print(f'Imported {path}')

def _import_from_directory(
        db: DatabaseConnection,
        path: str,
        resource_type: Type[BaseResource]) -> None:
    """
    Add resources from multiple files inside a directory to database.

    :param db: Connection to the database

    :param path: Path to the directory containg the files to read.

    :param resource_type: The type of resources the files in this
        directory contain.
    """

    # Import all files in this directory
    files = ( os.path.abspath(os.path.join(path, f)) for f in os.listdir(path) )
    for f in files:
        if not os.path.isfile(f):
            continue
        if f.startswith('.'):
            continue
        _import_from_file(db, f, resource_type)

def _import_from_directories(db: DatabaseConnection, path: str) -> None:
    """
    Add resources from multiple files inside multiple directories.

    :param db: Connection to database

    :param path: Path to the directory containing subdirectories named
        like resources containing the resource files.
    """

    # Check all subdirectories
    children = ( os.path.abspath(os.path.join(path, d)) for d in os.listdir(path) )
    subdirs = [ child for child in children if os.path.isdir(child) ]

    for subdir in subdirs:
        # Check if all child directories are named like resource types
        dir_name = os.path.basename(subdir)
        if dir_name not in config.IMPORT_DIR_TYPES:
            raise ValueError(
                "Cannot import unknown type of resource from directory '{}'".format(
                    subdir))

    # Make sure directories are imported in the correct order
    subdirs = sort_import_dirs(subdirs)

    # Add resources from all subdirectories
    for subdir in subdirs:
        _import_from_directory(
            db,
            subdir,
            config.IMPORT_DIR_TYPES[os.path.basename(subdir)])

def sort_import_dirs(paths: List[str]) -> List[str]:
    """
    Sort list of directories named like resource identifiers.

    Sort list of directories in order to make sure they can be imported
    correctly so that every resource type gets imported after resource
    types it relies on have been imported.
    """

    sorted_lst: List[Tuple[str, int]] = []

    # Assign order integer to every path
    for path in paths:
        dir_name = os.path.basename(path)
        import_type = IMPORT_DIR_TYPES[dir_name]
        import_order = IMPORT_ORDER[import_type]
        sorted_lst.append((path, import_order))

    # Sort list
    sorted_lst.sort(key = lambda x: x[1])

    # Extract paths
    return [ item[0] for item in sorted_lst ]

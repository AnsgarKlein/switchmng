import argparse

from typing import List

# Default configuration values
# Configuration values can be overridden by command line options
# or via options in configuration file.
_DEFAULT_MODE        = 'webserver'

_DEFAULT_CONFIG_FILE = None

_DEFAULT_DB_TYPE     = 'sqlite'
_DEFAULT_DB_PATH     = 'example.db'
_DEFAULT_DB_VERBOSE  = False

_DEFAULT_DEBUG       = False
_DEFAULT_IP          = '127.0.0.1'
_DEFAULT_PORT        = 8000


MODE        = _DEFAULT_MODE

CONFIG_FILE = _DEFAULT_CONFIG_FILE

DB_TYPE     = _DEFAULT_DB_TYPE
DB_PATH     = _DEFAULT_DB_PATH
DB_VERBOSE  = _DEFAULT_DB_VERBOSE

DEBUG       = _DEFAULT_DEBUG
IP          = _DEFAULT_IP
PORT        = _DEFAULT_PORT

def _default_config():
    """Reset global configuration values to default"""

    global MODE

    global CONFIG_FILE

    global DB_TYPE
    global DB_PATH
    global DB_VERBOSE

    global DEBUG
    global IP
    global PORT

    MODE        = _DEFAULT_MODE

    CONFIG_FILE = _DEFAULT_CONFIG_FILE

    DB_TYPE     = _DEFAULT_DB_TYPE
    DB_PATH     = _DEFAULT_DB_PATH
    DB_VERBOSE  = _DEFAULT_DB_VERBOSE

    DEBUG       = _DEFAULT_DEBUG
    IP          = _DEFAULT_IP
    PORT        = _DEFAULT_PORT

def parse_config(content: str) -> None:
    """Apply configuration from configuration file content.

    :param content: Content of the configuration file.
    """

    # TODO: Implement parsing of configuration file
    raise NotImplementedError('Parsing config file is not yet implemented')

def parse_config_file(path: str) -> None:
    """Apply configuration from configuration file.

    :param path: Path to configuration file.
    """

    with open(path, 'r') as f:
        content = f.read()
        parse_config(content)

def _add_subparser_webserver(subparsers) -> None:
    """Add subparser for webserver mode to given subparsers."""

    parser = subparsers.add_parser(
        'webserver',
        add_help = False,
        allow_abbrev = False)

    parser.usage = 'switchmng [ GENERAL OPTIONS ] webserver [ MODE-SPECIFIC OPTIONS ]'

    parser.description = '''
        Run switchmng with the builtin webserver.

        WARNING: *DO NOT* use this for production
                 environments! It will allow remote
                 users to execute code on your system!

        Start with -h option without specifying MODE to see general options.'''

    options = parser.add_argument_group('OPTIONS')

    options.add_argument(
        '-d', '--debug',
        help = '''
               Activate debug mode (default: {})
               WARNING: This will allow code to be excuted on your system from
               everyone who can access the website! Only use for development!'''
           .format(_DEFAULT_DEBUG),
        action = 'store_true',
        default = argparse.SUPPRESS)

    options.add_argument(
        '-h', '--help',
        help = 'Show help for selected mode and exit',
        action = 'help')

    options.add_argument(
        '-i', '--ip',
        help = 'IP to listen on (default: {})'
            .format(_DEFAULT_IP),
        default = argparse.SUPPRESS)

    options.add_argument(
        '-p', '--port',
        help = 'Port to listen on (default: {})'
           .format(_DEFAULT_PORT),
        default = argparse.SUPPRESS,
        type = int)

def _add_subparsers_dump(subparsers) -> None:
    """Add subparser for dump mode to given subparsers."""

    parser = subparsers.add_parser(
        'dump',
        add_help = False,
        allow_abbrev = False)

    parser.usage = 'switchmng [ GENERAL OPTIONS ] dump [ MODE-SPECIFIC OPTIONS ]'

    parser.description = 'NOT YET IMPLEMENTED'

    options = parser.add_argument_group('OPTIONS')

    options.add_argument(
        '-h', '--help',
        help = 'Show help for selected mode and exit',
        action = 'help')

def _create_argument_parser() -> argparse.ArgumentParser:
    """Create argparse argument parser"""

    parser = argparse.ArgumentParser(add_help = False, allow_abbrev = False)
    parser.prog = 'switchmng'
    parser.usage = 'switchmng [ GENERAL OPTIONS ] MODE [ MODE-SPECIFIC OPTIONS ]'

    description='''
                Specify which mode of operation to start in. Start mode
                with -h option for more info about what each mode does,
                what options are available and what they do.'''
    subparsers = parser.add_subparsers(
        title = 'MODE',
        description = description,
        help = 'default = {}'.format(_DEFAULT_MODE),
        prog = parser.prog,
        dest = 'mode')
    parser.set_defaults(mode = _DEFAULT_MODE)

    # Parser for webserver mode
    _add_subparser_webserver(subparsers)

    # Parser for dump mode
    _add_subparsers_dump(subparsers)

    # Parser for options that apply to all modes of operation
    options = parser.add_argument_group('GENERAL OPTIONS')

    options.description = '''
        The following options apply to all modes of operations
        independent of what MODE is selected.'''

    options.add_argument(
        '-c', '--config',
        help = 'Configuration file to read configuration from\
               All options set in configuration file will be\
               overwritten with options set on command line.\
               (default: {})'.format(_DEFAULT_CONFIG_FILE),
        metavar = 'FILE',
        default = argparse.SUPPRESS)

    options.add_argument(
        '--dbtype',
        help = 'Set type of database to use\
               (default: {})'.format(_DEFAULT_DB_TYPE),
        metavar = 'TYPE',
        choices = ('sqlite', None),
        default = argparse.SUPPRESS)

    options.add_argument(
        '--dbpath',
        help = 'Set path to sqlite database. Empty path "" means\
               an in memory sqlite database will be used. This\
               database will loose all content after application\
               exit! (default: "{}")'.format(_DEFAULT_DB_PATH),
        metavar = 'PATH',
        default = argparse.SUPPRESS)

    options.add_argument(
        '-h', '--help',
        help = 'Show help for selected mode and exit',
        action = 'help')

    options.add_argument(
        '-v', '--verbose',
        help = 'Make given subsystem verbose and print more\
               information to stdout. Can be supplied multiple\
               times. Possible values: sql',
        metavar = 'SUBSYSTEM',
        choices = ('sql', None),
        action = 'append',
        default = argparse.SUPPRESS)

    return parser

def parse_arguments(arguments: List[str]) -> None:
    """Apply configuration from command line arguments.

    :param arguments: List of command line arguments.
    """

    # Apply default config
    _default_config()

    # Create argument parser
    parser = _create_argument_parser()

    # Parse arguments
    args = parser.parse_args(arguments)

    # Check if config file was given on command line
    global CONFIG_FILE
    if 'config' in args:
        CONFIG_FILE = args.config

    # Apply all configuration settings from command line
    if CONFIG_FILE is not None:
        parse_config_file(CONFIG_FILE)

    # After applying config file apply the rest of command line parameters
    global MODE
    MODE = args.mode

    # Apply arguments from GENERAL group
    if 'dbtype' in args:
        global DB_TYPE
        DB_TYPE = args.dbtype

    if 'dbpath' in args:
        global DB_PATH
        DB_PATH = args.dbpath

    if 'verbose' in args:
        if 'sql' in args.verbose:
            global DB_VERBOSE
            DB_VERBOSE = True

    # Apply arguments from WEBSERVER group
    if 'debug' in args:
        global DEBUG
        DEBUG = args.debug

    if 'ip' in args:
        global IP
        IP = args.ip

    if 'port' in args:
        global PORT
        PORT = args.port

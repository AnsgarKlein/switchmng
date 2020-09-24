import sys
import argparse

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
_DEFAULT_PORT        = '8000'


MODE        = _DEFAULT_MODE

CONFIG_FILE = _DEFAULT_CONFIG_FILE

DB_TYPE     = _DEFAULT_DB_TYPE
DB_PATH     = _DEFAULT_DB_PATH
DB_VERBOSE  = _DEFAULT_DB_VERBOSE

DEBUG       = _DEFAULT_DEBUG
IP          = _DEFAULT_IP
PORT        = _DEFAULT_PORT

def _default_config():
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

def parse_config(content):
    raise NotImplementedError('Parsing config file is not yet implemented')

def parse_config_file(path):
    with open(path, 'r') as f:
        content = f.read()
        parse_config(content)

def parse_arguments(arguments):
    # Apply default config
    _default_config()

    # Setup argument parser
    parser = argparse.ArgumentParser(add_help = False, allow_abbrev = False)
    parser.prog = 'switchmng'
    parser.usage = '{} MODE [ GENERAL OPTIONS ] [ MODE-SPECIFIC OPTIONS ]'\
                   .format(parser.prog)

    # Parser for mode parameter
    pg1 = parser.add_argument_group('MODE')
    pg1.description = """
                      Specify which mode of operation to start in. See sections
                      below for more  info about what they do and what options
                      can be applied."""
    pg1.add_argument('MODE',
                     help = 'default = {}'.format(_DEFAULT_MODE),
                     nargs = '?',
                     choices = ('webserver', 'dump'),
                     default = 'webserver')

    # Parser for options that apply to all modes of operation
    pg3 = parser.add_argument_group('GENERAL OPTIONS')
    pg3.description = """
                      The following options apply to all modes of operations
                      independent of what MODE is selected."""
    pg3.add_argument('-c', '--config',
                     help = 'Configuration file to read configuration from\
                            All options set in configuration file will be\
                            overwritten with options set on command line.\
                            (default: {})'.format(_DEFAULT_CONFIG_FILE),
                     metavar = 'FILE',
                     default = argparse.SUPPRESS)
    pg3.add_argument('--dbtype',
                     help = 'Set type of database to use\
                            (default: {})'.format(_DEFAULT_DB_TYPE),
                     metavar = 'TYPE',
                     choices = ('sqlite', None),
                     default = argparse.SUPPRESS)
    pg3.add_argument('--dbpath',
                     help = 'Set path to sqlite database. Empty path "" means\
                            an in memory sqlite database will be used. This\
                            database will loose all content after application\
                            exit! (default: "{}")'.format(_DEFAULT_DB_PATH),
                     metavar = 'PATH',
                     default = argparse.SUPPRESS)
    pg3.add_argument('-h', '--help',
                     help = 'Show this help message and exit',
                     action = 'help')
    pg3.add_argument('-v', '--verbose',
                     help = 'Make given subsystem verbose and print more\
                            information to stdout. Can be supplied multiple\
                            times. Possible values: sql',
                     metavar = 'SUBSYSTEM',
                     choices = ('sql', None),
                     action = 'append',
                     default = argparse.SUPPRESS)


    # Parser for options for internal webserver
    pg4 = parser.add_argument_group('WEBSERVER')
    pg4.description = """
        Run switchmng with the builtin webserver.

        WARNING: *DO NOT* use this for production
                 environments! It will allow remote
                 users to execute code on your system!

        The following arguments only take effect when in webserver mode:"""
    pg4.add_argument('-d', '--debug',
                     help = """
                            Activate debug mode (default: {})
                            WARNING: This will allow code to be excuted on
                            your system from everyone who can access the
                            website!
                            Only use for development!"""
                        .format(_DEFAULT_DEBUG),
                     action = 'store_true',
                     default = argparse.SUPPRESS)
    pg4.add_argument('-i', '--ip',
                     help = 'IP to listen on (default: {})'
                        .format(_DEFAULT_IP),
                     default = argparse.SUPPRESS)
    pg4.add_argument('-p', '--port',
                     help = 'Port to listen on (default: {})'
                        .format(_DEFAULT_PORT),
                     default = argparse.SUPPRESS,
                     type = int)

    pg5 = parser.add_argument_group('DUMP')
    pg5.description = 'NOT YET IMPLEMENTED'

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
    MODE = args.MODE
    if MODE == 'dump':
        raise NotImplementedError('dump ist not yet implemented!')

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

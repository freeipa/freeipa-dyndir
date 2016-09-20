# coding: utf-8
# Author: Milan Kubik


import json
import logging
import sys

import argparse

from ipaqe_dyndir import inventory
from ipaqe_dyndir.utils import load_config, ConfigLoaderError


def main():
    parser = argparse.ArgumentParser(description='Convert ipa test config to '
                                     'ansible dynamic directory')
    parser.add_argument('-f', '--file', metavar="FILE",
                        dest='filename', default=None,
                        help='File containing the configuration. '
                             'By default reads from IPATEST_YAML_CONFIG '
                             'environment variable')
    parser.add_argument('--list', help='Print the inventory as json.',
                        dest='list_resources', action='store_true')
    parser.add_argument('--pretty', dest='pretty', action='store_true',
                        help='Pretty print the result.')
    parser.add_argument('-d', '--debug', metavar='LEVEL',
                        dest='loglevel', default=None,
                        help='Python logging level.')
    parser.add_argument('-c', '--config', metavar="CONFIG",
                        dest='configfile', default=None,
                        help='Configuration file for the dynamic directory. '
                             'If ommited, IPAQE_DYNDIR_CONFIG environment '
                             'variable or /etc/ipaqe-dyndir.conf is used.')

    args = parser.parse_args()

    loglevel = None
    if args.loglevel:
        try:
            loglevel = getattr(logging, args.loglevel)
        except AttributeError:
            loglevel = logging.ERROR
        finally:
            logging.basicConfig(level=loglevel)

    log = logging.getLogger(__name__)
    log.info('Setting log level to {}'.format(logging.getLevelName(loglevel)))

    if args.list_resources:
        try:
            indentation = 4 if args.pretty else None
            log.debug('Setting indentation to {}'.format(indentation))

            inventory_config = load_config(path=args.configfile)
            print(json.dumps(
                inventory.list_hosts(args.filename, inventory_config),
                indent=indentation, sort_keys=True))
        except inventory.InventoryError:
            # Catching the base exception means, that any expected
            # errors in the inventory module were handled and
            # the module cannot recover.
            sys.exit(1)
        except ConfigLoaderError:
            # Similar to the previous block
            sys.exit(1)
        except Exception as e:  # pylint: disable=W0703
            log.error('An unexpected exception occured.\n%s', e)
            sys.exit(1)
    else:
        log.debug('No operation specified.')
        parser.print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()

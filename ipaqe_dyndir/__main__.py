# coding: utf-8

import argparse
import json
import logging
import sys

from ipaqe_dyndir import inventory


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
    parser.add_argument('-d', '--debug', action='store_true',
                        dest='debug')

    args = parser.parse_args()

    # TODO: here load config from etc

    if args.debug:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    logging.basicConfig(level=loglevel)
    log = logging.getLogger(__name__)
    log.debug('Setting log level to %s' % logging.getLevelName(loglevel))

    if args.list_resources:
        try:
            indentation = 4 if args.pretty else None
            log.debug('Setting indentation to %s' % indentation)

            print(json.dumps(inventory.list_hosts(args.filename),
                             indent=indentation, sort_keys=True))
        except:
            log.debug('An exception occured. Terminating.')
            sys.exit(1)
    else:
        log.debug('No operation specified.')
        parser.print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()

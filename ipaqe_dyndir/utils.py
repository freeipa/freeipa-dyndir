# coding: utf-8
# Author: Milan Kubik
from __future__ import absolute_import

import os
import logging
import yaml

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError  # pylint: disable=redefined-builtin

log = logging.getLogger(__name__)


class ConfigLoaderError(Exception):
    """Config Loader Exception

    The exception is used to indicate that an error
    occured in the module and it has been handled
    somehow. The failure is not recoverable.
    """
    pass


def load_config(path=None):
    """configuration loader

    The function takes path to the configuration.
    If no path is specified, the configuration is
    looked up in the following places:

    * environment variable IPAQE_DYNDIR_CONF
    * global configuration in /etc/ipaqe-dyndir.conf

    If none of these paths exists, the function will
    fail.

    If the configuration content is not valid YAML
    document, the function will fail.
    """
    filename_etc = '/etc/ipaqe-dyndir.conf'
    filename_env = os.environ.get('IPAQE_DYNDIR_CONFIG')

    if path:
        filename = path
    elif filename_env:
        filename = filename_env
    else:
        filename = filename_etc

    log.info('Loading config from file {}'.format(filename))

    try:
        with open(filename) as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        log.error('Configuration file {} not found.'.format(filename))
        raise ConfigLoaderError
    except yaml.scanner.ScannerError as e:
        log.error('Error parsing the configuration file {name}.'
                  '\n{msg}'.format(name=filename, msg=e))
        raise ConfigLoaderError

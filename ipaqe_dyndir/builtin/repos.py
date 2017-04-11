# coding: utf-8
# Author: Milan Kubik
from __future__ import absolute_import

import logging

from ipaqe_dyndir.plugin.base import (
    PluginBase, PluginConfigError
)

log = logging.getLogger(__name__)


class UpdatesTestingRepositoryPlugin(PluginBase):  # pylint: disable=R0903
    """Enables or disables updates-testing repository

    The plugin takes single boolean.

    The output is put to `enable_updates_testing` host variable.
    """

    name = 'updates-testing'

    def __init__(self, config):
        log.debug('Initializing updates-testing plugin.')
        if isinstance(config, bool):
            self._config = config
        else:
            raise PluginConfigError(
                'Invalid attribute type {} in the updates-testing '
                'plugin configuration'.format(type(config))
            )

    def __call__(self, host):
        log.debug('Running updates-testing plugin for host {}'
                  .format(host['name']))
        return {
            'enable_updates_testing': self._config
        }


class COPRPlugin(PluginBase):  # pylint: disable=R0903
    """Creates a list of COPR repositories for a host.

    Takes a list of COPR repository names. E.g.:

    [
        '@freeipa/freeipa-master',
        'pspacek/bind-dyndb-ldap'
    ]

    The output is put into `copr_repositories` host variable.
    """

    name = 'copr'

    def __init__(self, config):
        log.debug('Initializing copr plugin.')
        if isinstance(config, (list, tuple)):
            self._config = config
        else:
            raise PluginConfigError(
                "Invalid attribute type {} in the copr plugin configuration."
                .format(type(config)))

    def __call__(self, host):
        log.debug('Running copr plugin for host {}'
                  .format(host['name']))
        if self._config:
            res = {
                'copr_repositories': list(self._config)
            }
        else:
            res = {}

        return res

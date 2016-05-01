# coding: utf-8

import logging
import os
import yaml

log = logging.getLogger(__name__)


# python2...
try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


SERVER_ROLES = ('master', 'replica')
CLIENT_ROLES = ('client',)
TRUST_ROLES = ('trust_master',)

SERVER_PACKAGES = ('freeipa-server-dns',)
TRUST_PACKAGES = ('freeipa-server-dns', 'freeipa-server-trust')
CLIENT_PACKAGES = ('freeipa-client',)


def list_hosts(filename=None):

    domain_filename = filename or os.environ.get('IPATEST_YAML_CONFIG')

    try:
        log.debug('Reading YAML file %s' % domain_filename)
        with open(domain_filename) as f:
            data = yaml.safe_load(f)
    except (TypeError, FileNotFoundError):
        log.error('Could not open file %s' % domain_filename)
        raise

    inventory = dict(
        servers=list(),
        clients=list(),
        _meta=dict(hostvars=dict())
    )

    hostvars = inventory['_meta']['hostvars']

    for domain in data['domains']:
        for host in domain['hosts']:
            hostname = host['name']
            host_role = host['role']

            log.debug('Processing host %s' % hostname)
            if host_role in SERVER_ROLES:
                inventory['servers'].append(hostname)
                hostvars[hostname] = dict(packages=SERVER_PACKAGES)
                log.debug('Created server entry %s' % hostname)
            elif host_role in TRUST_ROLES:
                inventory['servers'].append(hostname)
                hostvars[hostname] = dict(packages=TRUST_PACKAGES)
                log.debug('Created server entry %s' % hostname)
            elif host_role in CLIENT_ROLES:
                inventory['clients'].append(hostname)
                hostvars[hostname] = dict(packages=CLIENT_PACKAGES)
                log.debug('Created client entry %s' % hostname)
            else:
                log.debug("Couldn't recognize type of host %s" % hostname)

    return inventory

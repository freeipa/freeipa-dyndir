# coding: utf-8
# Author: Milan Kubik

import logging
import os
from pprint import pformat

import yaml

from ipaqe_dyndir.plugin.manager import PluginManager

log = logging.getLogger(__name__)


class InventoryError(Exception):
    pass


class InventoryHostAlreadyExistsError(InventoryError):
    pass


class InventoryUnknownHostRoleError(InventoryError):
    pass


class Inventory:
    """Class representing the ansible inventory.

    The class builds an ansible inventory from hosts
    fed into it. The host is represented as a dictionary with
    several required keys: `name` and `role`.

    The `name` key soecifies a FQDN of the host.
    The `role` specifies a role in multihost test as specified
    in freeipa testing fremework, based on pytests multihost plugin.
    """

    role_to_group_map = {
        'master': 'servers',
        'replica': 'servers',
        'trust_master': 'trust-servers',
        'client': 'clients',
    }

    group_to_packages_map = {
        'servers': ('freeipa-server-dns',),
        'trust-servers': ('freeipa-server-trust-ad', 'freeipa-server-dns'),
        'clients': ('freeipa-client',)
    }

    def __init__(self, config, *, quiet=False):
        self._data = {}
        self._metadata = {}
        self._config = config
        self._quiet = quiet
        self._pm = PluginManager(config)

    @property
    def data(self):
        """The inventory dictionary"""
        return self._data

    @property
    def metadata(self):
        """The metadata dictionary with hostvars"""
        return self._metadata

    def add_host(self, host):
        """Add a host to the inventory

        Adds a host to the inventory.
        The host is put to one of the four host groups based on its
        role. The role determines what packages are installed
        on the host. The list of packages (without dependencies)
        is then stored in the `packages` key in the host metadata.

        The function also uses the plugin manager instance to
        get any metadata provided by the registered plugins.
        """
        try:
            log.debug('Processing host {host} with type {htype}'
                      .format(host=host['name'], htype=host['role']))

            group = self._get_host_group(host['role'])
            packages = self._get_host_packages(group)

            self._add_host_to_group(host, group)
            self._generate_host_packages_metadata(host, packages)

            log.info('Running metadata plugins for host {}'
                     .format(host['name']))
            plugin_metadata = self._pm.run(host)
            self._update_metadata_for_host(host, plugin_metadata)
        except KeyError as e:
            log.error(e)
            raise

    def _add_host_to_group(self, host, group):
        try:
            self.data[group].append(host['name'])
        except KeyError:
            self.data[group] = [host['name']]

    def _bootstrap_metadata_dict(self):
        if 'hostvars' not in self.metadata:
            log.debug('Bootstraping hostvars in metadata')
            self._metadata['hostvars'] = {}

    def _generate_host_packages_metadata(self, host, packages):
        """Add the host package list to metadata


        If the metadata dictionary is empty, bootstrap the
        hostvars key.
        """
        log.info('Generating package metadata for host {name}'
                 .format(name=host['name']))

        self._bootstrap_metadata_dict()

        hostvars = self._metadata['hostvars']
        host_name = host['name']

        if host_name in hostvars:
            raise InventoryHostAlreadyExistsError(
                'The host {name} already exists and has metadata.'
                .format(name=host['name']))

        log.info('Adding packages {packages} for host {name}'
                 .format(packages=packages, name=host_name))
        hostvars[host_name] = dict(packages=packages)

    def _update_metadata_for_host(self, host, metadata):
        """In place update of host metadata

        If the dictionary for a host doesn't exist, the function
        will create it.
        """
        hostname = host['name']
        log.debug('Updating metadata for host {}'
                  .format(hostname))
        self._bootstrap_metadata_dict()

        try:
            host_vars = self.metadata['hostvars'][hostname]
        except KeyError:
            self._metadata['hostvars'][hostname] = {}
            host_vars = self.metadata['hostvars'][hostname]

        host_vars.update(metadata)

    def _get_host_group(self, role):
        """Map host role to inventory group

        Internal mapping from IPA defined host role to ansible
        inventory group.
        """
        try:
            return self.role_to_group_map[role]
        except KeyError:
            log.debug("Unknown role '{}'".format(role))
            raise InventoryUnknownHostRoleError(
                'Unknown role {}'.format(role))

    def _get_host_packages(self, group):
        return self.group_to_packages_map[group]

    def to_dict(self):
        """Exports the inventory data to a single dictionary"""
        retval = {}
        retval.update(self.data)
        if self.metadata:
            retval['_meta'] = self.metadata

        return retval


def list_hosts(filename=None, inventory_config=None):
    """List the inventory with metadata

    The function implements the ansible dynamic inventory
    providing host groups and additional metadata about
    hosts read from a yaml file that uses FreeIPA integration
    test configuration file format.

    It reads the domains section of the file and constructs
    the inventory with metadata about required packages.
    """

    domain_filename = filename or os.environ.get('IPATEST_YAML_CONFIG')
    if not domain_filename:
        log.error('IPA test config not provided')
        raise InventoryError

    try:
        log.debug('Reading YAML file {}'.format(domain_filename))
        with open(domain_filename) as f:
            data = yaml.safe_load(f)
    except yaml.scanner.ScannerError as e:
        log.error('The configuration file {name} is not valid YAML document.'
                  '\n{msg}'.format(name=domain_filename, msg=e))
        raise InventoryError
    except FileNotFoundError:
        log.error('Test configuration file {} does not exist'
                  .format(domain_filename))
        raise InventoryError

    inventory = Inventory(inventory_config)

    try:
        for domain in data['domains']:
            try:
                for host in domain['hosts']:
                    inventory.add_host(host)
            except InventoryHostAlreadyExistsError:
                log.error('Host {} already exists in the inventory.'
                          .format(host['name']))
                raise InventoryError
            except InventoryUnknownHostRoleError:
                log.error('Unrecognized host role {role} for host {name}'
                          .format(role=host['role'], name=host['name']))
                raise InventoryError
            except (KeyError, TypeError):
                log.error('The domain {dom} does not contain any hosts.'
                          .format(dom=domain['name']))
                log.debug('The domain element:\n{}'
                          .format(pformat(domain)))
                raise InventoryError
        log.debug('Finished the inventory.')
    except (KeyError, TypeError):
        log.error('The configuration file does not contain any valid domains.'
                  ' A domain must contain a list of host dictionaries.')
        log.debug('The configuration file:\n{}'.format(pformat(data)))
        raise InventoryError

    return inventory.to_dict()

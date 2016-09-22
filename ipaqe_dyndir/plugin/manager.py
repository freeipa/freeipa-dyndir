# coding: utf-8
# Author: Milan Kubik

import logging

from pkg_resources import iter_entry_points

from ipaqe_dyndir.plugin.base import PluginBase

DEFAULT_RESOURCE_GROUP = 'org.freeipa.dyndir.plugins'

log = logging.getLogger(__name__)


class PluginManager:
    """Dynamic Directory Plugin Manager

    The class acts as a loader of the plugins registered
    on the `org.freeipa.dyndir.plugins` endpoint.

    It is possible to specify custom endpoint.
    """
    def __init__(self, config, resource_group=None):
        self._config = config if config else {}
        self._active_plugins = []
        self._inactive_plugins = []
        self.load_plugins(resource_group or DEFAULT_RESOURCE_GROUP)

    @property
    def active_plugins(self):
        """List if active plugin instances"""
        return self._active_plugins

    @property
    def inactive_plugins(self):
        """List if inactive plugins"""
        return self._inactive_plugins

    @property
    def active_plugin_names(self):
        """List of active plugin names"""
        return [p.name for p in self.active_plugins]

    @property
    def inactive_plugin_names(self):
        """List of inactive plugin names"""
        return [p.name for p in self.inactive_plugins]

    def load_plugins(self, resource_group=DEFAULT_RESOURCE_GROUP):
        """Load the registered plugins

        The plugins that are registered on the expected entry point
        are loaded and then compared against the configuration.

        If there is a configuration entry (a dict key)
        matching the plugins name, then the plugin is instantiated
        and put to the list of active plugins.

        If the configuration is missing, the plugin is put to the
        list of inactive plugins.
        """
        for entry_point in iter_entry_points(resource_group):
            plugin = entry_point.load()

            if not issubclass(plugin, PluginBase):
                log.debug("Entry point {name} is not a subclass of {base}."
                          " Skipping.".format(name=plugin, base=PluginBase))

            log.debug("Found plugin {}.".format(plugin.name))
            try:
                self._active_plugins.append(plugin(self._config[plugin.name]))
                log.debug("Config exists. Adding {} to active plugins."
                          .format(plugin.name))
            except KeyError:
                log.debug("Plugin {} not enabled in config."
                          .format(plugin.name))
                self._inactive_plugins.append(plugin)

    def run(self, host):
        """Run all enabled plugins on given inventory.

        By default checks for conflicts in plugin output
        for given input inventory.
        """
        result = {}

        for plugin in self.active_plugins:
            result.update(plugin(host))

        return result

# coding: utf-8
# Author: Milan Kubik

from ipaqe_dyndir.plugin.manager import PluginManager


default_plugin_set = set([
    'updates-testing',
    'copr'
])


def test_manager_with_empty_config():
    m = PluginManager({})

    assert not m.active_plugins
    assert set(m.inactive_plugin_names) == default_plugin_set


def test_manager_with_unknown_config_keys():
    m = PluginManager({'_totaly_not_a_plugin': False})

    assert not m.active_plugins
    assert set(m.inactive_plugin_names) == default_plugin_set


def test_manager_with_config():
    m = PluginManager(
        {'updates-testing': True, 'copr': ['@freeipa/freeipa-master']}
    )

    assert not m.inactive_plugins
    assert set(m.active_plugin_names) == default_plugin_set


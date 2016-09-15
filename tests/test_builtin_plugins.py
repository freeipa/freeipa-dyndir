# coding: utf-8
# Author: Milan Kubik

import pytest

from ipaqe_dyndir.builtin.repos import (
    UpdatesTestingRepositoryPlugin,
    COPRPlugin
)
from ipaqe_dyndir.plugin.base import PluginConfigError

test_host = dict(name='test.example.com', role='master')

host_updates_enabled = {'enable_updates_testing': True}

host_updates_disabled = {'enable_updates_testing': False}

test_data_updates_testing = [
    (True, test_host, host_updates_enabled),
    (False, test_host, host_updates_disabled)
]

test_copr_freeipa = {'copr_repositories': ['@freeipa/freeipa-master']}

test_data_copr = [
    ([], test_host, {}),  # if empty list, do not generate the variable
    (tuple(), test_host, {}),  # take also immutables
    (['@freeipa/freeipa-master'], test_host, test_copr_freeipa),
    (('@freeipa/freeipa-master',), test_host, test_copr_freeipa)
]


def test_updates_testing_invalid_config():
    with pytest.raises(PluginConfigError):
        UpdatesTestingRepositoryPlugin({})


@pytest.mark.parametrize(
    'conf,host,exp_res', test_data_updates_testing)
def test_updates_config_configured(conf, host, exp_res):
    pl = UpdatesTestingRepositoryPlugin(conf)
    res = pl(host)
    assert (
        res['enable_updates_testing'] == exp_res['enable_updates_testing'])


def test_copr_plugin_invalid_config():
    with pytest.raises(PluginConfigError):
        COPRPlugin({})


@pytest.mark.parametrize(
    'conf,host,exp_res', test_data_copr)
def test_copr_repo_configs(conf, host, exp_res):
    pl = COPRPlugin(conf)
    res = pl(host)

    if not exp_res:
        assert not res
    else:
        assert (
            res['copr_repositories'] == exp_res['copr_repositories'])

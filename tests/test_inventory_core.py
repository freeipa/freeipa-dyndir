# coding: utf-8
# Author: Milan Kubik

import pytest

from ipaqe_dyndir.inventory import Inventory
from .util import get_test_data


@pytest.fixture(scope='class')
def empty_inventory():
    return Inventory({})


class TestEmptyInventory:
    def test_inventory_data(self, empty_inventory):
        assert empty_inventory.data == {}

    def test_inventory_metadata(self, empty_inventory):
        assert empty_inventory.metadata == {}

    def test_full_representation(self, empty_inventory):
        assert empty_inventory.to_dict() == {}


inventory_no_plugins = dict(
    inventory=dict(
        master=['freeipa-server-dns'],
        client=['freeipa-client'],
        replica=['freeipa-server-dns'],
        trust_master=['freeipa-server-trust-ad']
    )
)

simple_client_host = dict(get_test_data('simple_client_host.yml'))
simple_client_host_res = {
    'clients': [simple_client_host['name']],
    '_meta': {
        'hostvars': {
            simple_client_host['name']: {
                'packages': ('freeipa-client',)
            }
        }
    }
}


# TODO: Parametrize this
class TestPopulatedInventory:

    def test_no_plugins(self):
        inv = Inventory({})
        inv.add_host(simple_client_host)

        inventory = inv.to_dict()
        assert inventory == simple_client_host_res

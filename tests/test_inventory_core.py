# coding: utf-8
# Author: Milan Kubik

from ipaqe_dyndir.inventory import Inventory
from .util import get_test_data


def test_empty_inventory_data():
    inventory = Inventory({})
    assert inventory.data == {}


def test_empty_inventory_metadata():
    inventory = Inventory({})
    assert inventory.metadata == {}


def test_full_representation():
    inventory = Inventory({})
    assert inventory.to_dict() == {}


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


def test_populated_inventory_no_plugins():
    inv = Inventory({})
    inv.add_host(simple_client_host)

    inventory = inv.to_dict()
    assert inventory == simple_client_host_res

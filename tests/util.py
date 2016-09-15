# coding: utf-8
# Author: Milan Kubik

import os
import yaml
from functools import partial

here = os.path.abspath(os.path.dirname(__file__))
test_data_dir = os.path.join(here, 'test_data')

test_data_path = partial(os.path.join, test_data_dir)


def get_test_data(filename, import_yaml=True):
    with open(test_data_path(filename)) as f:
        data = f.read()

    if import_yaml:
        return yaml.load(data)
    else:
        return data

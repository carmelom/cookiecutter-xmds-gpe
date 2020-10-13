#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Created: 07-2020 - Carmelo Mordini <carmelo> <carmelo.mordini@unitn.it>

"""Module docstring

"""
from pathlib import Path
import itertools
from copy import deepcopy
from src.tasks import autosequence

from ruamel import yaml

DOIT_CONFIG = {
    'verbosity': 2,
    'backend': 'json',
    'dep_file': '.doit_scan.db',
}


with open('configure.yaml', 'r') as f:
    conf = yaml.safe_load(f)

run_dir = Path(conf['run_dir'])
run_dir.mkdir(parents=True, exist_ok=True)
sequence_index = autosequence(run_dir)

scan = {
    'imprint_x0': list(range(1, 5, 1)),
}

keys, values = list(zip(*scan.items()))

shots = []
for item in itertools.product(*values):
    conf['globals'].update(dict(zip(keys, item)))
    shots.append(deepcopy(conf))


def task_run_sequence():
    def _write_conf(_conf, filename):
        with open(filename, 'w') as f:
            f.write(yaml.safe_dump(_conf))

    for j, conf in enumerate(shots):
        conf_name = '_config.yaml'
        yield {
            'name': j,
            'actions': [
                (_write_conf, [conf, conf_name]),
                f"doit config_file={conf_name} sequence_index={sequence_index} run_number={j}"
            ]
        }


# def task_clear():
#     return {
#         'actions': ['doit -f dodo1.py clear']
#     }

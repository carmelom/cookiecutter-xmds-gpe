#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Created: 07-2020 - Carmelo Mordini <carmelo> <carmelo.mordini@unitn.it>

"""Module docstring

"""
from pathlib import Path
import itertools
from copy import deepcopy

from ruamel import yaml
from pprint import pprint

DOIT_CONFIG = {
    'verbosity': 2,
    'backend': 'json',
}


with open('configure.yaml', 'r') as f:
    conf = yaml.safe_load(f)

run_dir = Path(conf['run_dir'])
run_dir.mkdir(parents=True, exist_ok=True)
sequence_index = len(list(run_dir.iterdir()))

scan = {
    'imprint_x0': list(range(1, 5, 1)),
}

keys, values = list(zip(*scan.items()))

shots = []
for item in itertools.product(*values):
    conf['globals'].update(dict(zip(keys, item)))
    shots.append(deepcopy(conf))

# pprint(shots)


def task_run_sequence():
    def _write_conf(_conf, filename):
        print("WRITING")
        pprint(_conf)
        with open(filename, 'w') as f:
            f.write(yaml.safe_dump(_conf))

    for j, conf in enumerate(shots):
        conf_name = f'_config.yaml'
        yield {
            'name': j,
            'actions': [
                (_write_conf, [conf, conf_name]),
                f"doit -f dodo1.py config_file={conf_name} sequence_index={sequence_index} run_number={j}"
            ]
        }

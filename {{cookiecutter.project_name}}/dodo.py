#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Create: 01-2020 - Carmelo Mordini <carmelo> <carmelo.mordini@unitn.it>

"""Module docstring

"""
from pathlib import Path
from src import tasks
from src import h5tools
from doit import get_var

from ruamel import yaml

DOIT_CONFIG = {
    'verbosity': 2,
    'backend': 'json',
    # 'default_tasks': [
    #     'groundstate',
    #     'realtime',
    #     'collect'
    # ],
    'dep_file': '.doit.db',
}

config_file = get_var('config_file', 'configure.yaml')

with open(config_file, 'r') as f:
    conf = yaml.safe_load(f)


build_dir = Path(conf['build_dir'])
build_dir.mkdir(parents=True, exist_ok=True)

run_dir = Path(conf['run_dir'])

sequence_index = int(get_var('sequence_index', h5tools.autosequence(run_dir)))
run_number = int(get_var('run_number', 0))

h5filepath = run_dir / \
    conf['h5filepath'].format(
        sequence_index=sequence_index, run_number=run_number)


def task_groundstate():
    name = 'groundstate'
    _conf = tasks.conf_update(conf, name)
    return tasks.xmds_run(build_dir, _conf)


def task_realtime():
    name = 'realtime'
    _conf = tasks.conf_update(conf, name)
    return tasks.xmds_run(build_dir, _conf)


def task_collect():
    actions = [(h5tools.mkpath, [h5filepath, conf])]
    fdeps = []
    for name in 'groundstate', 'realtime':
        target_file = build_dir / conf[name]['output_filename']
        action = (h5tools.copy_group, [target_file, h5filepath, name])
        actions.append(action)
        fdeps.append(target_file)

    return {
        'actions': actions,
        'file_dep': fdeps
    }

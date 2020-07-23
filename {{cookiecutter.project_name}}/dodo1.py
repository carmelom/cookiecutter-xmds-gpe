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
    'dep_file': '.doit1.db',
}

config_file = get_var('config_file', 'configure.yaml')

with open(config_file, 'r') as f:
    conf = yaml.safe_load(f)

groundstate_output = conf['groundstate_output']
realtime_output = conf['realtime_output']

build_dir = Path(conf['build_dir'])
build_dir.mkdir(parents=True, exist_ok=True)

run_dir = Path(conf['run_dir'])

sequence_index = int(get_var('sequence_index', h5tools.autosequence(run_dir)))
run_number = int(get_var('run_number', 0))

h5filepath = run_dir / \
    conf['h5filepath'].format(
        sequence_index=sequence_index, run_number=run_number)


def task_groundstate():
    _conf = conf.copy()
    _conf.update({
        'exec_filename': 'groundstate',
        'output_filename': groundstate_output,
    })
    return tasks.xmds_run(build_dir, _conf)


def task_realtime():
    _conf = conf.copy()
    _conf['steps'] = int(round(_conf['runtime'] / _conf['dt'] / 100) * 100)
    _conf.update({
        'exec_filename': 'realtime',
        'init_filename': groundstate_output,
        'output_filename': realtime_output,
    })
    return tasks.xmds_run(build_dir, _conf)


def task_collect():
    def _mkpath():
        print(h5filepath)
        h5filepath.parent.mkdir(parents=True, exist_ok=True)

    return {
        'actions': [
            _mkpath,
            (h5tools.copy_attrs, [h5filepath, conf]),
            (h5tools.copy_group, [build_dir / groundstate_output,
                                  h5filepath, 'groundstate']),
            (h5tools.copy_group, [build_dir / realtime_output,
                                  h5filepath, 'realtime'])
        ],
        'file_dep': [build_dir / groundstate_output, build_dir / realtime_output],
    }

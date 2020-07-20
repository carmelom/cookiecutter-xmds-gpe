#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Create: 01-2020 - Carmelo Mordini <carmelo> <carmelo.mordini@unitn.it>

"""Module docstring

"""
from pathlib import Path
from movie import make_movie
import tasks

from doit import get_var

import h5py
from ruamel import yaml

DOIT_CONFIG = {
    'verbosity': 2,
    'backend': 'json',
    'default_tasks': [
        'groundstate',
        'realtime',
        'collect'
    ],
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

sequence_index = int(get_var('sequence_index', 0))
run_number = int(get_var('run_number', 0))

h5filepath = run_dir / \
    conf['h5filepath'].format(
        sequence_index=sequence_index, run_number=run_number)
h5filepath.parent.mkdir(parents=True, exist_ok=True)


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
    def _copy_attrs(h5file):
        with h5py.File(h5file, 'a') as fd:
            globals = conf.pop('globals')
            c = fd.require_group('configure')
            c.attrs.update(conf)
            g = c.require_group('globals')
            g.attrs.update(globals)

    def _copy_group(source, dest, group):
        with h5py.File(source, 'r') as fs:
            with h5py.File(dest, 'a') as fd:
                g = fd.require_group(group)
                for k in fs.keys():
                    try:
                        fs.copy(k, g)
                    except RuntimeError:
                        pass
    return {
        'actions': [
            (_copy_attrs, [h5filepath]),
            (_copy_group, [build_dir / groundstate_output,
                           h5filepath, 'groundstate']),
            (_copy_group, [build_dir /
                           realtime_output, h5filepath, 'realtime'])
        ],
        'file_dep': [build_dir / groundstate_output, build_dir / realtime_output],
        'targets': [h5filepath]
    }


def task_movie():
    return {
        'actions': [(make_movie, [h5filepath, 20, None], {})],
        'verbosity': 2
    }


def task_clear():
    return {
        'actions': [f'rm -r {build_dir}']
    }

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Create: 01-2020 - Carmelo Mordini <carmelo> <carmelo.mordini@unitn.it>

"""Module docstring

"""
from pathlib import Path
from src import tasks
from doit import get_var

import numpy as np
import h5py

from ruamel import yaml

DOIT_CONFIG = {
    'verbosity': 2,
    'backend': 'json',
    # 'default_tasks': [
    #     'merge',
    # ],
    'dep_file': '.doit_continue.db',
}

config_file = get_var('config_file', 'configure.yaml')

with open(config_file, 'r') as f:
    conf = yaml.safe_load(f)


build_dir = Path(conf['build_dir'])
build_dir.mkdir(parents=True, exist_ok=True)

run_dir = Path(conf['run_dir'])

sequence_index = int(get_var('sequence_index', None))  # this will raise a TypeError unless you specify it
run_number = int(get_var('run_number', 0))

h5filepath = run_dir / \
    conf['h5filepath'].format(
        sequence_index=sequence_index, run_number=run_number)

init_filename = build_dir / conf['continue']['init_filename']
output_filename = build_dir / conf['continue']['output_filename']


def task_init():
    def _init(source, dest):
        with h5py.File(source, 'r') as fs:
            g = fs['realtime/1']
            # just put them by hand now, don't try to be general
            x = g['x'][:]
            # y = g['y'][:]
            psiI = g['psiI'][-1, ...]
            psiR = g['psiR'][-1, ...]

        with h5py.File(dest, 'w') as fd:
            g = fd.require_group('1')
            g['x'] = x
            # g['y'] = y
            g['psiI'] = psiI
            g['psiR'] = psiR

    return {
        'actions': [(_init, (h5filepath, init_filename))],
        'file_dep': [h5filepath],
        'targets': [init_filename]
    }


def task_continue():
    name = 'continue'
    _conf = conf.copy()
    _conf['exec_filename'] = 'realtime'
    _conf.update(_conf[name])
    return tasks.xmds_run(build_dir, _conf)


def task_merge():
    tmpfile = run_dir / 'tmp.h5'

    def _merge(source, dest):
        with h5py.File(source, 'r') as f1:
            g1 = f1['1']
            t1 = g1['t'][:]
            psiI1 = g1['psiI'][:]
            psiR1 = g1['psiR'][:]

        with h5py.File(dest, 'a') as f0:
            g0 = f0['realtime/1']
            # please make sure that realtime has initial_sample="no"
            # otherwise read all the datasets with [1:]
            t0 = g0['t'][:]
            del g0['t']
            g0['t'] = np.concatenate([t0, t1 + t0[-1]])

            psiI0 = g0['psiI'][:]
            del g0['psiI']
            g0['psiI'] = np.concatenate([psiI0, psiI1], axis=0)

            psiR0 = g0['psiR'][:]
            del g0['psiR']
            g0['psiR'] = np.concatenate([psiR0, psiR1], axis=0)

    return {
        'actions': [
            (_merge, (output_filename, h5filepath)),
            # del[datatset] does not shrink the file size!
            # I would need to change the collect task to make the datasets expandable (maxshape=(None,))
            # but using h5repack is faster right now
            f"h5repack {h5filepath} {tmpfile}",
            f"mv {tmpfile} {h5filepath}"
        ]
    }

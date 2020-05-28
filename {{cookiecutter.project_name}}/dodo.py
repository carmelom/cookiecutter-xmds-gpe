#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Create: 01-2020 - Carmelo Mordini <carmelo> <carmelo.mordini@unitn.it>

"""Module docstring

"""
from pathlib import Path
from movie import make_movie
import tasks


build_path = Path('build')
build_path.mkdir(parents=True, exist_ok=True)


DOIT_CONFIG = {
    'verbosity': 1,
    # 'default_tasks': [
    #     'groundstate',
    #     'realtime',
    # ]
}

x0 = 3
runtime = 10
dt = 3e-3
steps = int(round(runtime / dt / 100) * 100)

groundstate_output = "groundstate.h5"
realtime_output = "soliton.h5"


def task_groundstate():
    conf = {
        'exec_filename': 'groundstate',
        'output_filename': groundstate_output,
        'globals': {'imprint_x0': x0}
    }
    return tasks.xmds_run(build_path, conf)


def task_realtime():
    conf = {
        'exec_filename': 'realtime',
        'init_filename': groundstate_output,
        'output_filename': realtime_output,
        'globals': {},
        'runtime': runtime, 'steps': steps
    }
    return tasks.xmds_run(build_path, conf)


def task_movie():
    h5file = build_path / realtime_output
    return {
        'actions': [(make_movie, [h5file, 20, None], {})]
    }

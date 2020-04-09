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
    name = 'groundstate'
    conf = {
        'exec_filename': name,
        'output_filename': groundstate_output,
        'globals': {'imprint_x0': x0}
    }
    yield tasks.create_render_task(name, build_path, conf)
    yield tasks.create_compile_task(name, build_path)
    yield tasks.create_run_task(name, build_path, groundstate_output)


def task_realtime():
    name = 'realtime'
    init_filename = groundstate_output
    output_filename = realtime_output
    conf = {
        'exec_filename': name,
        'init_filename': init_filename,
        'output_filename': output_filename,
        'globals': {},
        'runtime': runtime, 'steps': steps
    }
    yield tasks.create_render_task(name, build_path, conf)
    yield tasks.create_compile_task(name, build_path)
    yield tasks.create_run_task(name, build_path, output_filename, init_filename)


def task_movie():
    h5file = build_path / realtime_output
    return {
        'actions': [(make_movie, [h5file, 20, None], {})]
    }

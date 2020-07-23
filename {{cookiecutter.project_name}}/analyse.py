#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Create: 01-2020 - Carmelo Mordini <carmelo> <carmelo.mordini@unitn.it>

"""Module docstring

"""
from pathlib import Path
from src.movie import make_movie

from doit import get_var

from ruamel import yaml

DOIT_CONFIG = {
    'verbosity': 2,
    'backend': 'json',
    'dep_file': '.doit_analyse.db',
}

config_file = get_var('config_file', 'configure.yaml')

with open(config_file, 'r') as f:
    conf = yaml.safe_load(f)


sequence_index = int(get_var('sequence_index', 0))
sequence_dir = Path(conf['run_dir']) / f"{sequence_index:04d}"

filenames = list(sequence_dir.iterdir())


def task_movie():
    for filename in filenames:
        run_number = int(filename.stem[-4:])
        yield {
            'name': run_number,
            'actions': [(make_movie, [filename, 20, None], {})],
        }

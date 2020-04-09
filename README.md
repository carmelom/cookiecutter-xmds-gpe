# cookiecutter-xmds-gpe
A cookiecutter to scaffold gpe projects run by [xmds](http://www.xmds.org/index.html). It uses [jinja](https://jinja.palletsprojects.com/en/2.11.x/) and [doit](https://pydoit.org/) to structure and run the simulation, and includes a simple data cisualization script based on `matplotlib` and optionally [moviepy](https://zulko.github.io/moviepy/)

## Quick recap

A gpe simulation is split into two parts:

- a `groundstate` step, to compute the initial state with imaginary time evolution
- a `realtime` step, which runs the real-time gpe starting from the output of the previous step.

Each step is split into three tasks:

- `render`, which edits the corresponding .xml file by injecting user variables
- `compile`, calls `xmds2` to compile the executable
- `run` runs the simulation

The correct task sequence is managed by `doit`, which can be used to insert an extra step to manipulate the wavefunction before running the realtime, e.g. with a phase imprint. Edit the .xml files in `templates` and `dodo.py` accordingly.

The provided template runs a simple 1D GPE in harmonic trap, with a phase imprint of a soliton and its time evolution.

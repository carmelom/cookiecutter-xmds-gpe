# cookiecutter-xmds-gpe
A cookiecutter to scaffold gpe projects run by [xmds](http://www.xmds.org/index.html). It uses [jinja](https://jinja.palletsprojects.com/en/2.11.x/) and [doit](https://pydoit.org/) to structure and run the simulation, and includes a simple data visualization script based on `matplotlib` and optionally [moviepy](https://zulko.github.io/moviepy/)

The provided template runs a simple 1D GPE in harmonic trap, where we phase-imprint a soliton at the beginning of the imaginary time evolution, and then we follow its real-time dynamics.

## How to (TL;DR)

Edit `configure.yaml` with the relevant parameters for your run, and

    doit

To run a "sequence", scanning one of the configurable parameters, edit the `scan` dictionary in `dodo_scan.py` and simply

    doit -f dodo_scan.py

### Single run

A gpe simulation is split into two parts:

- a `groundstate` step, to compute the initial state with imaginary time evolution
- a `realtime` step, which runs the real-time gpe starting from the output of the previous step.

Each step is split into three tasks:

- `render`, which edits the corresponding .xml file by injecting user variables
- `compile`, calls `xmds2` to compile the executable
- `run` runs the simulation

The `dodo.py` doit file puts all the steps together. Thanks to the powerful doit task management system, only the necessary pieces of the smulation are run each time.

The executable run in each task is defined by the `exec_filename` variable, and default to 'groundstate' and 'realtime' respectively. The corresponding xmds script is compiled from the `template` folder using Jinja. Feel free to customize the scripts and their { include }s to tweak the simulation at will. For a description of the Jinja templating syntax, please refer to the documentation.

Each step outputs a separate hdf5 file in the `build_dir` folder. At the end of the run, all the results are collected in a single file by a `collect` task under the folder structure

`{run_dir}/{sequence_index}/project_name_{run_number}.h5`

The `sequence_index` automatically increases at each run, and `run_number` indexes the different shots of a same sequence.

In many different scenarios it is useful to insert an intermediate step to manipulate the wavefunction before running the realtime, e.g. with a phase imprint. Edit the .xml files in `templates`, add a task in `dodo.py` accordingly, and edit `collect` in order to save the new results.


### Sequence
A separate doit file allows to run a sequence of simulations scanning one or more of the configurable parameters. The `scan` dictionary in `dodo_scan.py` can be filled with iterables corresponding to the parameters of the scan; doit will unpack it in a sequence of dictionaries, each representing a single simulation run, and will schedule them for execution. The results will be collected under a single sequence_index.

### Analysis
This is beyond the scope of this package, but I recommend (by experience) using doit even for the analysis of the simulation results. Here we provide a doit file (`analyse.py`) with a simple visualization of the results in a single sequence:

    doit -f analyse.py sequence_index=0 movie:0

Add more analysis tasks and tweak it to you needs.

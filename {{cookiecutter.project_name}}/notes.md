# Notes

what does xmgpe do. Input: N, trap freqs

Output:
constants like
- N
- a_scatt

things that depend on the geometry
- geometry
- initialize the wavefunction
- potential

all of this goes in the header

- (initial) timestep

write a render.py and call its functions from doit

all of this will go inside xmgpe
- all the lxml part can be substituted with jinja2 templating
- call cookiecutter (API) from xmgpe to scaffold a new project


TODO

- [x] three tasks per groundstate / realtime
  - render --> writes xmds from executable and variables
  - compile --> call xmds2 and compiles
  - run --> runs the executable, saves the result to a target h5 file
- [ ] phase imprint (or any other action before gs / rt)
  - implement tasks for that

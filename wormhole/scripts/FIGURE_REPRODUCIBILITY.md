# Reproduce Figure 1

Plotting code for Figure 1 of Sergei Slobodov, *Can a Wormhole Induce a
Monopole?*, [arXiv:2610.35969](https://arxiv.org/abs/2610.35969).

Run from the `wormhole` directory after checking out this branch or commit:

```sh
python -m pip install -r scripts/requirements-figure.txt
python -c "from pathlib import Path; Path('figures').mkdir(exist_ok=True)"
python scripts/make_thinshell_fixed_monopole_flux.py
```

The script writes `figures/fig_thinshell_fixed_monopole_flux.pdf` and a PNG
preview at the same path with the `.png` extension. It reads no external data.
Run it in a separate checkout if you want to preserve existing generated files.

The figure evaluates the zero-monopole-flux Maxwell solution described in
Eq. (3) of the paper. In the code, `A` denotes the throat radius (the paper's
`R`), `R0` the charge radius (the paper's `A`), and `Q` the charge. Defaults
are `A=1`, `R0=2`, and `Q=1`, with multipoles through `L_MAX=80` on a
700-by-421 radial/angular grid. Field lines are contours of the axisymmetric
stream function. The connecting arrows illustrate the widely separated
one-ended interpretation.

The plotting code was prepared with AI assistance and checked by the author,
as disclosed in the paper. The dependency versions used for the reproduction
check are pinned in `requirements-figure.txt`; Python 3.12 was used.

This publication branch contains the plotting script and its reproduction
instructions. Other files inherited from the repository's main branch may
refer to older manuscript drafts; the paper linked above is the submitted
version to which this figure belongs.

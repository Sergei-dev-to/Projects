# lexlife

Minimal `world-min` simulator for lexocytes on a 2D grid.

## Run

```bash
python experiments.py
python experiments.py --diagnostics
python sweep.py
python swarm_experiment.py
python swarm_viz.py
```

## Model

Each occupied grid site contains one lexocyte with:
- tiny weights
- hidden state
- prediction of the next dominant neighbor symbol
- emitted symbol

The world tracks a separate viability value for each occupied site.

At each tick, each lexocyte:
- receives an encoded neighborhood token
- updates hidden state through a tiny recurrent computation
- produces both a next-token prediction and an emitted token
- is evaluated one tick later against the next encoded neighborhood token
- exists in a world where viability decays by default, is supported or dragged by local density, and is eroded by prediction mismatch
- is removed if viability reaches zero

Module layout:
- `lexocyte_min.py`: organism-level primitive
- `interaction_min.py`: local, memoryless token encoder
- `world_min.py`: viability, failure, and repeated ticks
- `swarm_world.py`: separate swarm-first disturbance/trace/repair experiment
- `swarm_atom.py`: weak interchangeable predictive atoms for the swarm-first experiment

Concept docs:
- `SWARM_GOAL.md`
- `LEXOCYTE_MIN.md`
- `INTERACTION_MIN.md`
- `WORLD_MIN.md`
- `REPRODUCTION_MIN.md` (future layer, not active yet)

This is the smallest inspectable stack currently implemented that is still more than plain cellular automata.

Current conceptual order:
1. `SWARM_GOAL.md`
2. `LEXOCYTE_MIN.md`
3. `INTERACTION_MIN.md`
4. `WORLD_MIN.md`
5. `REPRODUCTION_MIN.md` (later)

Project direction:
- keep the atom minimally LLM-like
- keep the atom weak
- make swarm-scale emergence, not individual cleverness, the main test

Current encoder modes:
- `mode`: observe the dominant neighbor token
- `mode_mixed`: preserve dominant token, but remap mixed neighborhoods to a different token class

Current comparison:
- `mode` and `mode_mixed` both stabilize near a similar survivor count in the current tuned setup
- `mode_mixed` changes the observation distribution and token regime, but does not yet produce a qualitatively richer attractor on its own
- a small verification sweep suggests initial density and seed currently matter more than encoder choice for final survivor count

## Current Read

In the current tuned run, the system no longer collapses immediately to a stable pair. It settles into a sparse but persistent coupled survivor set of about 19 lexocytes.

In a small sweep over seeds `{1,2,3}`, populations `{48,64,80}`, and encoders `{mode, mode_mixed}`, the strongest runs in the current rule family came from `initial_population=80`, with final populations between 33 and 41.

That means the next useful step is still not reproduction yet.
The better next step is to explore `world-min` more deeply:
- compare alternative local encoders
- inspect richer nontrivial attractors
- run parameter sweeps for persistence without trivial collapse

Reproduction should wait until the non-reproductive world already supports interesting coupled dynamics.

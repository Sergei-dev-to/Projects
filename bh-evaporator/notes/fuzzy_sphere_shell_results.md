# Fuzzy-Sphere Shell Results

## Files

Model note:

```text
bh-evaporator/notes/fuzzy_sphere_evaporator_model.md
```

Verification script:

```text
bh-evaporator/sim/fuzzy_sphere_shells.py
```

## What Was Checked

For spin:

```text
j = (N-1)/2
```

construct the `N x N` generators:

```text
J_x, J_y, J_z.
```

Define the fuzzy-sphere Laplacian on matrices:

```text
Delta(A) = sum_i [J_i, [J_i, A]].
```

Then diagonalize `Delta` as a superoperator on `Mat_N`.

Expected spectrum:

```text
lambda_l = l(l+1)
degeneracy = 2l + 1
l = 0, 1, ..., N-1.
```

## Result

The check passes for tested sizes.

Example `N=8`:

```text
l=0  eigenvalue=0   degeneracy=1
l=1  eigenvalue=2   degeneracy=3
l=2  eigenvalue=6   degeneracy=5
l=3  eigenvalue=12  degeneracy=7
l=4  eigenvalue=20  degeneracy=9
l=5  eigenvalue=30  degeneracy=11
l=6  eigenvalue=42  degeneracy=13
l=7  eigenvalue=56  degeneracy=15
```

Total dimension:

```text
1 + 3 + 5 + ... + (2N-1) = N^2.
```

So the fuzzy sphere gives the exact angular shell structure:

```text
Mat_N = direct sum_{l=0}^{N-1} V_l.
```

## Evaporation Count

The shrinking step:

```text
N -> N-1
```

removes:

```text
dim Mat_N - dim Mat_(N-1) = N^2 - (N-1)^2 = 2N - 1.
```

That is exactly the outer shell:

```text
l = N-1,
dim V_{N-1} = 2N - 1.
```

So the proposed evaporation split:

```text
Mat_N -> Mat_(N-1) + shell(l=N-1)
```

is algebraically clean.

## Thermodynamic Skeleton

If each angular matrix mode carries an effective soft label of dimension `d`,
then:

```text
S_N = N^2 log d.
```

If:

```text
M_N = mu N,
```

then:

```text
T_N = (dS/dM)^-1 = mu / (2 N log d).
```

The script prints the skeleton. For `d=2`, `mu=1`:

```text
N=4: S=11.090, M=4, T=0.180
N=6: S=24.953, M=6, T=0.120
N=8: S=44.361, M=8, T=0.090
```

This is the desired:

```text
S ~ M^2
T ~ 1/M.
```

## Critical Caveat

The fuzzy-sphere Laplacian eigenvalues are:

```text
l(l+1).
```

So if these modes are treated as ordinary energetic field modes, the outer
shell is high-energy, not soft.

Therefore the fuzzy sphere solves:

```text
finite angular state counting.
```

It does not solve:

```text
why these angular labels are soft.
```

For the evaporator, the matrix harmonics must be interpreted as:

```text
edge labels;
memory sectors;
near-degenerate internal labels;
or constrained soft degrees of freedom.
```

not as ordinary Laplacian excitations.

## Current Judgment

The fuzzy sphere is a much better matrix model for the 2D/angular branch than
the earlier clump model.

It gives:

```text
1. exact angular shell decomposition;
2. exact N^2 area-like count;
3. exact outer-shell loss 2N-1 under N -> N-1;
4. a clean candidate soft radiation/memory shell.
```

The next problem is physical, not algebraic:

```text
What justifies the soft-label interpretation of the matrix harmonics?
```


# Boundary-Tension Droplet Count Results

## Question

Can the Schwarzschild-like equation of state:

```text
S(E) proportional to E^2
```

come from a non-gravitational droplet model with boundary-tension energy?

## Model

Script:

```text
sim/boundary_tension_droplet_count.py
```

Data:

```text
sim/data/boundary_tension_polyomino_entropy.csv
sim/data/boundary_tension_polyomino_thermo.csv
sim/data/boundary_tension_rectangle_entropy.csv
sim/data/boundary_tension_droplet_summary.csv
```

Droplet states:

```text
C = connected set of occupied cells on the square lattice
A(C) = number of occupied cells
P(C) = lattice perimeter
```

Each occupied cell carries `q` soft internal labels:

```text
number of labels for shape C = q^A(C)
```

Energy is boundary tension:

```text
E(C) = sigma P(C)
```

The fixed-perimeter microcanonical entropy is:

```text
S(P) = log sum_C q^A(C)
```

where the sum is over connected shapes with perimeter `P`.

## Checklist

### 1. Define the lattice droplet and perimeter energy

Done.

The microscopic ingredients are:

```text
connected occupied cells
q internal labels per cell
boundary-tension energy
```

This replaces:

```text
dim H_n = q^n
E_n = alpha sqrt(n)
```

with:

```text
entropy from occupied area labels
energy from boundary length
```

### 2. Count or sample compact connected configurations

Two calculations were done.

Exact small connected-shape enumeration:

```text
fixed polyominoes through area 12
```

Counts:

```text
area  shapes
1     1
2     2
3     6
4     19
5     63
6     216
7     760
8     2725
9     9910
10    36446
11    135268
12    505861
```

Compact rectangle family:

```text
best rectangle at fixed perimeter
```

This gives the clean large-size asymptotic because the optimal shape at fixed
perimeter is square-like.

### 3. Check whether entropy at fixed energy scales as E^2

For compact square-like droplets:

```text
P = 4L
A = L^2 = P^2 / 16
S = A log q
E = sigma P
```

Therefore:

```text
S(E) = (log q / 16 sigma^2) E^2
```

The rectangle data verifies this exactly. For `q = 2`:

```text
P    A     S          S/P^2
16   16    11.090     0.0433217
24   36    24.953     0.0433217
32   64    44.361     0.0433217
48   144   99.813     0.0433217
80   400   277.259    0.0433217
```

The coefficient is:

```text
log(2) / 16 = 0.0433217
```

So the compact droplet gives:

```text
S proportional to E^2
```

from area labels and boundary energy.

The exact polyomino enumeration is too small for a clean asymptotic fit at
large perimeter. The complete small-perimeter rows still show the same trend:

```text
q   complete S vs P^2 slope   expected compact slope
1   0.0359                   0
2   0.0620                   0.0433
4   0.0945                   0.0866
```

These exact small-size slopes include shape entropy and finite-size effects.
The rectangle line is the large compact-droplet benchmark.

### 4. Check failure modes

#### No soft area labels

For `q = 1`, internal label entropy vanishes. The remaining entropy is shape
entropy, giving a different mechanism from area-label entropy.

Lesson:

```text
area-extensive soft labels are essential.
```

#### Noncompact/ragged shapes

At fixed perimeter, ragged shapes have less area than compact shapes. With
large enough `q`, the `q^A` factor favors compact high-area droplets.

For small `q` and small sizes, shape entropy competes with area entropy.

Lesson:

```text
the droplet model needs either compactness, surface tension, or an ensemble
where area-label entropy dominates ragged-shape entropy.
```

#### Finite enumeration cutoff

Exact enumeration through area 12 becomes incomplete for larger perimeters.
High-perimeter fits from that enumeration underestimate compact high-area
states.

Lesson:

```text
use exact enumeration only as a small-size check;
use the compact isoperimetric family for the asymptotic equation of state.
```

#### Shape entropy versus internal entropy

The target mechanism is:

```text
S_soft = A log q
```

Shape entropy is an additional contribution. It can help at small sizes. The
clean target source is the internal constrained-label entropy.

Lesson:

```text
the model should treat internal constrained labels as the main entropy.
```

### 5. Map the droplet to the sector-Hamiltonian evaporator

The sector label becomes a linear size:

```text
L = droplet radius / side length
```

The sector Hilbert space is:

```text
H_L = soft constrained labels on the occupied droplet
dim H_L approximately q^(area)
```

The core energy is:

```text
E_L = sigma perimeter
```

For square droplets:

```text
dim H_L = q^(L^2)
E_L = 4 sigma L
```

Then:

```text
S_L = L^2 log q
E_L = 4 sigma L
T_L = (dS/dE)^-1 = 2 sigma / (L log q)
C_L < 0
```

This is the same thermodynamic backbone as the sector model, now with a
physical interpretation:

```text
sector entropy = area labels
sector energy = boundary tension
```

## Result

This is a real improvement over assigning:

```text
E_n = alpha sqrt(n)
```

The mass-equivalent law follows from:

```text
area entropy plus perimeter energy.
```

The derived equation of state is:

```text
S(E) = (log q / 16 sigma^2) E^2
```

for compact square lattice droplets.

## Remaining Work

The droplet count fixes the equation-of-state concern at the thermodynamic
level. It leaves the dynamical questions:

```text
1. What microscopic Hamiltonian maintains a compact active droplet?
2. What constrained model supplies the soft area labels?
3. How does the boundary erode unitarily?
4. How are hard radiation and soft shell information separated?
5. Can the sector-Hamiltonian scrambling/emission model be reinterpreted as
   this droplet's effective erosion dynamics?
```

The next step should connect this droplet equation of state to the successful
energy-resolved sector evaporator:

```text
replace sector label n by L^2;
replace imposed E_n by boundary energy 4 sigma L;
replace abstract shell H_n -> H_(n-1) by one-layer droplet erosion.
```

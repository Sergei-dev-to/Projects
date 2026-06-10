# F12 Mass-Law Control Results

## Question

Is F12 a showstopper?

In the program matrix, F12 was:

```text
sqrt-mass vs linear-mass controls
```

It was the only remaining `N` for the edge-tension droplet. The concern is
whether failing to run that control means we missed a serious ambiguity in the
mass law.

## Script

```text
sim/f12_mass_law_control.py
```

Output:

```text
sim/data/f12_mass_law_control.csv
```

## Control

Let:

```text
S(L) ~ L^2
M(L) ~ L^a
boundary B(L) ~ L
P(L) ~ B(L) T(L)^(d+1)
```

Then:

```text
T(L) = (dS/dM)^-1 ~ L^(a-2)
```

and:

```text
T(M) ~ M^((a-2)/a).
```

For a `d`-dimensional bath:

```text
P(L) ~ L * T^(d+1)
     ~ L^[1 + (a-2)(d+1)].
```

So:

```text
P(M) ~ M^[1 + (a-2)(d+1)]/a.
```

## Result For 2D Bath

The controls:

```text
control a   T~M^x      P~M^y      tau~M0^z   C<0
   0.500     -3.000     -7.000      8.000 True
   1.000     -1.000     -2.000      3.000 True
   2.000      0.000      0.500      0.500 False
```

Best match:

```text
best combined BH match: a=1.0000, T~M^-1.0000, P~M^-2.0000
best T match: a=1.0000
best P match: a=1.0000
```

So with:

```text
S ~ L^2
boundary emission
2D bath
```

the Schwarzschild-like exponents pick:

```text
M ~ L.
```

That is exactly the edge-tension law.

## Interpretation

F12 is not a showstopper.

It is actually a useful control because it shows:

```text
the edge-tension mass law is not an arbitrary choice after the rest of the
model is fixed.
```

If:

```text
M ~ L^a
```

then:

```text
T ~ 1/M
P ~ 1/M^2
tau ~ M0^3
```

all select:

```text
a = 1.
```

The original "sqrt-mass" concern was mostly a bookkeeping issue from earlier
models where the internal label was `n ~ S`. In that language:

```text
M ~ sqrt(n)
```

is the same as:

```text
n ~ L^2,
M ~ L.
```

So the current model did not lose the black-hole relation. It expressed it in
the geometrically natural variable `L`.

## Matrix Consequence

F12 should not remain a plain `N`.

A conservative update is:

```text
F12 = Y/P
```

or simply:

```text
F12 = P
```

because the exponent control has now been run and favors the current
edge-tension law. It is not a central phenomenology feature, but it is no
longer missing.

## Remaining Caveat

This control assumes the rest of the model:

```text
S ~ L^2
boundary emission
2D bath
```

If those change, the selected mass exponent changes. But within the current
edge-tension droplet architecture, F12 supports the model rather than
threatening it.

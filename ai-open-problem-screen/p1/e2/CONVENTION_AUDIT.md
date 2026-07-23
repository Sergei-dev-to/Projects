# Hand audit of the hive convention

This note expands the primary `n=3` fixture without relying on either evaluator.
It is meant to make a boundary rotation or a reversed rhombus inequality visible
to a human reviewer in one page.

For

```text
lambda = mu = (2,1),    nu = (3,2,1),    n = 3,
```

the frozen boundary convention gives

```text
lambda edge: q[0,0]=0, q[1,0]=2, q[2,0]=3, q[3,0]=3
nu edge:                    q[0,1]=3, q[0,2]=5, q[0,3]=6
mu edge:                                q[2,1]=5, q[1,2]=6
interior: q[1,1]=x.
```

This is the border pictured in Anders Buch, *The Saturation Conjecture (after
A. Knutson and T. Tao)*, Example 1
([arXiv:math/9810180](https://arxiv.org/abs/math/9810180)). Buch states that its
rhombi give `4 <= x <= 5` and hence two integer hives.

Our geometric generator produces all nine elementary rhombi as follows. Each
line is `sum(obtuse)-sum(acute) >= 0`.

| family | base `p` | expanded form | reduced form |
|---|---:|---|---|
| east–north | `(0,0)` | `q[1,0]+q[0,1]-q[0,0]-q[1,1]` | `5-x >= 0` |
| east–north | `(0,1)` | `q[1,1]+q[0,2]-q[0,1]-q[1,2]` | `x-4 >= 0` |
| east–north | `(1,0)` | `q[2,0]+q[1,1]-q[1,0]-q[2,1]` | `x-4 >= 0` |
| north–northwest | `(1,0)` | `q[1,1]+q[0,1]-q[1,0]-q[0,2]` | `x-4 >= 0` |
| north–northwest | `(1,1)` | `q[1,2]+q[0,2]-q[1,1]-q[0,3]` | `5-x >= 0` |
| north–northwest | `(2,0)` | `q[2,1]+q[1,1]-q[2,0]-q[1,2]` | `x-4 >= 0` |
| northwest–west | `(2,0)` | `q[1,1]+q[1,0]-q[2,0]-q[0,1]` | `x-4 >= 0` |
| northwest–west | `(2,1)` | `q[1,2]+q[1,1]-q[2,1]-q[0,2]` | `x-4 >= 0` |
| northwest–west | `(3,0)` | `q[2,1]+q[2,0]-q[3,0]-q[1,1]` | `5-x >= 0` |

Thus every orientation supplies the expected concavity direction, the unique
polytope is the interval `[4,5]` in the ordinary integer `x` lattice, and its
Ehrhart polynomial is `N+1`. The checked-in raw representation is
`reports/inputs/buch_n3_interval.hive.json`; the standalone Normaliz input and
output are under `reports/normaliz/`.

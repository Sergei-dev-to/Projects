"use strict";

// Fixed-mass jet sieve for planar Newtonian central configurations.
//
// The implementation is dependency-free.  It evaluates the central-
// configuration equations on truncated Taylor series, removes translation,
// rotation, and scale, and tests the successive compatibility conditions at a
// singular fixed-mass solution.

function zeroSeries(order) {
  return Array(order + 1).fill(0);
}

function constSeries(value, order) {
  const out = zeroSeries(order);
  out[0] = value;
  return out;
}

function addSeries(a, b) {
  return a.map((x, i) => x + b[i]);
}

function subSeries(a, b) {
  return a.map((x, i) => x - b[i]);
}

function scaleSeries(a, c) {
  return a.map(x => c * x);
}

function mulSeries(a, b) {
  const order = a.length - 1;
  const out = zeroSeries(order);
  for (let i = 0; i <= order; i++) {
    for (let j = 0; j + i <= order; j++) out[i + j] += a[i] * b[j];
  }
  return out;
}

function powSeries(a, exponent) {
  const order = a.length - 1;
  const a0 = a[0];
  if (!(a0 > 0)) throw new Error(`series power requires positive constant term, got ${a0}`);
  const u = scaleSeries(a, 1 / a0);
  u[0] -= 1;
  let term = constSeries(1, order);
  let sum = constSeries(1, order);
  let binomial = 1;
  for (let p = 1; p <= order; p++) {
    term = mulSeries(term, u);
    binomial *= (exponent - (p - 1)) / p;
    sum = addSeries(sum, scaleSeries(term, binomial));
  }
  return scaleSeries(sum, Math.pow(a0, exponent));
}

function dot(a, b) {
  let s = 0;
  for (let i = 0; i < a.length; i++) s += a[i] * b[i];
  return s;
}

function norm(a) {
  return Math.sqrt(dot(a, a));
}

function normalize(a) {
  const n = norm(a);
  if (n === 0) throw new Error("cannot normalize zero vector");
  return a.map(x => x / n);
}

function transpose(a) {
  return a[0].map((_, j) => a.map(row => row[j]));
}

function matMul(a, b) {
  const bt = transpose(b);
  return a.map(row => bt.map(col => dot(row, col)));
}

function matVec(a, x) {
  return a.map(row => dot(row, x));
}

function identity(n) {
  return Array.from({ length: n }, (_, i) =>
    Array.from({ length: n }, (_, j) => i === j ? 1 : 0));
}

// Jacobi diagonalization for the small real symmetric matrices used here.
function symmetricEigen(a, tolerance = 1e-14) {
  const n = a.length;
  const d = a.map(row => row.slice());
  const v = identity(n);
  const maxIterations = 100 * n * n;
  for (let iter = 0; iter < maxIterations; iter++) {
    let p = 0, q = 1, max = 0;
    for (let i = 0; i < n; i++) {
      for (let j = i + 1; j < n; j++) {
        const x = Math.abs(d[i][j]);
        if (x > max) { max = x; p = i; q = j; }
      }
    }
    if (max < tolerance) break;
    const app = d[p][p], aqq = d[q][q], apq = d[p][q];
    const phi = 0.5 * Math.atan2(2 * apq, aqq - app);
    const c = Math.cos(phi), s = Math.sin(phi);

    for (let k = 0; k < n; k++) {
      if (k === p || k === q) continue;
      const dkp = d[k][p], dkq = d[k][q];
      d[k][p] = d[p][k] = c * dkp - s * dkq;
      d[k][q] = d[q][k] = s * dkp + c * dkq;
    }
    d[p][p] = c * c * app - 2 * s * c * apq + s * s * aqq;
    d[q][q] = s * s * app + 2 * s * c * apq + c * c * aqq;
    d[p][q] = d[q][p] = 0;
    for (let k = 0; k < n; k++) {
      const vkp = v[k][p], vkq = v[k][q];
      v[k][p] = c * vkp - s * vkq;
      v[k][q] = s * vkp + c * vkq;
    }
  }
  const pairs = Array.from({ length: n }, (_, i) => ({
    value: d[i][i],
    vector: v.map(row => row[i])
  })).sort((x, y) => x.value - y.value);
  return {
    values: pairs.map(x => x.value),
    vectors: pairs.map(x => normalize(x.vector))
  };
}

function solveLinear(aInput, bInput, pivotTolerance = 1e-13) {
  const n = bInput.length;
  const a = aInput.map((row, i) => row.slice().concat([bInput[i]]));
  for (let col = 0; col < n; col++) {
    let pivot = col;
    for (let row = col + 1; row < n; row++) {
      if (Math.abs(a[row][col]) > Math.abs(a[pivot][col])) pivot = row;
    }
    if (Math.abs(a[pivot][col]) < pivotTolerance) {
      throw new Error(`singular linear system at column ${col}: ${a[pivot][col]}`);
    }
    [a[col], a[pivot]] = [a[pivot], a[col]];
    const scale = a[col][col];
    for (let j = col; j <= n; j++) a[col][j] /= scale;
    for (let row = 0; row < n; row++) {
      if (row === col) continue;
      const factor = a[row][col];
      if (factor === 0) continue;
      for (let j = col; j <= n; j++) a[row][j] -= factor * a[col][j];
    }
  }
  return a.map(row => row[n]);
}

function determinant(aInput, pivotTolerance = 1e-18) {
  const n = aInput.length;
  const a = aInput.map(row => row.slice());
  let sign = 1;
  let value = 1;
  for (let col = 0; col < n; col++) {
    let pivot = col;
    for (let row = col + 1; row < n; row++) {
      if (Math.abs(a[row][col]) > Math.abs(a[pivot][col])) pivot = row;
    }
    if (Math.abs(a[pivot][col]) < pivotTolerance) return 0;
    if (pivot !== col) {
      [a[col], a[pivot]] = [a[pivot], a[col]];
      sign *= -1;
    }
    const diagonal = a[col][col];
    value *= diagonal;
    for (let row = col + 1; row < n; row++) {
      const factor = a[row][col] / diagonal;
      for (let j = col + 1; j < n; j++) a[row][j] -= factor * a[col][j];
    }
  }
  return sign * value;
}

function makeProblem({ name, masses, inertia, omittedBody = 0, omittedComponent = "y" }) {
  if (masses.some(m => m === 0)) throw new Error("all masses must be nonzero");
  const n = masses.length;
  const dimension = 2 * (n - 1) + 1;
  return { name, masses, inertia, omittedBody, omittedComponent, n, dimension };
}

function evaluateSeries(problem, coefficients, order) {
  const { masses, inertia, omittedBody, omittedComponent, n } = problem;
  const q = Array.from({ length: n }, () => ({
    x: zeroSeries(order), y: zeroSeries(order)
  }));
  for (let i = 0; i < n - 1; i++) {
    q[i].x = coefficients[2 * i].slice(0, order + 1);
    q[i].y = coefficients[2 * i + 1].slice(0, order + 1);
  }
  for (const component of ["x", "y"]) {
    let weighted = zeroSeries(order);
    for (let i = 0; i < n - 1; i++) {
      weighted = addSeries(weighted, scaleSeries(q[i][component], masses[i]));
    }
    q[n - 1][component] = scaleSeries(weighted, -1 / masses[n - 1]);
  }
  const lambda = coefficients[2 * (n - 1)].slice(0, order + 1);
  const equations = [];
  for (let i = 0; i < n - 1; i++) {
    const acceleration = { x: zeroSeries(order), y: zeroSeries(order) };
    for (let j = 0; j < n; j++) {
      if (i === j) continue;
      const dx = subSeries(q[j].x, q[i].x);
      const dy = subSeries(q[j].y, q[i].y);
      const r2 = addSeries(mulSeries(dx, dx), mulSeries(dy, dy));
      const invr3 = powSeries(r2, -1.5);
      acceleration.x = addSeries(acceleration.x,
        scaleSeries(mulSeries(dx, invr3), masses[j]));
      acceleration.y = addSeries(acceleration.y,
        scaleSeries(mulSeries(dy, invr3), masses[j]));
    }
    for (const component of ["x", "y"]) {
      if (i === omittedBody && component === omittedComponent) continue;
      equations.push(addSeries(acceleration[component],
        mulSeries(lambda, q[i][component])));
    }
  }

  let inertiaSeries = zeroSeries(order);
  for (let i = 0; i < n; i++) {
    const radius2 = addSeries(mulSeries(q[i].x, q[i].x), mulSeries(q[i].y, q[i].y));
    inertiaSeries = addSeries(inertiaSeries, scaleSeries(radius2, masses[i]));
  }
  inertiaSeries[0] -= inertia;
  equations.push(inertiaSeries);
  equations.push(q[omittedBody][omittedComponent].slice());

  if (equations.length !== problem.dimension) {
    throw new Error(`expected ${problem.dimension} equations, got ${equations.length}`);
  }
  return equations;
}

function constantCoefficients(z0, order) {
  return z0.map(value => constSeries(value, order));
}

function residualAt(problem, z0) {
  return evaluateSeries(problem, constantCoefficients(z0, 0), 0).map(s => s[0]);
}

function jacobianAt(problem, z0) {
  const n = problem.dimension;
  const j = Array.from({ length: n }, () => Array(n).fill(0));
  for (let col = 0; col < n; col++) {
    const coefficients = constantCoefficients(z0, 1);
    coefficients[col][1] = 1;
    const equations = evaluateSeries(problem, coefficients, 1);
    for (let row = 0; row < n; row++) j[row][col] = equations[row][1];
  }
  return j;
}

function nullBases(j, relativeTolerance = 1e-8, absoluteTolerance = 1e-10) {
  const jt = transpose(j);
  const rightEigen = symmetricEigen(matMul(jt, j));
  const leftEigen = symmetricEigen(matMul(j, jt));
  // Evaluating ||Jv|| is substantially more accurate for the nearly-zero
  // modes than taking sqrt of a cancellation-limited eigenvalue of J^T J.
  const singularValues = rightEigen.vectors.map(vector => norm(matVec(j, vector)));
  const largest = Math.max(...singularValues);
  const cutoff = Math.max(absoluteTolerance, relativeTolerance * largest);
  let nullity = singularValues.filter(x => x <= cutoff).length;
  if (nullity === 0) nullity = 1;
  const right = rightEigen.vectors.slice(0, nullity);
  const left = leftEigen.vectors.slice(0, nullity);
  return { singularValues, cutoff, nullity, right, left };
}

function combineBasis(basis, coefficients) {
  const out = Array(basis[0].length).fill(0);
  for (let k = 0; k < basis.length; k++) {
    for (let i = 0; i < out.length; i++) out[i] += coefficients[k] * basis[k][i];
  }
  return out;
}

function borderedSolve(j, rightBasis, leftBasis, rhs) {
  const n = j.length, r = rightBasis.length;
  const a = Array.from({ length: n + r }, () => Array(n + r).fill(0));
  const b = Array(n + r).fill(0);
  for (let i = 0; i < n; i++) {
    for (let k = 0; k < n; k++) a[i][k] = j[i][k];
    for (let k = 0; k < r; k++) a[i][n + k] = leftBasis[k][i];
    b[i] = rhs[i];
  }
  for (let k = 0; k < r; k++) {
    for (let i = 0; i < n; i++) a[n + k][i] = rightBasis[k][i];
  }
  const solution = solveLinear(a, b);
  return { correction: solution.slice(0, n), obstruction: solution.slice(n) };
}

function jetSieve(problem, z0, {
  maxOrder = 6,
  directionVector = null,
  directionCoefficients = null,
  nullTolerance = 1e-8,
  stopTolerance = 1e-8
} = {}) {
  const f0 = residualAt(problem, z0);
  const j = jacobianAt(problem, z0);
  const bases = nullBases(j, nullTolerance);
  let tangent;
  if (directionVector) {
    tangent = normalize(directionVector);
  } else if (directionCoefficients) {
    tangent = normalize(combineBasis(bases.right, directionCoefficients));
  } else {
    tangent = bases.right[0].slice();
  }
  const tangentResidual = norm(matVec(j, tangent));
  const coefficients = constantCoefficients(z0, maxOrder);
  for (let i = 0; i < tangent.length; i++) coefficients[i][1] = tangent[i];
  const orders = [{ order: 1, obstructionNorm: tangentResidual, obstruction: [] }];
  let stoppedAt = null;

  for (let k = 2; k <= maxOrder; k++) {
    const equations = evaluateSeries(problem, coefficients, k);
    const forcing = equations.map(series => series[k]);
    const solved = borderedSolve(j, bases.right, bases.left, forcing.map(x => -x));
    const obstructionNorm = norm(solved.obstruction);
    orders.push({
      order: k,
      forcingNorm: norm(forcing),
      correctionNorm: norm(solved.correction),
      obstructionNorm,
      obstruction: solved.obstruction
    });
    for (let i = 0; i < solved.correction.length; i++) coefficients[i][k] = solved.correction[i];
    if (obstructionNorm > stopTolerance) {
      stoppedAt = k;
      break;
    }
  }
  return {
    problem: problem.name,
    baseResidualNorm: norm(f0),
    singularValues: bases.singularValues,
    nullCutoff: bases.cutoff,
    nullity: bases.nullity,
    tangentResidual,
    stoppedAt,
    orders,
    tangent,
    coefficients
  };
}

function robertsCalibration() {
  const a = 3 / 5, b = 4 / 5;
  const problem = makeProblem({
    name: "Roberts continuum at (a,b)=(3/5,4/5)",
    masses: [1, 1, 1, 1, -1 / 4],
    inertia: 2
  });
  const z0 = [a, 0, -a, 0, 0, b, 0, -b, 2];
  const exactTangent = [1, 0, -1, 0, 0, -a / b, 0, a / b, 0];
  return jetSieve(problem, z0, {
    maxOrder: 6,
    directionVector: exactTangent,
    stopTolerance: 2e-8
  });
}

function triangleCenterCalibration() {
  const root3 = Math.sqrt(3);
  const centralMass = (81 + 64 * root3) / 249;
  const problem = makeProblem({
    name: "degenerate equilateral triangle plus central positive mass",
    masses: [1, 1, 1, centralMass],
    inertia: 3
  });
  const z0 = [
    1, 0,
    -1 / 2, root3 / 2,
    -1 / 2, -root3 / 2,
    centralMass + 1 / root3
  ];
  const probe = jetSieve(problem, z0, { maxOrder: 2, stopTolerance: 1e-8 });
  const nullity = probe.nullity;
  const sweep = [];
  if (nullity === 1) {
    sweep.push(probe);
  } else if (nullity === 2) {
    for (let i = 0; i < 72; i++) {
      const theta = Math.PI * i / 72;
      const result = jetSieve(problem, z0, {
        maxOrder: 2,
        directionCoefficients: [Math.cos(theta), Math.sin(theta)],
        stopTolerance: 1e-8
      });
      sweep.push({ theta, order2: result.orders[1] });
    }
  }
  const obstructionNorms = sweep.map(item =>
    item.order2 ? item.order2.obstructionNorm : item.orders[1].obstructionNorm);
  return {
    problem: problem.name,
    centralMass,
    baseResidualNorm: probe.baseResidualNorm,
    singularValues: probe.singularValues,
    nullity,
    directionSweepCount: sweep.length,
    minimumOrder2Obstruction: Math.min(...obstructionNorms),
    maximumOrder2Obstruction: Math.max(...obstructionNorms),
    sample: sweep.slice(0, 4)
  };
}

// Chen--Hsiao's convex-but-not-strictly-convex five-body family.  Their
// reciprocal-distance parameter is theta = r_13^{-3}; all distances are
// scaled so that lambda equals the total mass.  Unlike a generic continuation,
// both mass parameters are explicit functions of theta.
function chenHsiaoFamily(theta) {
  if (!(theta > 1 && theta < 2)) throw new Error("theta must lie in (1,2)");
  const aDistance2 = Math.pow(theta, -2 / 3);
  const bDistance2 = Math.pow(2 - theta, -2 / 3);
  const alpha = Math.sqrt((aDistance2 + bDistance2 - 2) / 2);
  const beta = (bDistance2 - aDistance2) / (4 * alpha);
  const gamma = Math.sqrt(1 - beta * beta);
  const s12 = 1 / (8 * Math.pow(alpha, 3));
  const s34 = 1 / (8 * Math.pow(beta, 3));
  const mu = (theta - 1) * alpha / ((s34 - 1) * beta);
  const nu = -(
    (2 - 2 * s12) * (s34 - 1) + 2 * Math.pow(theta - 1, 2)
  ) / ((1 - 8 * s12) * (s34 - 1));
  const totalMass = 2 + 2 * mu + nu;
  const gamma1 = 2 * mu * gamma / totalMass;
  const gamma2 = (2 + nu) * gamma / totalMass;
  const raw = [
    [-alpha, -gamma1],
    [alpha, -gamma1],
    [-beta, gamma2],
    [beta, gamma2],
    [0, -gamma1]
  ];

  // Rotate q1 onto the x-axis, matching the gauge used by makeProblem.
  const radius = Math.hypot(raw[0][0], raw[0][1]);
  const cosine = raw[0][0] / radius;
  const sine = -raw[0][1] / radius;
  const positions = raw.map(([x, y]) => [
    cosine * x - sine * y,
    sine * x + cosine * y
  ]);
  const masses = [1, 1, mu, mu, nu];
  let inertia = 0;
  for (let i = 0; i < positions.length; i++) {
    inertia += masses[i] * (positions[i][0] ** 2 + positions[i][1] ** 2);
  }
  const problem = makeProblem({
    name: "Chen--Hsiao exceptional five-body degeneracy",
    masses,
    inertia
  });
  const z0 = positions.slice(0, 4).flat().concat([totalMass]);
  return {
    theta, alpha, beta, gamma, gamma1, gamma2, mu, nu, totalMass,
    masses, positions, inertia, problem, z0
  };
}

function permuteGaugedFamily(family, permutation) {
  const orderedMasses = permutation.map(i => family.masses[i]);
  const orderedRaw = permutation.map(i => family.positions[i]);
  const [x0, y0] = orderedRaw[0];
  const radius = Math.hypot(x0, y0);
  const cosine = x0 / radius;
  const sine = -y0 / radius;
  const positions = orderedRaw.map(([x, y]) => [
    cosine * x - sine * y,
    sine * x + cosine * y
  ]);
  const problem = makeProblem({
    name: family.problem.name,
    masses: orderedMasses,
    inertia: family.inertia
  });
  const z0 = positions.slice(0, 4).flat().concat([family.totalMass]);
  return { problem, z0, positions, masses: orderedMasses };
}

function bisectRoot(fn, left, right, iterations = 80) {
  let a = left, b = right;
  let fa = fn(a), fb = fn(b);
  if (!(Number.isFinite(fa) && Number.isFinite(fb) && fa * fb <= 0)) {
    throw new Error(`root is not bracketed: f(${a})=${fa}, f(${b})=${fb}`);
  }
  for (let i = 0; i < iterations; i++) {
    const middle = (a + b) / 2;
    const fm = fn(middle);
    if (fm === 0) return middle;
    if (fa * fm <= 0) {
      b = middle;
      fb = fm;
    } else {
      a = middle;
      fa = fm;
    }
  }
  return (a + b) / 2;
}

function chenHsiaoDegeneracy() {
  const determinantAt = theta => {
    const family = chenHsiaoFamily(theta);
    if (!(family.mu > 0 && family.nu > 0)) return NaN;
    return determinant(jacobianAt(family.problem, family.z0));
  };
  const brackets = [];
  let previous = null;
  const samples = 5000;
  for (let i = 0; i <= samples; i++) {
    const theta = 1.35 + (1.65 - 1.35) * i / samples;
    let family;
    try { family = chenHsiaoFamily(theta); } catch (_) { continue; }
    if (!(family.mu > 0 && family.nu > 0 && Number.isFinite(family.nu))) continue;
    const value = determinantAt(theta);
    if (!Number.isFinite(value)) continue;
    if (previous && previous.value * value < 0) {
      brackets.push([previous.theta, theta]);
    }
    previous = { theta, value };
  }
  const roots = brackets.map(([left, right]) => bisectRoot(determinantAt, left, right));
  if (roots.length === 0) throw new Error("no determinant sign change found in family");
  const theta = roots.reduce((best, candidate) => {
    const error = Math.abs(chenHsiaoFamily(candidate).nu - 0.5180855751);
    const bestError = Math.abs(chenHsiaoFamily(best).nu - 0.5180855751);
    return error < bestError ? candidate : best;
  }, roots[0]);
  const family = chenHsiaoFamily(theta);
  const sieve = jetSieve(family.problem, family.z0, {
    maxOrder: 6,
    nullTolerance: 2e-7,
    stopTolerance: 1e-7
  });
  const rotatedTangent = [];
  for (let i = 0; i < 4; i++) {
    rotatedTangent.push([sieve.tangent[2 * i], sieve.tangent[2 * i + 1]]);
  }
  let weightedX = 0, weightedY = 0;
  for (let i = 0; i < 4; i++) {
    weightedX += family.masses[i] * rotatedTangent[i][0];
    weightedY += family.masses[i] * rotatedTangent[i][1];
  }
  rotatedTangent.push([
    -weightedX / family.masses[4],
    -weightedY / family.masses[4]
  ]);
  const gaugeRadius = Math.hypot(family.alpha, family.gamma1);
  const gaugeCosine = -family.alpha / gaugeRadius;
  const gaugeSine = family.gamma1 / gaugeRadius;
  const rawTangent = rotatedTangent.map(([x, y]) => [
    gaugeCosine * x + gaugeSine * y,
    -gaugeSine * x + gaugeCosine * y
  ]);
  const rawPositions = [
    [-family.alpha, -family.gamma1],
    [family.alpha, -family.gamma1],
    [-family.beta, family.gamma2],
    [family.beta, family.gamma2],
    [0, -family.gamma1]
  ];
  // Choose the equivalent tangent modulo rotation for which the middle body
  // has zero horizontal velocity.  Reflection symmetry is then manifest.
  const angularCorrection = -rawTangent[4][0] / family.gamma1;
  const symmetryAdaptedTangent = rawTangent.map(([dx, dy], i) => {
    const [x, y] = rawPositions[i];
    return [dx - angularCorrection * y, dy + angularCorrection * x];
  });
  const collinearityDerivative = symmetryAdaptedTangent[4][1]
    - (symmetryAdaptedTangent[0][1] + symmetryAdaptedTangent[1][1]) / 2;
  const permutationChecks = [
    [0, 1, 2, 3, 4],
    [1, 2, 3, 4, 0],
    [2, 4, 0, 3, 1],
    [4, 3, 1, 0, 2]
  ].map(permutation => {
    const determinantForPermutation = parameter => {
      const point = chenHsiaoFamily(parameter);
      const gauged = permuteGaugedFamily(point, permutation);
      return determinant(jacobianAt(gauged.problem, gauged.z0));
    };
    const localTheta = bisectRoot(determinantForPermutation, 1.4934, 1.49346);
    const point = chenHsiaoFamily(localTheta);
    const gauged = permuteGaugedFamily(point, permutation);
    const localSieve = jetSieve(gauged.problem, gauged.z0, {
      maxOrder: 2,
      nullTolerance: 2e-7,
      stopTolerance: 1e-7
    });
    return {
      permutation,
      theta: localTheta,
      mu: point.mu,
      nu: point.nu,
      baseResidualNorm: localSieve.baseResidualNorm,
      tangentResidual: localSieve.tangentResidual,
      order2Obstruction: localSieve.orders[1].obstructionNorm
    };
  });
  return {
    problem: family.problem.name,
    theta: family.theta,
    mu: family.mu,
    nu: family.nu,
    totalMass: family.totalMass,
    inertia: family.inertia,
    positions: family.positions,
    unrotatedPositions: rawPositions,
    symmetryAdaptedTangent,
    collinearityDerivative,
    determinantBrackets: brackets,
    allRootParameters: roots.map(root => ({
      theta: root,
      mu: chenHsiaoFamily(root).mu,
      nu: chenHsiaoFamily(root).nu
    })),
    permutationChecks,
    sieve: summarize(sieve)
  };
}

function summarize(result) {
  return {
    problem: result.problem,
    baseResidualNorm: result.baseResidualNorm,
    nullity: result.nullity,
    singularValues: result.singularValues,
    stoppedAt: result.stoppedAt,
    orders: result.orders.map(x => ({
      order: x.order,
      obstructionNorm: x.obstructionNorm,
      forcingNorm: x.forcingNorm,
      correctionNorm: x.correctionNorm
    }))
  };
}

function main() {
  const mode = process.argv[2] || "all";
  const output = {};
  if (mode === "all" || mode === "roberts") output.roberts = summarize(robertsCalibration());
  if (mode === "all" || mode === "triangle") output.triangleCenter = triangleCenterCalibration();
  if (mode === "all" || mode === "chen-hsiao") output.chenHsiao = chenHsiaoDegeneracy();
  console.log(JSON.stringify(output, null, 2));
}

if (require.main === module) main();

module.exports = {
  makeProblem,
  residualAt,
  jacobianAt,
  nullBases,
  jetSieve,
  robertsCalibration,
  triangleCenterCalibration,
  chenHsiaoFamily,
  chenHsiaoDegeneracy,
  determinant
};

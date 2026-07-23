"use strict";

// Ramification census on the two-equal-pairs family (1,1,mu,mu,nu).
//
// Traces the singular set of the mass projection
//   { (z, mu, nu) : F(z; mu, nu) = 0, corank D_z F >= 1 }
// by pseudo-arclength continuation of the augmented system
//   H(z, v, mu, nu) = [ F ; (D_z F) v ; v.v - 1 ] = 0,
// starting from the certified Chen--Hsiao fold point.  Along the curve it
// evaluates the fixed-mass Lyapunov--Schmidt quadratic obstruction
//   Q = (1/2) w^T D_z^2 F [v, v],
// the mass-transversality projections w^T F_mu, w^T F_nu, and the second
// singular value of D_z F.  Ordinary folds have Q != 0 and are discarded.
// Candidate generation is intentionally incomplete: it records sampled sign
// crossings of Q and sampled near-corank-two points.  Tangential/even-order Q
// zeros and events between continuation steps require a separate search.
//
// Discovery-stage double precision only (Gate 4 of the stop/go protocol);
// survivors require exact escalation as in fold_interval_certificate.js.
//
// The masses enter the series evaluation as genuine Taylor variables, so all
// Jacobian blocks and second derivatives are exact modulo rounding; no finite
// differences are used anywhere.

const fs = require("fs");
const path = require("path");
const { chenHsiaoFamily, makeProblem, jetSieve } = require("./jet_sieve.js");

// ---------- series arithmetic (independent copy of the jet_sieve kernel) ----

function zeroSeries(order) { return Array(order + 1).fill(0); }

function constSeries(value, order) {
  const out = zeroSeries(order);
  out[0] = value;
  return out;
}

function addSeries(a, b) { return a.map((x, i) => x + b[i]); }
function subSeries(a, b) { return a.map((x, i) => x - b[i]); }
function scaleSeries(a, c) { return a.map(x => c * x); }

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

function dot(a, b) { let s = 0; for (let i = 0; i < a.length; i++) s += a[i] * b[i]; return s; }
function norm(a) { return Math.sqrt(dot(a, a)); }
function axpy(a, x, y) { return y.map((v, i) => v + a * x[i]); }

function normalizeVec(a) {
  const n = norm(a);
  if (n === 0) throw new Error("cannot normalize zero vector");
  return a.map(x => x / n);
}

function transpose(a) { return a[0].map((_, j) => a.map(row => row[j])); }
function matMul(a, b) { const bt = transpose(b); return a.map(row => bt.map(col => dot(row, col))); }
function matVec(a, x) { return a.map(row => dot(row, x)); }

function identity(n) {
  return Array.from({ length: n }, (_, i) =>
    Array.from({ length: n }, (_, j) => i === j ? 1 : 0));
}

function symmetricEigen(a, tolerance = 1e-14) {
  const n = a.length;
  const d = a.map(row => row.slice());
  const v = identity(n);
  const maxIterations = 120 * n * n;
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
    vectors: pairs.map(x => normalizeVec(x.vector))
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

// ---------- extended central-configuration equations ------------------------
//
// Extended variables Z = (q1x,q1y,q2x,q2y,q3x,q3y,q4x,q4y,lambda,mu,nu),
// eleven entries, each a Taylor series.  Masses are (1,1,mu,mu,nu); body 5 is
// eliminated by the center of mass; gauge: q1y = 0 equation, inertia fixed.
// Nine equations: seven force components (skipping body-1 y), inertia, q1y.

const DZ = 9;          // physical unknowns (8 coordinates + lambda)
const DEXT = 11;       // physical + (mu, nu)
const NEQ = DZ;        // square in z at fixed masses
const DX = 2 * DZ + 2; // augmented unknowns (z, v, mu, nu)
const NAUG = 2 * DZ + 1;

function evaluateExtended(coeffs, order, inertia) {
  const one = constSeries(1, order);
  const mu = coeffs[9].slice(0, order + 1);
  const nu = coeffs[10].slice(0, order + 1);
  const masses = [one, one, mu, mu, nu];
  const q = [];
  for (let i = 0; i < 4; i++) {
    q.push({ x: coeffs[2 * i].slice(0, order + 1), y: coeffs[2 * i + 1].slice(0, order + 1) });
  }
  let wx = zeroSeries(order), wy = zeroSeries(order);
  for (let i = 0; i < 4; i++) {
    wx = addSeries(wx, mulSeries(q[i].x, masses[i]));
    wy = addSeries(wy, mulSeries(q[i].y, masses[i]));
  }
  const invNu = powSeries(nu, -1);
  q.push({
    x: scaleSeries(mulSeries(wx, invNu), -1),
    y: scaleSeries(mulSeries(wy, invNu), -1)
  });
  const lambda = coeffs[8].slice(0, order + 1);
  const equations = [];
  for (let i = 0; i < 4; i++) {
    const acceleration = { x: zeroSeries(order), y: zeroSeries(order) };
    for (let j = 0; j < 5; j++) {
      if (i === j) continue;
      const dx = subSeries(q[j].x, q[i].x);
      const dy = subSeries(q[j].y, q[i].y);
      const r2 = addSeries(mulSeries(dx, dx), mulSeries(dy, dy));
      const invr3 = powSeries(r2, -1.5);
      acceleration.x = addSeries(acceleration.x, mulSeries(mulSeries(dx, invr3), masses[j]));
      acceleration.y = addSeries(acceleration.y, mulSeries(mulSeries(dy, invr3), masses[j]));
    }
    for (const component of ["x", "y"]) {
      if (i === 0 && component === "y") continue;
      equations.push(addSeries(acceleration[component], mulSeries(lambda, q[i][component])));
    }
  }
  let inertiaSeries = zeroSeries(order);
  for (let i = 0; i < 5; i++) {
    const radius2 = addSeries(mulSeries(q[i].x, q[i].x), mulSeries(q[i].y, q[i].y));
    inertiaSeries = addSeries(inertiaSeries, mulSeries(radius2, masses[i]));
  }
  inertiaSeries[0] -= inertia;
  equations.push(inertiaSeries);
  equations.push(q[0].y.slice());
  if (equations.length !== NEQ) throw new Error(`expected ${NEQ} equations`);
  return equations;
}

function constantExtended(Z, order) { return Z.map(value => constSeries(value, order)); }

function residualExt(Z, inertia) {
  return evaluateExtended(constantExtended(Z, 0), 0, inertia).map(s => s[0]);
}

// 9 x 11 Jacobian in all extended variables.
function fullJacobianExt(Z, inertia) {
  const j = Array.from({ length: NEQ }, () => Array(DEXT).fill(0));
  for (let col = 0; col < DEXT; col++) {
    const coeffs = constantExtended(Z, 1);
    coeffs[col][1] = 1;
    const equations = evaluateExtended(coeffs, 1, inertia);
    for (let row = 0; row < NEQ; row++) j[row][col] = equations[row][1];
  }
  return j;
}

// D^2 F [d, d] in extended variables (d has 11 entries).
function d2F(Z, d, inertia) {
  const coeffs = constantExtended(Z, 2);
  for (let i = 0; i < DEXT; i++) coeffs[i][1] = d[i];
  const equations = evaluateExtended(coeffs, 2, inertia);
  return equations.map(s => 2 * s[2]);
}

function d2FBilinear(Z, a, b, inertia) {
  const ab = a.map((x, i) => x + b[i]);
  const qab = d2F(Z, ab, inertia);
  const qa = d2F(Z, a, inertia);
  const qb = d2F(Z, b, inertia);
  return qab.map((x, i) => (x - qa[i] - qb[i]) / 2);
}

// ---------- augmented system ------------------------------------------------

function splitX(X) {
  const z = X.slice(0, DZ);
  const v = X.slice(DZ, 2 * DZ);
  const mu = X[2 * DZ], nu = X[2 * DZ + 1];
  return { z, v, mu, nu, Z: z.concat([mu, nu]) };
}

function evalH(X, inertia) {
  const { Z, v } = splitX(X);
  const Jf = fullJacobianExt(Z, inertia);
  const H = Array(NAUG).fill(0);
  const F = residualExt(Z, inertia);
  for (let r = 0; r < NEQ; r++) H[r] = F[r];
  for (let r = 0; r < NEQ; r++) {
    let s = 0;
    for (let k = 0; k < DZ; k++) s += Jf[r][k] * v[k];
    H[NEQ + r] = s;
  }
  H[2 * NEQ] = dot(v, v) - 1;
  return { H, Jf };
}

function jacobianH(X, inertia) {
  const { Z, v } = splitX(X);
  const Jf = fullJacobianExt(Z, inertia);
  const DH = Array.from({ length: NAUG }, () => Array(DX).fill(0));
  for (let r = 0; r < NEQ; r++) {
    for (let k = 0; k < DZ; k++) DH[r][k] = Jf[r][k];
    DH[r][2 * DZ] = Jf[r][9];
    DH[r][2 * DZ + 1] = Jf[r][10];
  }
  const vext = v.concat([0, 0]);
  const qvv = d2F(Z, vext, inertia);
  const unitCache = [];
  for (let col = 0; col < DEXT; col++) {
    const e = Array(DEXT).fill(0);
    e[col] = 1;
    unitCache.push(d2F(Z, e, inertia));
  }
  for (let col = 0; col < DEXT; col++) {
    const e = Array(DEXT).fill(0);
    e[col] = 1;
    const sum = vext.map((x, i) => x + e[i]);
    const qsum = d2F(Z, sum, inertia);
    const mixed = qsum.map((x, i) => (x - qvv[i] - unitCache[col][i]) / 2);
    const target = col < DZ ? col : (col === 9 ? 2 * DZ : 2 * DZ + 1);
    for (let r = 0; r < NEQ; r++) DH[NEQ + r][target] = mixed[r];
  }
  for (let r = 0; r < NEQ; r++) {
    for (let k = 0; k < DZ; k++) DH[NEQ + r][DZ + k] = Jf[r][k];
  }
  for (let k = 0; k < DZ; k++) DH[2 * NEQ][DZ + k] = 2 * v[k];
  return DH;
}

function tangentAt(X, inertia, orient) {
  const DH = jacobianH(X, inertia);
  const gram = matMul(transpose(DH), DH);
  const eig = symmetricEigen(gram);
  let T = eig.vectors[0];
  if (orient && dot(T, orient) < 0) T = T.map(x => -x);
  const residual = norm(matVec(DH, T));
  const gap = Math.sqrt(Math.max(eig.values[1], 0));
  return { T, residual, gap };
}

function newtonCorrect(Xpred, T, inertia, { tolerance = 1e-11, maxIterations = 10 } = {}) {
  let X = Xpred.slice();
  for (let iter = 0; iter < maxIterations; iter++) {
    let H;
    try { H = evalH(X, inertia).H; } catch (err) { return { ok: false, error: String(err) }; }
    const g = H.concat([dot(T, X.map((x, i) => x - Xpred[i]))]);
    const residual = norm(H);
    if (residual < tolerance && Math.abs(g[NAUG]) < 1e-9) {
      return { ok: true, X, residual, iterations: iter };
    }
    let DH;
    try { DH = jacobianH(X, inertia); } catch (err) { return { ok: false, error: String(err) }; }
    const A = DH.map(row => row.slice());
    A.push(T.slice());
    let delta;
    try { delta = solveLinear(A, g); } catch (err) { return { ok: false, error: String(err) }; }
    X = X.map((x, i) => x - delta[i]);
    if (norm(delta) > 10) return { ok: false, error: "diverging correction" };
  }
  return { ok: false, error: "no convergence" };
}

// ---------- monitors --------------------------------------------------------

function positionsOf(z, mu, nu) {
  const masses = [1, 1, mu, mu, nu];
  const q = [];
  for (let i = 0; i < 4; i++) q.push([z[2 * i], z[2 * i + 1]]);
  let wx = 0, wy = 0;
  for (let i = 0; i < 4; i++) { wx += masses[i] * q[i][0]; wy += masses[i] * q[i][1]; }
  q.push([-wx / nu, -wy / nu]);
  return q;
}

function minPairDistance(q) {
  let best = Infinity;
  for (let i = 0; i < q.length; i++) {
    for (let j = i + 1; j < q.length; j++) {
      const d = Math.hypot(q[i][0] - q[j][0], q[i][1] - q[j][1]);
      if (d < best) best = d;
    }
  }
  return best;
}

function monitors(X, inertia, wPrevious) {
  const { z, v, mu, nu, Z } = splitX(X);
  const Jf = fullJacobianExt(Z, inertia);
  const Jz = Jf.map(row => row.slice(0, DZ));
  const left = symmetricEigen(matMul(Jz, transpose(Jz)));
  let w = left.vectors[0];
  if (wPrevious && dot(w, wPrevious) < 0) w = w.map(x => -x);
  const JzT = transpose(Jz);
  const sigmas = left.vectors.map(u => norm(matVec(JzT, u))).sort((a, b) => a - b);
  const vext = v.concat([0, 0]);
  const Q = dot(w, d2F(Z, vext, inertia)) / 2;
  const wFmu = dot(w, Jf.map(row => row[9]));
  const wFnu = dot(w, Jf.map(row => row[10]));
  const q = positionsOf(z, mu, nu);
  return {
    mu, nu, lambda: z[8], Q, wFmu, wFnu,
    sigma1: sigmas[0], sigma2: sigmas[1],
    minDistance: minPairDistance(q),
    q1x: z[0],
    w
  };
}

// ---------- seed ------------------------------------------------------------

function buildSeed() {
  const theta = 1.493431096540984;
  const family = chenHsiaoFamily(theta);
  const inertia = family.inertia;
  const Z = family.z0.concat([family.mu, family.nu]);
  const Jf = fullJacobianExt(Z, inertia);
  const Jz = Jf.map(row => row.slice(0, DZ));
  const right = symmetricEigen(matMul(transpose(Jz), Jz));
  const v = right.vectors[0];
  let X = family.z0.concat(v, [family.mu, family.nu]);
  // Converge onto the augmented curve: Newton with the current numerical
  // tangent as the pseudo-arclength constraint.
  let { T } = tangentAt(X, inertia, null);
  const corrected = newtonCorrect(X, T, inertia, { tolerance: 1e-12 });
  if (!corrected.ok) throw new Error(`seed refinement failed: ${corrected.error}`);
  return { X: corrected.X, inertia, family };
}

// ---------- candidate refinement -------------------------------------------

function refineZero(Xa, Xb, Ta, inertia, wPrevious, quantity) {
  // Bisection on the segment chord with Newton reprojection; quantity is a
  // monitor key that changes sign between Xa and Xb.
  let a = Xa.slice(), b = Xb.slice();
  let fa = monitors(a, inertia, wPrevious)[quantity];
  const fb = monitors(b, inertia, wPrevious)[quantity];
  if (fa * fb > 0) return null;
  let last = null;
  for (let i = 0; i < 60; i++) {
    const mid = a.map((x, k) => (x + b[k]) / 2);
    const chord = normalizeVec(b.map((x, k) => x - a[k]));
    const corrected = newtonCorrect(mid, chord, inertia, { tolerance: 1e-12 });
    if (!corrected.ok) break;
    const mon = monitors(corrected.X, inertia, wPrevious);
    last = { X: corrected.X, monitor: mon };
    if (Math.abs(mon[quantity]) < 1e-12) break;
    if (fa * mon[quantity] <= 0) { b = corrected.X; } else { a = corrected.X; fa = mon[quantity]; }
    if (norm(b.map((x, k) => x - a[k])) < 1e-13) break;
  }
  return last;
}

function fixedMassJetCheck(X, inertia) {
  const { z, mu, nu } = splitX(X);
  const problem = makeProblem({
    name: `census candidate (mu=${mu}, nu=${nu})`,
    masses: [1, 1, mu, mu, nu],
    inertia
  });
  const sieve = jetSieve(problem, z, { maxOrder: 4, nullTolerance: 1e-6, stopTolerance: 1e-8 });
  return {
    nullity: sieve.nullity,
    singularValues: sieve.singularValues.slice(0, 3),
    orders: sieve.orders.map(o => ({ order: o.order, obstructionNorm: o.obstructionNorm })),
    stoppedAt: sieve.stoppedAt
  };
}

// ---------- continuation driver ---------------------------------------------

function traceDirection(seed, direction, options) {
  const {
    maxSteps = 4000,
    initialStep = 0.005,
    maxStep = 0.04,
    minStep = 1e-7,
    corankTwoThreshold = 5e-3
  } = options || {};
  const inertia = seed.inertia;
  let X = seed.X.slice();
  let { T } = tangentAt(X, inertia, null);
  // Orient the first tangent by the sign of its nu-component; direction ±1.
  const nuComponent = T[DX - 1];
  const orientSign = (nuComponent !== 0 ? Math.sign(nuComponent) : 1) * direction;
  if (orientSign < 0) T = T.map(x => -x);

  let ds = initialStep;
  let arclength = 0;
  let previousMonitor = monitors(X, inertia, null);
  let wPrevious = previousMonitor.w;
  const trace = [];
  const candidates = [];
  const events = [];
  let previousX = X.slice();
  let termination = "max steps reached";

  for (let step = 0; step < maxSteps; step++) {
    const Xpred = axpy(ds, T, X);
    const corrected = newtonCorrect(Xpred, T, inertia);
    if (!corrected.ok) {
      ds /= 2;
      if (ds < minStep) {
        termination = `step collapse: ${corrected.error}`;
        events.push({ step, arclength, type: "step-collapse", error: corrected.error });
        break;
      }
      continue;
    }
    const Xnew = corrected.X;
    const mon = monitors(Xnew, inertia, wPrevious);
    wPrevious = mon.w;

    if (previousMonitor) {
      if (previousMonitor.Q === 0 || mon.Q === 0 || previousMonitor.Q * mon.Q < 0) {
        const refined = refineZero(previousX, Xnew, T, inertia, wPrevious, "Q");
        if (refined) {
          const jet = (() => {
            try { return fixedMassJetCheck(refined.X, inertia); }
            catch (err) { return { error: String(err) }; }
          })();
          candidates.push({
            type: "Q-zero",
            step, arclength,
            mu: refined.monitor.mu, nu: refined.monitor.nu,
            lambda: refined.monitor.lambda,
            Q: refined.monitor.Q,
            wFmu: refined.monitor.wFmu, wFnu: refined.monitor.wFnu,
            sigma2: refined.monitor.sigma2,
            minDistance: refined.monitor.minDistance,
            X: refined.X,
            fixedMassJet: jet
          });
        } else {
          events.push({ step, arclength, type: "Q-zero-refinement-failed" });
        }
      }
    }
    if (mon.sigma2 < corankTwoThreshold) {
      events.push({
        step, arclength, type: "near-corank-two",
        mu: mon.mu, nu: mon.nu, sigma2: mon.sigma2
      });
    }

    trace.push({
      step, arclength: arclength + ds,
      mu: mon.mu, nu: mon.nu, lambda: mon.lambda,
      Q: mon.Q, wFmu: mon.wFmu, wFnu: mon.wFnu,
      sigma1: mon.sigma1, sigma2: mon.sigma2,
      minDistance: mon.minDistance, q1x: mon.q1x
    });

    if (!(mon.mu > 0 && mon.nu > 0)) {
      termination = "left positive-mass region";
      break;
    }
    if (mon.minDistance < 0.02) {
      termination = "approaching collision";
      break;
    }
    if (Math.abs(mon.q1x) < 0.02) {
      termination = "rotation gauge degenerating (q1 near origin)";
      break;
    }
    const distanceToSeed = norm(Xnew.map((x, i) => x - seed.X[i]));
    if (step > 25 && distanceToSeed < 1.5 * ds) {
      termination = "closed loop back to seed";
      break;
    }

    arclength += ds;
    // Keep the point and monitor paired.  The former code stored X here while
    // previousMonitor described Xnew, giving refineZero a two-step chord whose
    // endpoints did not necessarily bracket the detected sign change.
    previousX = Xnew.slice();
    previousMonitor = mon;
    let Tnew;
    try {
      Tnew = tangentAt(Xnew, inertia, T).T;
    } catch (err) {
      termination = `tangent failure: ${err}`;
      break;
    }
    X = Xnew;
    T = Tnew;
    if (corrected.iterations <= 3 && ds < maxStep) ds = Math.min(ds * 1.3, maxStep);
    if (step % 200 === 0) {
      process.stderr.write(
        `dir ${direction} step ${step} s=${arclength.toFixed(3)} ` +
        `mu=${mon.mu.toFixed(6)} nu=${mon.nu.toFixed(6)} Q=${mon.Q.toExponential(3)} ` +
        `sigma2=${mon.sigma2.toExponential(2)} dmin=${mon.minDistance.toFixed(3)}\n`);
    }
  }
  return { direction, termination, steps: trace.length, arclength, trace, candidates, events };
}

function main() {
  const seed = buildSeed();
  const seedMonitor = monitors(seed.X, seed.inertia, null);
  process.stderr.write(
    `seed: mu=${seedMonitor.mu} nu=${seedMonitor.nu} Q=${seedMonitor.Q} ` +
    `sigma1=${seedMonitor.sigma1.toExponential(2)} sigma2=${seedMonitor.sigma2.toExponential(2)} ` +
    `wFnu=${seedMonitor.wFnu}\n`);
  const residual = norm(evalH(seed.X, seed.inertia).H);
  if (residual > 1e-9) throw new Error(`seed residual too large: ${residual}`);

  const maxSteps = Number(process.env.CENSUS_MAX_STEPS || 4000);
  const forward = traceDirection(seed, +1, { maxSteps });
  const backward = traceDirection(seed, -1, { maxSteps });

  const thin = branch => ({
    direction: branch.direction,
    termination: branch.termination,
    steps: branch.steps,
    arclength: branch.arclength,
    muRange: [Math.min(...branch.trace.map(t => t.mu)), Math.max(...branch.trace.map(t => t.mu))],
    nuRange: [Math.min(...branch.trace.map(t => t.nu)), Math.max(...branch.trace.map(t => t.nu))],
    QRange: [Math.min(...branch.trace.map(t => t.Q)), Math.max(...branch.trace.map(t => t.Q))],
    sigma2Min: Math.min(...branch.trace.map(t => t.sigma2)),
    candidates: branch.candidates,
    events: branch.events.slice(0, 50)
  });

  const summary = {
    snapshot: new Date().toISOString(),
    seed: {
      mu: seedMonitor.mu, nu: seedMonitor.nu,
      Q: seedMonitor.Q, sigma1: seedMonitor.sigma1, sigma2: seedMonitor.sigma2,
      wFmu: seedMonitor.wFmu, wFnu: seedMonitor.wFnu,
      augmentedResidual: residual
    },
    forward: thin(forward),
    backward: thin(backward)
  };
  const summaryPath = path.join(__dirname, "census_summary.json");
  fs.writeFileSync(summaryPath, JSON.stringify(summary, null, 2));
  console.log(JSON.stringify(summary, null, 2));
  process.stderr.write(`summary written to ${summaryPath}\n`);

  const tracePath = path.join(__dirname, "census_trace.json");
  fs.writeFileSync(tracePath, JSON.stringify({
    seed: summary.seed,
    forward: { termination: forward.termination, trace: forward.trace },
    backward: { termination: backward.termination, trace: backward.trace }
  }));
  process.stderr.write(`full trace written to ${tracePath}\n`);
}

if (require.main === module) main();

module.exports = {
  evaluateExtended, residualExt, fullJacobianExt, d2F, d2FBilinear,
  evalH, jacobianH, tangentAt, newtonCorrect, monitors, buildSeed, traceDirection
};

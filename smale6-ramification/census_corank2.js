"use strict";

// Kernel-sphere quadratic-obstruction test at the corank-two census point:
// mu = 1 on the (1,1,mu,mu,nu) discriminant, i.e. four unit masses at the
// vertices of a square with a central body of mass nu at the degenerate value.
//
// The square-plus-center is an exact central configuration for every nu:
//   q1=(a,0), q2=(0,a), q3=(0,-a), q4=(-a,0), q5=(0,0),
//   lambda(nu) = (1/4 + 1/sqrt(2) + nu) / a^3.
// The gauge-fixed Jacobian loses rank at isolated nu.  This script locates
// the degenerate nu near the census crossing (nu ~ 2.3797), verifies the
// kernel dimension, and sweeps the fixed-mass order-two Lyapunov--Schmidt
// obstruction over the projective kernel circle, escalating to order three
// in any direction where the quadratic projection is small.
//
// Stop rule (retrospective Gate 4): the point is rejected as a continuum
// source only if every projective kernel direction carries a robust nonzero
// obstruction at some finite order.  A finite directional sweep is only
// discovery evidence for that universal condition.

const fs = require("fs");
const path = require("path");

const {
  makeProblem, residualAt, jacobianAt, jetSieve, determinant
} = require("./jet_sieve.js");

const INERTIA = (() => {
  // Match the census gauge: inertia value inherited from the Chen--Hsiao seed.
  const { chenHsiaoFamily } = require("./jet_sieve.js");
  return chenHsiaoFamily(1.493431096540984).inertia;
})();

function squareProblem(nu) {
  const a = Math.sqrt(INERTIA / 4);
  const lambda = (0.25 + Math.SQRT1_2 + nu) / Math.pow(a, 3);
  const problem = makeProblem({
    name: `square plus central mass nu=${nu}`,
    masses: [1, 1, 1, 1, nu],
    inertia: INERTIA
  });
  const z0 = [a, 0, 0, a, 0, -a, -a, 0, lambda];
  return { problem, z0, a, lambda };
}

function detAt(nu) {
  const { problem, z0 } = squareProblem(nu);
  return determinant(jacobianAt(problem, z0));
}

function bisect(fn, a, b, iterations = 90) {
  let fa = fn(a), fb = fn(b);
  if (!(fa * fb <= 0)) throw new Error(`not bracketed: f(${a})=${fa}, f(${b})=${fb}`);
  for (let i = 0; i < iterations; i++) {
    const m = (a + b) / 2;
    const fm = fn(m);
    if (fm === 0) return m;
    if (fa * fm <= 0) { b = m; fb = fm; } else { a = m; fa = fm; }
  }
  return (a + b) / 2;
}

function reconstructBinaryCubic(cubicSamples) {
  // For C(c,s)=A c^3+B c^2 s+C c s^2+D s^3, the samples at
  // 0, pi/4, pi/2, and 3pi/4 recover the four vector coefficients.
  const f0 = cubicSamples[0].obstruction;
  const f45 = cubicSamples[90].obstruction;
  const f90 = cubicSamples[180].obstruction;
  const f135 = cubicSamples[270].obstruction;
  const components = [];
  for (let j = 0; j < f0.length; j++) {
    const A = f0[j], D = f90[j];
    const sum = 2 * Math.SQRT2 * f45[j] - A - D;       // B+C
    const difference = 2 * Math.SQRT2 * f135[j] + A - D; // B-C
    components.push([A, (sum + difference) / 2, (sum - difference) / 2, D]);
  }
  return components;
}

function evaluateBinaryCubic(components, theta) {
  const c = Math.cos(theta), s = Math.sin(theta);
  return components.map(([A, B, C, D]) =>
    A * c * c * c + B * c * c * s + C * c * s * s + D * s * s * s);
}

function cubicFitAudit(cubicSamples) {
  const components = reconstructBinaryCubic(cubicSamples);
  let maxSampleVectorResidual = 0;
  for (const sample of cubicSamples) {
    const predicted = evaluateBinaryCubic(components, sample.theta);
    const residual = Math.hypot(...predicted.map((x, i) => x - sample.obstruction[i]));
    maxSampleVectorResidual = Math.max(maxSampleVectorResidual, residual);
  }

  const denseSamples = 1000000;
  let minNorm = Infinity, maxNorm = 0, argminTheta = 0, argmaxTheta = 0;
  for (let i = 0; i < denseSamples; i++) {
    const theta = Math.PI * i / denseSamples;
    const value = Math.hypot(...evaluateBinaryCubic(components, theta));
    if (value < minNorm) { minNorm = value; argminTheta = theta; }
    if (value > maxNorm) { maxNorm = value; argmaxTheta = theta; }
  }

  let sylvesterResultant = null;
  if (components.length === 2) {
    const [p, q] = components;
    sylvesterResultant = determinant([
      [p[0], p[1], p[2], p[3], 0, 0],
      [0, p[0], p[1], p[2], p[3], 0],
      [0, 0, p[0], p[1], p[2], p[3]],
      [q[0], q[1], q[2], q[3], 0, 0],
      [0, q[0], q[1], q[2], q[3], 0],
      [0, 0, q[0], q[1], q[2], q[3]]
    ]);
  }
  return {
    monomialOrder: ["c^3", "c^2 s", "c s^2", "s^3"],
    coefficientsByCokernelComponent: components,
    maxSampleVectorResidual,
    sylvesterResultant,
    denseSamples,
    minNorm,
    argminTheta,
    maxNorm,
    argmaxTheta
  };
}

function main() {
  // Verify the square is an exact solution away from the degeneracy.
  const check = squareProblem(2.0);
  const residual = Math.hypot(...residualAt(check.problem, check.z0));
  if (residual > 1e-12) throw new Error(`square residual too large: ${residual}`);

  // A symmetry doublet makes det touch zero quadratically without a sign
  // change, so locate degeneracies as interior minima of |det| and confirm
  // each by the smallest singular value.
  const samples = [];
  for (let i = 0; i <= 800; i++) {
    const nu = 2.0 + 0.8 * i / 800;
    samples.push({ nu, value: Math.abs(detAt(nu)) });
  }
  const minima = [];
  for (let i = 1; i < samples.length - 1; i++) {
    if (samples[i].value < samples[i - 1].value && samples[i].value < samples[i + 1].value) {
      minima.push([samples[i - 1].nu, samples[i + 1].nu]);
    }
  }
  const roots = minima.map(([lo, hi]) => {
    let a = lo, b = hi;
    for (let i = 0; i < 200; i++) {
      const m1 = a + (b - a) / 3, m2 = b - (b - a) / 3;
      if (Math.abs(detAt(m1)) < Math.abs(detAt(m2))) b = m2; else a = m1;
    }
    return (a + b) / 2;
  });

  const output = { inertia: INERTIA, squareResidual: residual, roots: [] };
  for (const nuStar of roots) {
    const { problem, z0, a, lambda } = squareProblem(nuStar);
    const probe = jetSieve(problem, z0, {
      maxOrder: 2, nullTolerance: 1e-6, stopTolerance: 1e-8
    });
    const entry = {
      nuStar, a, lambda,
      baseResidualNorm: probe.baseResidualNorm,
      singularValues: probe.singularValues.slice(0, 4),
      nullity: probe.nullity,
      sweep: null
    };
    if (probe.nullity >= 2) {
      const samples = 360;
      let min = Infinity, max = 0, argmin = 0;
      let min3 = Infinity, max3 = 0, argmin3 = 0, argmax3 = 0;
      const flagged = [];
      const cubicSamples = [];
      for (let i = 0; i < samples; i++) {
        const theta = Math.PI * i / samples;
        const result = jetSieve(problem, z0, {
          maxOrder: 4,
          directionCoefficients: [Math.cos(theta), Math.sin(theta)],
          nullTolerance: 1e-6,
          stopTolerance: 1e-8
        });
        const order2 = result.orders[1].obstructionNorm;
        if (order2 < min) { min = order2; argmin = theta; }
        if (order2 > max) max = order2;
        if (order2 < 1e-6) {
          const order3 = result.orders.find(o => o.order === 3);
          if (!order3) throw new Error("missing cubic obstruction at theta=" + theta);
          if (order3.obstructionNorm < min3) { min3 = order3.obstructionNorm; argmin3 = theta; }
          if (order3.obstructionNorm > max3) { max3 = order3.obstructionNorm; argmax3 = theta; }
          cubicSamples.push({ theta, obstruction: order3.obstruction });
          flagged.push({
            theta,
            orders: result.orders.map(o => ({ order: o.order, obstructionNorm: o.obstructionNorm })),
            stoppedAt: result.stoppedAt
          });
        }
      }
      entry.sweep = {
        samples,
        minOrder2Obstruction: min,
        maxOrder2Obstruction: max,
        argminTheta: argmin,
        minOrder3Obstruction: min3,
        maxOrder3Obstruction: max3,
        argminOrder3Theta: argmin3,
        argmaxOrder3Theta: argmax3,
        cubicFitAudit: cubicFitAudit(cubicSamples),
        flaggedDirections: flagged
      };
    } else {
      // Corank one at this root: single-direction jet is decisive.
      entry.sweep = {
        orders: probe.orders.map(o => ({ order: o.order, obstructionNorm: o.obstructionNorm })),
        stoppedAt: probe.stoppedAt
      };
    }
    output.roots.push(entry);
  }
  const outputPath = path.join(__dirname, "census_corank2_out.json");
  fs.writeFileSync(outputPath, JSON.stringify(output, null, 2));
  console.log(JSON.stringify(output, null, 2));
  process.stderr.write(`output written to ${outputPath}\n`);
}

main();

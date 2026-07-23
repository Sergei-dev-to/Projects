"use strict";

// Deterministic differential-evolution search for homothetic nested-rhombus
// continua. No external packages are used.

class RNG {
  constructor(seed = 0x9e3779b9) { this.s = seed >>> 0; }
  next() {
    let x = this.s;
    x ^= x << 13; x ^= x >>> 17; x ^= x << 5;
    this.s = x >>> 0;
    return this.s / 0x100000000;
  }
  int(n) { return Math.floor(this.next() * n); }
}

function makeConfig(u, radii, masses, centerMass = 0) {
  const a = Math.sqrt(u), b = Math.sqrt(1 - u);
  const q = [];
  for (let k = 0; k < radii.length; k++) {
    const r = radii[k], m = masses[k];
    q.push({ x: r * a, y: 0, m });
    q.push({ x: -r * a, y: 0, m });
    q.push({ x: 0, y: r * b, m });
    q.push({ x: 0, y: -r * b, m });
  }
  if (centerMass !== 0) q.push({ x: 0, y: 0, m: centerMass });
  return q;
}

function ccResidual(q) {
  const acc = q.map(() => ({ x: 0, y: 0 }));
  for (let i = 0; i < q.length; i++) {
    for (let j = 0; j < q.length; j++) if (i !== j) {
      const dx = q[j].x - q[i].x, dy = q[j].y - q[i].y;
      const r2 = dx * dx + dy * dy;
      const invr3 = 1 / (r2 * Math.sqrt(r2));
      acc[i].x += q[j].m * dx * invr3;
      acc[i].y += q[j].m * dy * invr3;
    }
  }
  let numer = 0, denom = 0;
  for (let i = 0; i < q.length; i++) {
    numer += acc[i].x * q[i].x + acc[i].y * q[i].y;
    denom += q[i].x * q[i].x + q[i].y * q[i].y;
  }
  const lambda = -numer / denom;
  let ss = 0, scale = 0, max = 0;
  for (let i = 0; i < q.length; i++) {
    const rx = acc[i].x + lambda * q[i].x;
    const ry = acc[i].y + lambda * q[i].y;
    ss += rx * rx + ry * ry;
    scale += acc[i].x * acc[i].x + acc[i].y * acc[i].y +
             lambda * lambda * (q[i].x * q[i].x + q[i].y * q[i].y);
    max = Math.max(max, Math.hypot(rx, ry));
  }
  return { relative: Math.sqrt(ss / Math.max(scale, 1e-300)), lambda, max };
}

function decode(x, levels, withCenter) {
  const radii = [1], masses = [1];
  for (let k = 1; k < levels; k++) radii.push(Math.exp(x[k - 1]));
  for (let k = 1; k < levels; k++) masses.push(Math.exp(x[levels - 1 + k - 1]));
  const centerMass = withCenter ? Math.exp(x[2 * (levels - 1)]) : 0;
  return { radii, masses, centerMass };
}

function objective(x, levels, withCenter, samples) {
  const p = decode(x, levels, withCenter);
  let sum = 0;
  // Avoid fake duplicate layers.
  for (let i = 0; i < p.radii.length; i++) for (let j = i + 1; j < p.radii.length; j++) {
    const d = Math.abs(Math.log(p.radii[i] / p.radii[j]));
    if (d < 0.04) sum += 100 * (0.04 - d) ** 2;
  }
  for (const u of samples) {
    const r = ccResidual(makeConfig(u, p.radii, p.masses, p.centerMass)).relative;
    sum += r * r;
  }
  return Math.sqrt(sum / samples.length);
}

function differentialEvolution(levels, withCenter, seed, generations = 1600) {
  const dim = 2 * (levels - 1) + (withCenter ? 1 : 0);
  const popSize = Math.max(50, 18 * dim);
  const rng = new RNG(seed);
  const lo = [], hi = [];
  for (let k = 0; k < levels - 1; k++) { lo.push(Math.log(0.18)); hi.push(Math.log(5.5)); }
  for (let k = 0; k < levels - 1; k++) { lo.push(Math.log(0.003)); hi.push(Math.log(80)); }
  if (withCenter) { lo.push(Math.log(0.003)); hi.push(Math.log(80)); }
  const samples = [0.12, 0.19, 0.28, 0.39, 0.5, 0.61, 0.72, 0.81, 0.88];
  const pop = Array.from({ length: popSize }, () =>
    Array.from({ length: dim }, (_, d) => lo[d] + rng.next() * (hi[d] - lo[d])));
  const fit = pop.map(v => objective(v, levels, withCenter, samples));
  let best = fit.indexOf(Math.min(...fit));
  for (let g = 0; g < generations; g++) {
    const F = 0.55 + 0.35 * rng.next(), CR = 0.75 + 0.2 * rng.next();
    for (let i = 0; i < popSize; i++) {
      let a, b, c;
      do a = rng.int(popSize); while (a === i);
      do b = rng.int(popSize); while (b === i || b === a);
      do c = rng.int(popSize); while (c === i || c === a || c === b);
      const forced = rng.int(dim);
      const trial = pop[i].slice();
      for (let d = 0; d < dim; d++) if (d === forced || rng.next() < CR) {
        trial[d] = pop[a][d] + F * (pop[b][d] - pop[c][d]);
        trial[d] = Math.max(lo[d], Math.min(hi[d], trial[d]));
      }
      const f = objective(trial, levels, withCenter, samples);
      if (f < fit[i]) { pop[i] = trial; fit[i] = f; if (f < fit[best]) best = i; }
    }
    if ((g + 1) % 200 === 0) {
      best = fit.indexOf(Math.min(...fit));
      process.stderr.write(`g=${g + 1} best=${fit[best].toExponential(6)}\n`);
    }
  }
  best = fit.indexOf(Math.min(...fit));
  const params = decode(pop[best], levels, withCenter);
  const held = [];
  for (let i = 1; i < 100; i++) {
    const u = 0.08 + 0.84 * i / 100;
    held.push(ccResidual(makeConfig(u, params.radii, params.masses, params.centerMass)).relative);
  }
  return { fit: fit[best], params, heldMax: Math.max(...held), vector: pop[best] };
}

function verifyRoberts() {
  const vals = [0.1, 0.23, 0.5, 0.77, 0.9].map(u => {
    const q = makeConfig(u, [1], [1], -0.25);
    return { u, ...ccResidual(q) };
  });
  console.log(JSON.stringify({ robertsCheck: vals }, null, 2));
}

function main() {
  verifyRoberts();
  const levels = Number(process.argv[2] || 2);
  const withCenter = (process.argv[3] || "center") !== "nocenter";
  const seed = Number(process.argv[4] || 123456789);
  const generations = Number(process.argv[5] || 1600);
  const result = differentialEvolution(levels, withCenter, seed, generations);
  console.log(JSON.stringify({ levels, withCenter, seed, generations, result }, null, 2));
}

main();


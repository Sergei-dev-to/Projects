"use strict";

// Numerical design aid for a rigorous Lyapunov--Schmidt certificate at the
// Chen--Hsiao five-body degeneracy.  This is deliberately dependency-free;
// it prints targets that can later be enclosed by interval arithmetic.

const { nullBases } = require("./jet_sieve.js");

function zeros(order) { return Array(order + 1).fill(0); }
function constant(x, order) { const a = zeros(order); a[0] = x; return a; }
function add(a, b) { return a.map((x, i) => x + b[i]); }
function sub(a, b) { return a.map((x, i) => x - b[i]); }
function scale(a, c) { return a.map(x => c * x); }
function mul(a, b) {
  const n = a.length - 1, c = zeros(n);
  for (let i = 0; i <= n; i++) for (let j = 0; i + j <= n; j++) c[i + j] += a[i] * b[j];
  return c;
}
function power(a, p) {
  const n = a.length - 1, a0 = a[0];
  const u = scale(a, 1 / a0); u[0] -= 1;
  let sum = constant(1, n), term = constant(1, n), bin = 1;
  for (let k = 1; k <= n; k++) {
    term = mul(term, u);
    bin *= (p - k + 1) / k;
    sum = add(sum, scale(term, bin));
  }
  return scale(sum, a0 ** p);
}
function dot(a, b) { return a.reduce((s, x, i) => s + x * b[i], 0); }
function norm(a) { return Math.sqrt(dot(a, a)); }

function forceEquationsAtPositions(q, masses) {
  const n = q.length, out = Array.from({ length: n }, () => [0, 0]);
  for (let i = 0; i < n; i++) {
    for (let j = 0; j < n; j++) {
      if (i === j) continue;
      const dx = q[j][0] - q[i][0], dy = q[j][1] - q[i][1];
      const s = (dx * dx + dy * dy) ** -1.5;
      out[i][0] += masses[j] * (1 - s) * dx;
      out[i][1] += masses[j] * (1 - s) * dy;
    }
  }
  return out;
}

// Odd block in a reflection-equivariant full gauge: COM=0, y2=y1.
// Odd coordinates are common horizontal motions of pair (1,2), common
// horizontal motions of pair (3,4), and opposite vertical motions of (3,4).
function oddEquations(u, base, mu, nu) {
  const [c1, c2, d2] = u;
  const { a, b, gamma1, gamma2 } = base;
  const q = [
    [-a + c1, -gamma1], [a + c1, -gamma1],
    [-b + c2, gamma2 + d2], [b + c2, gamma2 - d2],
    [0, 0]
  ];
  q[4][0] = -(q[0][0] + q[1][0] + mu * q[2][0] + mu * q[3][0]) / nu;
  q[4][1] = -(q[0][1] + q[1][1] + mu * q[2][1] + mu * q[3][1]) / nu;
  const e = forceEquationsAtPositions(q, [1, 1, mu, mu, nu]);
  return [e[0][0] + e[1][0], e[0][1] - e[1][1], e[2][0] + e[3][0]];
}

function finiteJacobian(fun, x, step = 1e-6) {
  const f0 = fun(x), J = Array.from({ length: f0.length }, () => Array(x.length).fill(0));
  for (let col = 0; col < x.length; col++) {
    const xp = x.slice(), xm = x.slice(); xp[col] += step; xm[col] -= step;
    const fp = fun(xp), fm = fun(xm);
    for (let row = 0; row < f0.length; row++) J[row][col] = (fp[row] - fm[row]) / (2 * step);
  }
  return J;
}

// Exact polynomialization. y=(a,b,h,k,A,B,C,D,E,G), where the capital
// variables denote the six distinct inverse cubes of mutual distances.
function polynomialH(y, mu, nu) {
  const [a, b, h, k, A, B, C, D, E, G] = y;
  const p12 = 64 * A * A * a ** 6 - 1;
  const p34 = 64 * B * B * b ** 6 - 1;
  const p13 = C * C * ((a - b) ** 2 + h * h) ** 3 - 1;
  const p14 = D * D * ((a + b) ** 2 + h * h) ** 3 - 1;
  const p35 = E * E * (b * b + (h - k) ** 2) ** 3 - 1;
  const p15 = G * G * (a * a + k * k) ** 3 - 1;
  const f1 = 2 * a * (1 - A)
    + mu * ((a - b) * (1 - C) + (a + b) * (1 - D))
    + nu * a * (1 - G);
  const f2 = mu * h * ((1 - C) + (1 - D)) + nu * k * (1 - G);
  const f3 = (b - a) * (1 - C) + (a + b) * (1 - D)
    + 2 * mu * b * (1 - B) + nu * b * (1 - E);
  const f4 = -2 * k * (1 - G) + 2 * mu * (h - k) * (1 - E);
  return [p12, p34, p13, p14, p35, p15, f1, f2, f3, f4];
}

function augmentedPolynomialSystem(z) {
  const y = z.slice(0, 10), mu = z[10], nu = z[11], v = z.slice(12, 22);
  const H = polynomialH(y, mu, nu);
  const Hx = finiteJacobian(t => polynomialH(t, mu, nu), y, 2e-6);
  const Hv = Hx.map(row => dot(row, v));
  return H.concat([y[3]], Hv, [v[3] - 1]);
}

// x=(a,b,h,k).  The reflection-symmetric positions, before translating to
// center of mass, are (-a,0),(a,0),(-b,h),(b,h),(0,k).
// The scale is fixed by setting the central-configuration multiplier equal
// to the total mass, as in Chen--Hsiao.
function symmetricEquationsSeries(x, mu, nu, order) {
  const [a, b, h, k] = x;
  const one = constant(1, order);
  const s12 = power(scale(mul(a, a), 4), -1.5);
  const s34 = power(scale(mul(b, b), 4), -1.5);
  const s13 = power(add(mul(sub(a, b), sub(a, b)), mul(h, h)), -1.5);
  const s14 = power(add(mul(add(a, b), add(a, b)), mul(h, h)), -1.5);
  const s35 = power(add(mul(b, b), mul(sub(h, k), sub(h, k))), -1.5);
  const s15 = power(add(mul(a, a), mul(k, k)), -1.5);
  const t12 = sub(one, s12), t34 = sub(one, s34);
  const t13 = sub(one, s13), t14 = sub(one, s14);
  const t35 = sub(one, s35), t15 = sub(one, s15);

  const f1 = add(add(scale(mul(a, t12), 2),
    scale(add(mul(sub(a, b), t13), mul(add(a, b), t14)), mu)),
    scale(mul(a, t15), nu));
  const f2 = add(scale(mul(h, add(t13, t14)), mu), scale(mul(k, t15), nu));
  const f3 = add(add(add(mul(sub(b, a), t13), mul(add(a, b), t14)),
    scale(mul(b, t34), 2 * mu)), scale(mul(b, t35), nu));
  const f4 = add(scale(mul(k, t15), -2), scale(mul(sub(h, k), t35), 2 * mu));
  return [f1, f2, f3, f4];
}

function equations(x, mu, nu) {
  return symmetricEquationsSeries(x.map(t => constant(t, 0)), mu, nu, 0).map(s => s[0]);
}

function jacobian(x, mu, nu) {
  const J = Array.from({ length: 4 }, () => Array(4).fill(0));
  for (let col = 0; col < 4; col++) {
    const xs = x.map((value, i) => [value, i === col ? 1 : 0]);
    const fs = symmetricEquationsSeries(xs, mu, nu, 1);
    for (let row = 0; row < 4; row++) J[row][col] = fs[row][1];
  }
  return J;
}

function main() {
  const theta = 1.4934310965409843;
  const A = theta ** (-2 / 3), B = (2 - theta) ** (-2 / 3);
  const a = Math.sqrt((A + B - 2) / 2);
  const b = (B - A) / (4 * a);
  const h = Math.sqrt(1 - b * b), k = 0;
  const s12 = 1 / (8 * a ** 3), s34 = 1 / (8 * b ** 3);
  const mu = (1 - theta) * a / ((1 - s34) * b);
  const nu = (-2 * (theta - 1) ** 2 / (s34 - 1) - 2 * (1 - s12)) / (1 - 8 * s12);
  const x = [a, b, h, k];
  const J = jacobian(x, mu, nu);
  const nb = nullBases(J, 1e-8, 1e-10);
  const v = nb.right[0], w = nb.left[0];
  const xs = x.map((value, i) => [value, v[i], 0]);
  const coeff2 = symmetricEquationsSeries(xs, mu, nu, 2).map(s => s[2]);
  const aLS = dot(w, coeff2);
  const s15 = a ** -3, s35 = 1;
  const fNu = [a * (1 - s15), k * (1 - s15), b * (1 - s35), 0];
  const bNu = dot(w, fNu);
  const fMu = [
    (a - b) * (1 - theta) + (a + b) * (theta - 1),
    h * ((1 - theta) + (theta - 1)),
    2 * b * (1 - s34),
    2 * (h - k) * (1 - s35)
  ];
  const bMu = dot(w, fMu);
  const totalMass = 2 + 2 * mu + nu;
  const gamma1 = 2 * mu * h / totalMass, gamma2 = (2 + nu) * h / totalMass;
  const oddJ = finiteJacobian(u => oddEquations(u, { a, b, gamma1, gamma2 }, mu, nu), [0, 0, 0]);
  const oddSV = nullBases(oddJ, 1e-12, 1e-12).singularValues;
  const inverseCubes = [s12, s34, theta, 2 - theta, 1, a ** -3];
  const shapeVWithKOne = v.map(t => t / v[3]);
  const [da, db, dh, dk] = shapeVWithKOne;
  const distanceV = [
    -3 * s12 * da / a,
    -3 * s34 * db / b,
    -1.5 * theta * (2 * (a - b) * (da - db) + 2 * h * dh) / ((a - b) ** 2 + h * h),
    -1.5 * (2 - theta) * (2 * (a + b) * (da + db) + 2 * h * dh) / ((a + b) ** 2 + h * h),
    -1.5 * (2 * b * db + 2 * h * (dh - dk)),
    -3 * (a ** -3) * da / a
  ];
  const yPoly = x.concat(inverseCubes), vPoly = shapeVWithKOne.concat(distanceV);
  const zAug = yPoly.concat([mu, nu], vPoly);
  const HxPoly = finiteJacobian(t => polynomialH(t, mu, nu), yPoly, 1e-6);
  const HxNB = nullBases(HxPoly, 1e-8, 1e-10);
  const rankMinor = HxPoly.filter((_, i) => i !== 4).map(row => row.filter((_, j) => j !== 8));
  const rankMinorSV = nullBases(rankMinor, 1e-12, 1e-12).singularValues;
  const augResidual = augmentedPolynomialSystem(zAug);
  const augJ = finiteJacobian(augmentedPolynomialSystem, zAug, 2e-5);
  const augSV = nullBases(augJ, 1e-13, 1e-13).singularValues;

  console.log(JSON.stringify({
    theta, x: { a, b, h, k }, masses: { mu, nu },
    residual: equations(x, mu, nu), J,
    singularValues: nb.singularValues, rightKernel: v, leftKernel: w,
    tangentResidual: J.map(row => dot(row, v)),
    secondOrderForcing: coeff2, aLS, fNu, bNu, fMu, bMu,
    foldRatioMinusAOverBNu: -aLS / bNu,
    oddBlock: { J: oddJ, singularValues: oddSV },
    polynomialCertificateTarget: {
      y: yPoly, vWithVkOne: vPoly,
      HResidual: polynomialH(yPoly, mu, nu),
      HxSingularValues: HxNB.singularValues,
      HxRightKernel: HxNB.right[0],
      HxLeftKernel: HxNB.left[0],
      rankMinorDeleteRowP35ColE: { singularValues: rankMinorSV },
      augmentedResidualNorm: norm(augResidual),
      augmentedSingularValues: augSV
    },
    norms: { v: norm(v), w: norm(w) }
  }, null, 2));
}

if (require.main === module) main();

module.exports = { symmetricEquationsSeries, equations, jacobian, polynomialH, augmentedPolynomialSystem };

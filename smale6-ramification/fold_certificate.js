"use strict";

// Polynomial Moore--Spence formulation for the Chen--Hsiao five-body fold.
//
// Reflection-symmetric positions, before translating to the center of mass,
// are
//   (-a,0), (a,0), (-b,1), (b,1), (0,c)
// with masses (1,1,mu,mu,nu).  The height of the trapezoid is the scale
// gauge.  Four relative-acceleration equations define central configurations
// in the symmetric fixed-point space.  At the Chen--Hsiao boundary c=0.
//
// Reciprocal distances are independent lifted variables.  Consequently the
// central equations, their physical shape Jacobian, the kernel equations,
// and all distance constraints below are polynomial.

const DIMENSION = 16;

const INDEX = Object.freeze({
  a: 0, b: 1, c: 2, lambda: 3, mu: 4, nu: 5,
  va: 6, vb: 7, vc: 8, vlambda: 9,
  u12: 10, u13: 11, u14: 12, u15: 13, u34: 14, u35: 15
});

const numberOps = {
  constant: x => x,
  add: (x, y) => x + y,
  sub: (x, y) => x - y,
  mul: (x, y) => x * y,
  neg: x => -x
};

function makeAD(value, derivatives) {
  return { value, derivatives };
}

function adConstant(value, ops, n = DIMENSION) {
  return makeAD(ops.constant(value), Array.from({ length: n }, () => ops.constant(0)));
}

function adVariable(value, variableIndex, ops, n = DIMENSION) {
  const derivatives = Array.from({ length: n }, () => ops.constant(0));
  derivatives[variableIndex] = ops.constant(1);
  return makeAD(value, derivatives);
}

function adAdd(x, y, ops) {
  return makeAD(
    ops.add(x.value, y.value),
    x.derivatives.map((d, i) => ops.add(d, y.derivatives[i]))
  );
}

function adSub(x, y, ops) {
  return makeAD(
    ops.sub(x.value, y.value),
    x.derivatives.map((d, i) => ops.sub(d, y.derivatives[i]))
  );
}

function adMul(x, y, ops) {
  return makeAD(
    ops.mul(x.value, y.value),
    x.derivatives.map((d, i) => ops.add(
      ops.mul(d, y.value), ops.mul(x.value, y.derivatives[i])))
  );
}

function adNeg(x, ops) {
  return makeAD(ops.neg(x.value), x.derivatives.map(ops.neg));
}

function adScale(x, scalar, ops) {
  return adMul(x, adConstant(scalar, ops, x.derivatives.length), ops);
}

function adPow(x, exponent, ops) {
  if (!Number.isInteger(exponent) || exponent < 0) throw new Error("nonnegative integer power required");
  let out = adConstant(1, ops, x.derivatives.length);
  let base = x;
  let p = exponent;
  while (p > 0) {
    if (p & 1) out = adMul(out, base, ops);
    p >>= 1;
    if (p) base = adMul(base, base, ops);
  }
  return out;
}

function buildPolynomialSystem(baseValues, ops = numberOps) {
  if (baseValues.length !== DIMENSION) throw new Error(`expected ${DIMENSION} variables`);
  const x = baseValues.map((value, i) => adVariable(value, i, ops));
  const C = value => adConstant(value, ops);
  const add = (u, v) => adAdd(u, v, ops);
  const sub = (u, v) => adSub(u, v, ops);
  const mul = (u, v) => adMul(u, v, ops);
  const neg = u => adNeg(u, ops);
  const scale = (u, s) => adScale(u, s, ops);
  const pow = (u, p) => adPow(u, p, ops);

  const a = x[INDEX.a], b = x[INDEX.b], c = x[INDEX.c];
  const lambda = x[INDEX.lambda], mu = x[INDEX.mu], nu = x[INDEX.nu];
  const kernel = [x[INDEX.va], x[INDEX.vb], x[INDEX.vc], x[INDEX.vlambda]];
  const zero = C(0), one = C(1);
  const positions = [
    [neg(a), zero], [a, zero], [neg(b), one], [b, one], [zero, c]
  ];
  const masses = [one, one, mu, mu, nu];
  const positionDerivatives = Array.from({ length: 5 }, () =>
    Array.from({ length: 2 }, () => Array(4).fill(0)));
  positionDerivatives[0][0][0] = -1;
  positionDerivatives[1][0][0] = 1;
  positionDerivatives[2][0][1] = -1;
  positionDerivatives[3][0][1] = 1;
  positionDerivatives[4][1][2] = 1;

  const reciprocal = new Map([
    ["0,1", x[INDEX.u12]], ["0,2", x[INDEX.u13]],
    ["0,3", x[INDEX.u14]], ["0,4", x[INDEX.u15]],
    ["1,2", x[INDEX.u14]], ["1,3", x[INDEX.u13]],
    ["1,4", x[INDEX.u15]], ["2,3", x[INDEX.u34]],
    ["2,4", x[INDEX.u35]], ["3,4", x[INDEX.u35]]
  ]);
  const rho = (i, j) => reciprocal.get(i < j ? `${i},${j}` : `${j},${i}`);

  const acceleration = Array.from({ length: 5 }, () => [C(0), C(0)]);
  const accelerationJacobian = Array.from({ length: 5 }, () =>
    Array.from({ length: 2 }, () => Array.from({ length: 4 }, () => C(0))));

  for (let i = 0; i < 5; i++) {
    for (let j = 0; j < 5; j++) {
      if (i === j) continue;
      const d = [sub(positions[j][0], positions[i][0]), sub(positions[j][1], positions[i][1])];
      const r = rho(i, j);
      const r3 = pow(r, 3), r5 = pow(r, 5);
      for (let component = 0; component < 2; component++) {
        acceleration[i][component] = add(acceleration[i][component],
          mul(masses[j], mul(d[component], r3)));
      }
      for (let k = 0; k < 4; k++) {
        const e = [
          positionDerivatives[j][0][k] - positionDerivatives[i][0][k],
          positionDerivatives[j][1][k] - positionDerivatives[i][1][k]
        ];
        const radial = add(scale(d[0], e[0]), scale(d[1], e[1]));
        for (let component = 0; component < 2; component++) {
          const derivative = sub(scale(r3, e[component]),
            scale(mul(mul(d[component], r5), radial), 3));
          accelerationJacobian[i][component][k] = add(
            accelerationJacobian[i][component][k], mul(masses[j], derivative));
        }
      }
    }
  }

  const equations = [];
  const physicalJacobian = [];
  for (const body of [0, 2]) {
    for (let component = 0; component < 2; component++) {
      const displacement = sub(positions[body][component], positions[4][component]);
      equations.push(add(sub(acceleration[body][component], acceleration[4][component]),
        mul(lambda, displacement)));
      const row = [];
      for (let k = 0; k < 4; k++) {
        const displacementDerivative = positionDerivatives[body][component][k]
          - positionDerivatives[4][component][k];
        let entry = add(
          sub(accelerationJacobian[body][component][k], accelerationJacobian[4][component][k]),
          scale(lambda, displacementDerivative)
        );
        if (k === 3) entry = add(entry, displacement);
        row.push(entry);
      }
      physicalJacobian.push(row);
    }
  }

  for (let row = 0; row < 4; row++) {
    let value = C(0);
    for (let col = 0; col < 4; col++) value = add(value, mul(physicalJacobian[row][col], kernel[col]));
    equations.push(value);
  }
  equations.push(sub(kernel[2], one));
  equations.push(c);

  const liftedPairs = [
    [0, 1, x[INDEX.u12]], [0, 2, x[INDEX.u13]],
    [0, 3, x[INDEX.u14]], [0, 4, x[INDEX.u15]],
    [2, 3, x[INDEX.u34]], [2, 4, x[INDEX.u35]]
  ];
  for (const [i, j, r] of liftedPairs) {
    const dx = sub(positions[j][0], positions[i][0]);
    const dy = sub(positions[j][1], positions[i][1]);
    equations.push(sub(mul(pow(r, 2), add(pow(dx, 2), pow(dy, 2))), one));
  }
  if (equations.length !== DIMENSION) throw new Error(`constructed ${equations.length} equations`);
  return { equations, physicalJacobian, positions, masses };
}

function evaluateNumber(values) {
  const built = buildPolynomialSystem(values, numberOps);
  return {
    residual: built.equations.map(e => e.value),
    jacobian: built.equations.map(e => e.derivatives),
    physicalJacobian: built.physicalJacobian.map(row => row.map(e => e.value))
  };
}

function solveLinear(aInput, bInput, pivotTolerance = 1e-15) {
  const n = bInput.length;
  const a = aInput.map((row, i) => row.slice().concat([bInput[i]]));
  for (let col = 0; col < n; col++) {
    let pivot = col;
    for (let row = col + 1; row < n; row++) {
      if (Math.abs(a[row][col]) > Math.abs(a[pivot][col])) pivot = row;
    }
    if (Math.abs(a[pivot][col]) < pivotTolerance) throw new Error(`singular Newton matrix at ${col}`);
    [a[col], a[pivot]] = [a[pivot], a[col]];
    const diagonal = a[col][col];
    for (let j = col; j <= n; j++) a[col][j] /= diagonal;
    for (let row = 0; row < n; row++) {
      if (row === col) continue;
      const factor = a[row][col];
      for (let j = col; j <= n; j++) a[row][j] -= factor * a[col][j];
    }
  }
  return a.map(row => row[n]);
}

function normInfinity(vector) {
  return Math.max(...vector.map(Math.abs));
}

function initialGuess() {
  return [
    0.47254694403625785, 0.5632957284873605, 0,
    11.209271113194482, 7.214703144339055, 0.5180857510793098,
    -0.10590957504162582, -0.09607566183130924, 1, 6.201620566499254,
    1.058095933769568, 0.995907588589765, 0.6945499542782082,
    2.116191867539136, 0.8876332177108267, 0.8712791304243579
  ];
}

function newtonSolve(start = initialGuess(), maxIterations = 12) {
  let point = start.slice();
  const history = [];
  for (let iteration = 0; iteration < maxIterations; iteration++) {
    const evaluated = evaluateNumber(point);
    const residualNorm = normInfinity(evaluated.residual);
    history.push({ iteration, residualNorm });
    if (residualNorm < 5e-14) break;
    const correction = solveLinear(evaluated.jacobian, evaluated.residual.map(x => -x));
    point = point.map((x, i) => x + correction[i]);
  }
  const evaluated = evaluateNumber(point);
  return { point, history, ...evaluated, residualNorm: normInfinity(evaluated.residual) };
}

function determinant(matrix) {
  const n = matrix.length;
  if (n === 0) return 1;
  if (n === 1) return matrix[0][0];
  let result = 0;
  for (let j = 0; j < n; j++) {
    const minor = matrix.slice(1).map(row => row.filter((_, k) => k !== j));
    result += (j % 2 ? -1 : 1) * matrix[0][j] * determinant(minor);
  }
  return result;
}

function cofactor(matrix, row, column) {
  const minor = matrix.filter((_, i) => i !== row)
    .map(r => r.filter((_, j) => j !== column));
  return ((row + column) % 2 ? -1 : 1) * determinant(minor);
}

function foldDiagnostics(solution) {
  const values = solution.point;
  const built = buildPolynomialSystem(values, numberOps);
  const j = built.physicalJacobian.map(row => row.map(x => x.value));
  const kernel = values.slice(INDEX.va, INDEX.vlambda + 1);
  let bestColumn = 0, bestNorm = -1, left = null;
  for (let column = 0; column < 4; column++) {
    const candidate = Array.from({ length: 4 }, (_, row) => cofactor(j, row, column));
    const candidateNorm = Math.hypot(...candidate);
    if (candidateNorm > bestNorm) {
      bestNorm = candidateNorm;
      bestColumn = column;
      left = candidate;
    }
  }
  const leftNorm = Math.hypot(...left);
  left = left.map(x => x / leftNorm);

  const q = built.positions.map(position => position.map(x => x.value));
  const masses = built.masses.map(x => x.value);
  const rhos = new Map([
    ["0,1", values[INDEX.u12]], ["0,2", values[INDEX.u13]],
    ["0,3", values[INDEX.u14]], ["0,4", values[INDEX.u15]],
    ["1,2", values[INDEX.u14]], ["1,3", values[INDEX.u13]],
    ["1,4", values[INDEX.u15]], ["2,3", values[INDEX.u34]],
    ["2,4", values[INDEX.u35]], ["3,4", values[INDEX.u35]]
  ]);
  const rho = (i, k) => rhos.get(i < k ? `${i},${k}` : `${k},${i}`);
  const dq = [
    [-kernel[0], 0], [kernel[0], 0], [-kernel[1], 0], [kernel[1], 0], [0, kernel[2]]
  ];
  const accelerationSecond = Array.from({ length: 5 }, () => [0, 0]);
  for (let i = 0; i < 5; i++) {
    for (let body = 0; body < 5; body++) {
      if (i === body) continue;
      const d = [q[body][0] - q[i][0], q[body][1] - q[i][1]];
      const e = [dq[body][0] - dq[i][0], dq[body][1] - dq[i][1]];
      const radial = d[0] * e[0] + d[1] * e[1];
      const speed2 = e[0] ** 2 + e[1] ** 2;
      const r = rho(i, body);
      for (let component = 0; component < 2; component++) {
        accelerationSecond[i][component] += masses[body] * (
          d[component] * (15 * r ** 7 * radial ** 2 - 3 * r ** 5 * speed2)
          - 6 * e[component] * r ** 5 * radial
        );
      }
    }
  }
  const hvv = [];
  for (const body of [0, 2]) {
    for (let component = 0; component < 2; component++) {
      const relativeDirection = dq[body][component] - dq[4][component];
      hvv.push(accelerationSecond[body][component] - accelerationSecond[4][component]
        + 2 * kernel[3] * relativeDirection);
    }
  }
  const gNu = built.equations.slice(0, 4).map(e => e.derivatives[INDEX.nu]);
  const quadratic = 0.5 * left.reduce((sum, x, i) => sum + x * hvv[i], 0);
  const transversalityNu = left.reduce((sum, x, i) => sum + x * gNu[i], 0);
  return {
    physicalJacobian: j,
    determinant: determinant(j),
    bestCofactorColumn: bestColumn,
    cofactorNorm: bestNorm,
    leftKernelUnit: left,
    rightKernelVcOne: kernel,
    leftResidual: j[0].map((_, column) => left.reduce((s, w, row) => s + w * j[row][column], 0)),
    rightResidual: j.map(row => row.reduce((s, entry, column) => s + entry * kernel[column], 0)),
    hessianDirection: hvv,
    quadraticCoefficient: quadratic,
    nuTransversality: transversalityNu
  };
}

function main() {
  const solution = newtonSolve();
  const diagnostics = foldDiagnostics(solution);
  console.log(JSON.stringify({
    residualNorm: solution.residualNorm,
    history: solution.history,
    variables: Object.fromEntries(Object.entries(INDEX).map(([name, index]) => [name, solution.point[index]])),
    diagnostics
  }, null, 2));
}

if (require.main === module) main();

module.exports = {
  DIMENSION,
  INDEX,
  numberOps,
  buildPolynomialSystem,
  evaluateNumber,
  initialGuess,
  newtonSolve,
  foldDiagnostics,
  solveLinear
};

"use strict";

// Certify that the Chen--Hsiao fold has no additional nonsymmetric planar
// kernel.  Everything evaluated on the root box is a polynomial interval
// expression.  In particular no SVD, numerical eigenvalue, square root, or
// numerical determinant is part of the certificate.

const {
  INDEX,
  newtonSolve
} = require("./fold_certificate.js");
const {
  FixedInterval,
  intervalOps
} = require("./fixed_interval.js");
const { findCertificate } = require("./fold_interval_certificate.js");
const { determinant, certifyInvariants } = require("./fold_invariants_certificate.js");

const Z = () => intervalOps.constant(0);
const I = value => intervalOps.constant(value);
const HALF = FixedInterval.point("0.5");

function add2(left, right) {
  return [left[0].add(right[0]), left[1].add(right[1])];
}

function sub2(left, right) {
  return [left[0].sub(right[0]), left[1].sub(right[1])];
}

function scale2(vector, scalar) {
  return [vector[0].mul(scalar), vector[1].mul(scalar)];
}

function dot2(left, right) {
  return left[0].mul(right[0]).add(left[1].mul(right[1]));
}

function power(value, exponent) {
  let result = I(1);
  let base = value;
  let remaining = exponent;
  while (remaining > 0) {
    if (remaining & 1) result = result.mul(base);
    remaining >>= 1;
    if (remaining) base = base.mul(base);
  }
  return result;
}

// D(d |d|^-3)[e] = u^3 e - 3 u^5 d (d.e), where u=|d|^-1.
function pairDerivative(displacement, direction, reciprocalDistance) {
  const u3 = power(reciprocalDistance, 3);
  const u5 = power(reciprocalDistance, 5);
  const radial = dot2(displacement, direction);
  return sub2(scale2(direction, u3),
    scale2(displacement, I(3).mul(u5).mul(radial)));
}

function reciprocalMap(box) {
  return new Map([
    ["0,1", box[INDEX.u12]], ["0,2", box[INDEX.u13]],
    ["0,3", box[INDEX.u14]], ["0,4", box[INDEX.u15]],
    ["1,2", box[INDEX.u14]], ["1,3", box[INDEX.u13]],
    ["1,4", box[INDEX.u15]], ["2,3", box[INDEX.u34]],
    ["2,4", box[INDEX.u35]], ["3,4", box[INDEX.u35]]
  ]);
}

function oddBlock(rootBox) {
  const a = rootBox[INDEX.a];
  const b = rootBox[INDEX.b];
  const c = rootBox[INDEX.c];
  const lambda = rootBox[INDEX.lambda];
  const mu = rootBox[INDEX.mu];
  const nu = rootBox[INDEX.nu];
  const masses = [I(1), I(1), mu, mu, nu];
  const positions = [
    [a.neg(), Z()], [a, Z()],
    [b.neg(), I(1)], [b, I(1)],
    [Z(), c]
  ];
  const reciprocals = reciprocalMap(rootBox);
  const reciprocal = (i, j) => reciprocals.get(i < j ? `${i},${j}` : `${j},${i}`);

  // Full planar slice:
  // q1=(-a,0), q2=(a,0), q3=(s-b,1+y), q4=(s+b,1-y), q5=(x5,c).
  // The three columns below are the odd directions s, y, x5.
  const directions = [
    [[0, 0], [0, 0], [1, 0], [1, 0], [0, 0]],
    [[0, 0], [0, 0], [0, 1], [0, -1], [0, 0]],
    [[0, 0], [0, 0], [0, 0], [0, 0], [1, 0]]
  ].map(column => column.map(vector => vector.map(I)));

  return Array.from({ length: 3 }, (_, output) =>
    Array.from({ length: 3 }, (_, column) => {
      const dq = directions[column];
      const dAcceleration = Array.from({ length: 5 }, () => [Z(), Z()]);
      for (let body = 0; body < 5; body++) {
        for (let other = 0; other < 5; other++) {
          if (body === other) continue;
          const displacement = sub2(positions[other], positions[body]);
          const direction = sub2(dq[other], dq[body]);
          const term = pairDerivative(displacement, direction, reciprocal(body, other));
          dAcceleration[body] = add2(dAcceleration[body], scale2(term, masses[other]));
        }
      }
      const dE = Array.from({ length: 4 }, (_, body) =>
        add2(sub2(dAcceleration[body], dAcceleration[4]),
          scale2(sub2(dq[body], dq[4]), lambda)));
      if (output === 0) return dE[0][0].add(dE[1][0]).mul(HALF);
      if (output === 1) return dE[0][1].sub(dE[1][1]).mul(HALF);
      return dE[2][0].add(dE[3][0]).mul(HALF);
    }));
}

function certifyFullPlanar(rootBox) {
  const symmetric = certifyInvariants(rootBox);
  const odd = oddBlock(rootBox);
  const oddDeterminant = determinant(odd);
  return {
    oddBlock: odd,
    oddDeterminant,
    oddDeterminantExcludesZero: !oddDeterminant.containsZero(),
    symmetricRankMinor: symmetric.rankMinor,
    symmetricRankMinorExcludesZero: symmetric.rankMinorExcludesZero,
    fullCorankOne: symmetric.rankMinorExcludesZero && !oddDeterminant.containsZero()
  };
}

function serialize(result) {
  return {
    oddBlock: result.oddBlock.map(row => row.map(value => value.toDecimal(16))),
    oddDeterminant: result.oddDeterminant.toDecimal(16),
    oddDeterminantExcludesZero: result.oddDeterminantExcludesZero,
    symmetricRankMinor: result.symmetricRankMinor.toDecimal(16),
    symmetricRankMinorExcludesZero: result.symmetricRankMinorExcludesZero,
    fullCorankOne: result.fullCorankOne
  };
}

function main() {
  const root = findCertificate(newtonSolve());
  if (!root.attempt) throw new Error("no certified root box");
  const result = certifyFullPlanar(root.attempt.box);
  console.log(JSON.stringify(serialize(result), null, 2));
  if (!result.fullCorankOne) process.exitCode = 1;
}

if (require.main === module) main();

module.exports = { pairDerivative, oddBlock, certifyFullPlanar };

"use strict";

// Validates the geometric nondegeneracy data on the Krawczyk root box:
//   * the 4x4 physical shape Jacobian has rank exactly three;
//   * the Lyapunov--Schmidt quadratic projection is nonzero;
//   * varying nu at fixed mu is transverse to the discriminant.
// Cofactors are deliberately left unnormalised, avoiding interval square
// roots and divisions.  Their scale is irrelevant to all nonzero tests.

const {
  INDEX,
  buildPolynomialSystem,
  newtonSolve
} = require("./fold_certificate.js");
const {
  FixedInterval,
  intervalOps
} = require("./fixed_interval.js");
const { findCertificate } = require("./fold_interval_certificate.js");

const zero = () => intervalOps.constant(0);
const integer = value => intervalOps.constant(value);

function sum(terms) {
  return terms.reduce((accumulator, term) => accumulator.add(term), zero());
}

function power(value, exponent) {
  if (!Number.isInteger(exponent) || exponent < 0) throw new Error("invalid exponent");
  let result = integer(1);
  let base = value;
  let remaining = exponent;
  while (remaining > 0) {
    if (remaining & 1) result = result.mul(base);
    remaining >>= 1;
    if (remaining) base = base.mul(base);
  }
  return result;
}

function determinant(matrix) {
  const n = matrix.length;
  if (n === 0) return integer(1);
  if (n === 1) return matrix[0][0];
  let result = zero();
  for (let column = 0; column < n; column++) {
    const minor = matrix.slice(1).map(row => row.filter((_, j) => j !== column));
    const term = matrix[0][column].mul(determinant(minor));
    result = column % 2 ? result.sub(term) : result.add(term);
  }
  return result;
}

function cofactor(matrix, row, column) {
  const minor = matrix.filter((_, i) => i !== row)
    .map(entries => entries.filter((_, j) => j !== column));
  const value = determinant(minor);
  return (row + column) % 2 ? value.neg() : value;
}

function dot(left, right) {
  return sum(left.map((value, i) => value.mul(right[i])));
}

function intervalHessianDirection(box, built) {
  const q = built.positions.map(position => position.map(coordinate => coordinate.value));
  const masses = built.masses.map(mass => mass.value);
  const kernel = box.slice(INDEX.va, INDEX.vlambda + 1);
  const rhos = new Map([
    ["0,1", box[INDEX.u12]], ["0,2", box[INDEX.u13]],
    ["0,3", box[INDEX.u14]], ["0,4", box[INDEX.u15]],
    ["1,2", box[INDEX.u14]], ["1,3", box[INDEX.u13]],
    ["1,4", box[INDEX.u15]], ["2,3", box[INDEX.u34]],
    ["2,4", box[INDEX.u35]], ["3,4", box[INDEX.u35]]
  ]);
  const rho = (i, j) => rhos.get(i < j ? `${i},${j}` : `${j},${i}`);
  const dq = [
    [kernel[0].neg(), zero()], [kernel[0], zero()],
    [kernel[1].neg(), zero()], [kernel[1], zero()],
    [zero(), kernel[2]]
  ];
  const accelerationSecond = Array.from({ length: 5 }, () => [zero(), zero()]);

  for (let i = 0; i < 5; i++) {
    for (let body = 0; body < 5; body++) {
      if (i === body) continue;
      const displacement = [q[body][0].sub(q[i][0]), q[body][1].sub(q[i][1])];
      const direction = [dq[body][0].sub(dq[i][0]), dq[body][1].sub(dq[i][1])];
      const radial = dot(displacement, direction);
      const speedSquared = dot(direction, direction);
      const rho5 = power(rho(i, body), 5);
      const rho7 = power(rho(i, body), 7);
      for (let component = 0; component < 2; component++) {
        const radialPart = integer(15).mul(rho7).mul(radial).mul(radial)
          .sub(integer(3).mul(rho5).mul(speedSquared));
        const term = displacement[component].mul(radialPart)
          .sub(integer(6).mul(direction[component]).mul(rho5).mul(radial));
        accelerationSecond[i][component] = accelerationSecond[i][component]
          .add(masses[body].mul(term));
      }
    }
  }

  const result = [];
  for (const body of [0, 2]) {
    for (let component = 0; component < 2; component++) {
      const relativeDirection = dq[body][component].sub(dq[4][component]);
      result.push(accelerationSecond[body][component]
        .sub(accelerationSecond[4][component])
        .add(integer(2).mul(kernel[3]).mul(relativeDirection)));
    }
  }
  return result;
}

function certifyInvariants(rootBox) {
  const built = buildPolynomialSystem(rootBox, intervalOps);
  const physicalJacobian = built.physicalJacobian.map(row => row.map(entry => entry.value));

  // Numerically the fourth cofactor column is largest and its second entry
  // is farthest from zero.  The exact interval test below is what matters.
  const cofactorColumn = 3;
  const leftCofactor = Array.from({ length: 4 }, (_, row) =>
    cofactor(physicalJacobian, row, cofactorColumn));
  const rankMinor = leftCofactor[1];

  const hessianDirection = intervalHessianDirection(rootBox, built);
  const nuDerivative = built.equations.slice(0, 4)
    .map(equation => equation.derivatives[INDEX.nu]);
  const projectedSecondDerivative = dot(leftCofactor, hessianDirection);
  const quadraticCoefficient = FixedInterval.point("0.5").mul(projectedSecondDerivative);
  const nuTransversality = dot(leftCofactor, nuDerivative);
  const foldCurvatureMagnitude = quadraticCoefficient.div(nuTransversality);

  const positiveIndices = [
    INDEX.a, INDEX.b, INDEX.mu, INDEX.nu,
    INDEX.u12, INDEX.u13, INDEX.u14, INDEX.u15, INDEX.u34, INDEX.u35
  ];
  const positivity = Object.fromEntries(positiveIndices.map(index => [index, rootBox[index].lo > 0n]));
  return {
    physicalJacobian,
    cofactorColumn,
    leftCofactor,
    rankMinor,
    hessianDirection,
    nuDerivative,
    projectedSecondDerivative,
    quadraticCoefficient,
    nuTransversality,
    foldCurvatureMagnitude,
    rankMinorExcludesZero: !rankMinor.containsZero(),
    quadraticExcludesZero: !quadraticCoefficient.containsZero(),
    transversalityExcludesZero: !nuTransversality.containsZero(),
    positivity,
    allRequiredPositive: Object.values(positivity).every(Boolean)
  };
}

function serialize(result) {
  return {
    cofactorColumn: result.cofactorColumn,
    leftCofactor: result.leftCofactor.map(value => value.toDecimal(16)),
    rankMinor: result.rankMinor.toDecimal(16),
    rankMinorExcludesZero: result.rankMinorExcludesZero,
    hessianDirection: result.hessianDirection.map(value => value.toDecimal(16)),
    projectedSecondDerivative: result.projectedSecondDerivative.toDecimal(16),
    quadraticCoefficient: result.quadraticCoefficient.toDecimal(16),
    quadraticExcludesZero: result.quadraticExcludesZero,
    nuDerivative: result.nuDerivative.map(value => value.toDecimal(16)),
    nuTransversality: result.nuTransversality.toDecimal(16),
    transversalityExcludesZero: result.transversalityExcludesZero,
    foldExpansion: `nu(c)=nu_* - ${result.foldCurvatureMagnitude.toDecimal(16)} c^2 + O(c^3)`,
    positivity: result.positivity,
    allRequiredPositive: result.allRequiredPositive
  };
}

function main() {
  const solution = newtonSolve();
  const certificate = findCertificate(solution);
  if (!certificate.attempt) throw new Error("no Krawczyk root box available");
  // A verified zero belongs to its Krawczyk image, which is much tighter
  // than the original trial box and is therefore used below.
  const invariants = certifyInvariants(certificate.attempt.image);
  const success = invariants.rankMinorExcludesZero
    && invariants.quadraticExcludesZero
    && invariants.transversalityExcludesZero
    && invariants.allRequiredPositive;
  console.log(JSON.stringify({ success, ...serialize(invariants) }, null, 2));
  if (!success) process.exitCode = 1;
}

if (require.main === module) main();

module.exports = {
  determinant,
  cofactor,
  intervalHessianDirection,
  certifyInvariants
};

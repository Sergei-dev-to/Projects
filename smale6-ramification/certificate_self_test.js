"use strict";

const assert = require("assert");
const {
  SCALE,
  FixedInterval,
  floorDiv,
  ceilDiv
} = require("./fixed_interval.js");
const { newtonSolve } = require("./fold_certificate.js");
const { findCertificate } = require("./fold_interval_certificate.js");
const { certifyInvariants } = require("./fold_invariants_certificate.js");
const { certifyFullPlanarCorank } = require("./full_planar_certificate.js");
const { oddBlock: independentOddBlock } = require("./fold_full_planar_certificate.js");
const {
  jetHessianDirection,
  overlap
} = require("./fold_hessian_crosscheck.js");

// Exhaustively exercise signed floor/ceiling behavior over small integers.
for (let numerator = -100n; numerator <= 100n; numerator++) {
  for (let denominator = 1n; denominator <= 31n; denominator++) {
    const lower = floorDiv(numerator, denominator);
    const upper = ceilDiv(numerator, denominator);
    assert(lower * denominator <= numerator);
    assert(numerator < (lower + 1n) * denominator);
    assert((upper - 1n) * denominator < numerator);
    assert(numerator <= upper * denominator);
  }
}

// Exact endpoint checks, including negative multiplication and reciprocals.
assert.strictEqual(
  FixedInterval.bounds("-0.1", "0.2")
    .mul(FixedInterval.bounds("-3", "4")).toDecimal(4),
  "[-0.6000, 0.8000]"
);
assert.strictEqual(
  FixedInterval.bounds("2", "4").reciprocal().toDecimal(4),
  "[0.2500, 0.5000]"
);
assert.strictEqual(
  FixedInterval.bounds("-4", "-2").reciprocal().toDecimal(4),
  "[-0.5000, -0.2500]"
);
assert.throws(() => FixedInterval.bounds("-1", "1").reciprocal());

// End-to-end exact certificate decisions.
const solution = newtonSolve();
const certificate = findCertificate(solution);
assert(certificate.attempt, "Krawczyk inclusion failed");
assert(certificate.attempt.allStrictlyIncluded);
assert(certificate.attempt.contractionCertified);
assert(certificate.attempt.contractionNormUpperGrid < SCALE);

const rootEnclosure = certificate.attempt.image;
const invariants = certifyInvariants(rootEnclosure);
assert(invariants.rankMinorExcludesZero);
assert(invariants.quadraticExcludesZero);
assert(invariants.transversalityExcludesZero);
assert(!invariants.foldCurvatureMagnitude.containsZero());
assert(invariants.foldCurvatureMagnitude.lo > 0n);
assert(invariants.allRequiredPositive);

const full = certifyFullPlanarCorank(rootEnclosure);
assert(full.evenMinorExcludesZero);
assert(full.oddDeterminantExcludesZero);
assert(full.fullMinorExcludesZero);
const secondOdd = independentOddBlock(rootEnclosure);
assert(full.odd.every((row, i) => row.every((entry, j) => overlap(entry, secondOdd[i][j]))));

// Independently recompute the second directional derivative by Taylor jets.
const jetHessian = jetHessianDirection(rootEnclosure);
assert(invariants.hessianDirection.every((entry, i) => overlap(entry, jetHessian[i])));
const jetProjection = invariants.leftCofactor.reduce((accumulator, entry, i) =>
  accumulator.add(entry.mul(jetHessian[i])), FixedInterval.point("0"));
assert(!jetProjection.containsZero());
assert(overlap(invariants.projectedSecondDerivative, jetProjection));

console.log("all exact fold-certificate checks passed");

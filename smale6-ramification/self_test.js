"use strict";

const assert = require("assert");
const {
  robertsCalibration,
  triangleCenterCalibration,
  chenHsiaoDegeneracy
} = require("./jet_sieve");

const roberts = robertsCalibration();
assert(roberts.baseResidualNorm < 1e-12);
assert.strictEqual(roberts.nullity, 1);
assert.strictEqual(roberts.stoppedAt, null);
assert(Math.max(...roberts.orders.map(x => x.obstructionNorm)) < 1e-11);

const triangle = triangleCenterCalibration();
assert(triangle.baseResidualNorm < 1e-12);
assert.strictEqual(triangle.nullity, 2);
assert(triangle.minimumOrder2Obstruction > 0.4);

const chenHsiao = chenHsiaoDegeneracy();
assert(Math.abs(chenHsiao.nu - 0.51808575107931) < 1e-12);
assert(chenHsiao.sieve.baseResidualNorm < 1e-11);
assert.strictEqual(chenHsiao.sieve.nullity, 1);
assert(chenHsiao.sieve.singularValues[1] > 0.2);
assert.strictEqual(chenHsiao.sieve.stoppedAt, 2);
assert(chenHsiao.sieve.orders[1].obstructionNorm > 0.1);
assert(Math.abs(chenHsiao.collinearityDerivative) > 3);
assert(chenHsiao.permutationChecks.every(x => x.order2Obstruction > 0.1));

console.log("all fixed-mass jet-sieve checks passed");

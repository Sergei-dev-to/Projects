"use strict";

// Independent second-order jet calculation of D_x^2 G[v,v].  Unlike the
// closed derivative formula in fold_invariants_certificate.js, this route
// propagates truncated Taylor series and derives the reciprocal-distance
// series from u^2 |d|^2=1.  Agreement provides a useful guard against a
// hand-coded Hessian error.

const {
  INDEX,
  buildPolynomialSystem,
  newtonSolve
} = require("./fold_certificate.js");
const { FixedInterval, intervalOps } = require("./fixed_interval.js");
const { findCertificate } = require("./fold_interval_certificate.js");
const {
  cofactor,
  intervalHessianDirection,
  determinant
} = require("./fold_invariants_certificate.js");

const C = value => intervalOps.constant(value);
const point = value => FixedInterval.point(value);
const jet = (c0, c1 = C(0), c2 = C(0)) => [c0, c1, c2];
const add = (left, right) => left.map((entry, i) => entry.add(right[i]));
const sub = (left, right) => left.map((entry, i) => entry.sub(right[i]));
const mul = (left, right) => [
  left[0].mul(right[0]),
  left[0].mul(right[1]).add(left[1].mul(right[0])),
  left[0].mul(right[2]).add(left[1].mul(right[1])).add(left[2].mul(right[0]))
];
const scale = (value, scalar) => value.map(entry => entry.mul(scalar));

function addMany(values) {
  return values.reduce(add, jet(C(0)));
}

function reciprocalDistanceJet(displacementJets, baseReciprocal) {
  const squaredDistance = addMany(displacementJets.map(component => mul(component, component)));
  const reciprocalSquared = baseReciprocal.mul(baseReciprocal);
  const z1 = reciprocalSquared.mul(squaredDistance[1]);
  const z2 = reciprocalSquared.mul(squaredDistance[2]);
  const rho1 = baseReciprocal.mul(point("-0.5")).mul(z1);
  const rho2 = baseReciprocal.mul(
    point("-0.5").mul(z2).add(point("0.375").mul(z1).mul(z1))
  );
  return jet(baseReciprocal, rho1, rho2);
}

function jetHessianDirection(rootBox) {
  const built = buildPolynomialSystem(rootBox, intervalOps);
  const q = built.positions.map(position => position.map(coordinate => coordinate.value));
  const masses = built.masses.map(mass => mass.value);
  const kernel = rootBox.slice(INDEX.va, INDEX.vlambda + 1);
  const dq = [
    [kernel[0].neg(), C(0)], [kernel[0], C(0)],
    [kernel[1].neg(), C(0)], [kernel[1], C(0)],
    [C(0), kernel[2]]
  ];
  const rhos = new Map([
    ["0,1", rootBox[INDEX.u12]], ["0,2", rootBox[INDEX.u13]],
    ["0,3", rootBox[INDEX.u14]], ["0,4", rootBox[INDEX.u15]],
    ["1,2", rootBox[INDEX.u14]], ["1,3", rootBox[INDEX.u13]],
    ["1,4", rootBox[INDEX.u15]], ["2,3", rootBox[INDEX.u34]],
    ["2,4", rootBox[INDEX.u35]], ["3,4", rootBox[INDEX.u35]]
  ]);
  const rho = (i, j) => rhos.get(i < j ? `${i},${j}` : `${j},${i}`);
  const acceleration = Array.from({ length: 5 }, () => [jet(C(0)), jet(C(0))]);

  for (let i = 0; i < 5; i++) {
    for (let body = 0; body < 5; body++) {
      if (i === body) continue;
      const displacement = [0, 1].map(component => jet(
        q[body][component].sub(q[i][component]),
        dq[body][component].sub(dq[i][component])
      ));
      const rhoJet = reciprocalDistanceJet(displacement, rho(i, body));
      const rhoCubed = mul(mul(rhoJet, rhoJet), rhoJet);
      for (let component = 0; component < 2; component++) {
        acceleration[i][component] = add(acceleration[i][component],
          scale(mul(displacement[component], rhoCubed), masses[body]));
      }
    }
  }

  const lambdaJet = jet(rootBox[INDEX.lambda], kernel[3]);
  const equations = [];
  for (const body of [0, 2]) {
    for (let component = 0; component < 2; component++) {
      const relativePosition = jet(
        q[body][component].sub(q[4][component]),
        dq[body][component].sub(dq[4][component])
      );
      equations.push(add(
        sub(acceleration[body][component], acceleration[4][component]),
        mul(lambdaJet, relativePosition)
      ));
    }
  }
  return equations.map(equation => equation[2].mul(C(2)));
}

function overlap(left, right) {
  return left.lo <= right.hi && right.lo <= left.hi;
}

function main() {
  const solution = newtonSolve();
  const certificate = findCertificate(solution);
  if (!certificate.attempt) throw new Error("no Krawczyk root box available");
  const box = certificate.attempt.image;
  const built = buildPolynomialSystem(box, intervalOps);
  const physical = built.physicalJacobian.map(row => row.map(entry => entry.value));
  const left = Array.from({ length: 4 }, (_, row) => cofactor(physical, row, 3));
  const closed = intervalHessianDirection(box, built);
  const jets = jetHessianDirection(box);
  const closedProjection = left.reduce((sum, entry, i) =>
    sum.add(entry.mul(closed[i])), C(0));
  const jetProjection = left.reduce((sum, entry, i) =>
    sum.add(entry.mul(jets[i])), C(0));
  const componentOverlap = closed.map((entry, i) => overlap(entry, jets[i]));
  const success = componentOverlap.every(Boolean)
    && overlap(closedProjection, jetProjection)
    && !jetProjection.containsZero();
  console.log(JSON.stringify({
    success,
    closedFormula: closed.map(value => value.toDecimal(16)),
    independentJets: jets.map(value => value.toDecimal(16)),
    componentOverlap,
    closedProjection: closedProjection.toDecimal(16),
    independentJetProjection: jetProjection.toDecimal(16),
    projectionsOverlap: overlap(closedProjection, jetProjection),
    independentProjectionExcludesZero: !jetProjection.containsZero()
  }, null, 2));
  if (!success) process.exitCode = 1;
}

if (require.main === module) main();

module.exports = { reciprocalDistanceJet, jetHessianDirection, overlap };

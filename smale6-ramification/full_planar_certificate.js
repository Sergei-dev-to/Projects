"use strict";

// Full-planar corank certificate at the reflection-symmetric Chen--Hsiao
// root.  The local shape slice is
//   q1=(-a,0), q2=(a,0),
//   q3=(s-b,1+y), q4=(s+b,1-y), q5=(x5,c).
// The even coordinates are (a,b,c,lambda); the odd coordinates are
// (s,y,x5).  Reflection equivariance makes the Jacobian block diagonal at
// s=y=x5=0.  This file validates the 3x3 odd block and multiplies its
// determinant by a certified nonzero 3x3 minor of the even block.

const {
  INDEX,
  buildPolynomialSystem,
  newtonSolve
} = require("./fold_certificate.js");
const { intervalOps } = require("./fixed_interval.js");
const { findCertificate } = require("./fold_interval_certificate.js");
const { determinant, cofactor } = require("./fold_invariants_certificate.js");

const C = value => intervalOps.constant(value);

function power(value, exponent) {
  let result = C(1);
  let base = value;
  let remaining = exponent;
  while (remaining > 0) {
    if (remaining & 1) result = result.mul(base);
    remaining >>= 1;
    if (remaining) base = base.mul(base);
  }
  return result;
}

function oddBlock(rootBox) {
  const built = buildPolynomialSystem(rootBox, intervalOps);
  const positions = built.positions.map(position => position.map(entry => entry.value));
  const masses = built.masses.map(entry => entry.value);
  const lambda = rootBox[INDEX.lambda];
  const rhos = new Map([
    ["0,1", rootBox[INDEX.u12]], ["0,2", rootBox[INDEX.u13]],
    ["0,3", rootBox[INDEX.u14]], ["0,4", rootBox[INDEX.u15]],
    ["1,2", rootBox[INDEX.u14]], ["1,3", rootBox[INDEX.u13]],
    ["1,4", rootBox[INDEX.u15]], ["2,3", rootBox[INDEX.u34]],
    ["2,4", rootBox[INDEX.u35]], ["3,4", rootBox[INDEX.u35]]
  ]);
  const rho = (i, j) => rhos.get(i < j ? `${i},${j}` : `${j},${i}`);

  // Derivatives of positions with respect to (s,y,x5).
  const dq = Array.from({ length: 5 }, () =>
    Array.from({ length: 2 }, () => [0, 0, 0]));
  dq[2][0][0] = 1;
  dq[3][0][0] = 1;
  dq[2][1][1] = 1;
  dq[3][1][1] = -1;
  dq[4][0][2] = 1;

  const accelerationDerivative = Array.from({ length: 5 }, () =>
    Array.from({ length: 2 }, () => Array.from({ length: 3 }, () => C(0))));
  for (let i = 0; i < 5; i++) {
    for (let j = 0; j < 5; j++) {
      if (i === j) continue;
      const displacement = [
        positions[j][0].sub(positions[i][0]),
        positions[j][1].sub(positions[i][1])
      ];
      const rho3 = power(rho(i, j), 3);
      const rho5 = power(rho(i, j), 5);
      for (let variable = 0; variable < 3; variable++) {
        const direction = [
          dq[j][0][variable] - dq[i][0][variable],
          dq[j][1][variable] - dq[i][1][variable]
        ];
        const radial = displacement[0].mul(C(direction[0]))
          .add(displacement[1].mul(C(direction[1])));
        for (let component = 0; component < 2; component++) {
          const derivative = rho3.mul(C(direction[component]))
            .sub(C(3).mul(displacement[component]).mul(rho5).mul(radial));
          accelerationDerivative[i][component][variable] =
            accelerationDerivative[i][component][variable]
              .add(masses[j].mul(derivative));
        }
      }
    }
  }

  // E_i=A_i-A_5+lambda(q_i-q_5), for i=0,...,3.
  const eDerivative = Array.from({ length: 4 }, (_, i) =>
    Array.from({ length: 2 }, (_, component) =>
      Array.from({ length: 3 }, (_, variable) =>
        accelerationDerivative[i][component][variable]
          .sub(accelerationDerivative[4][component][variable])
          .add(lambda.mul(C(dq[i][component][variable] - dq[4][component][variable]))))));
  const half = require("./fixed_interval.js").FixedInterval.point("0.5");
  const combine = (i, component, j, sign) =>
    eDerivative[i][component].map((entry, variable) =>
      entry.add(sign === 1
        ? eDerivative[j][component][variable]
        : eDerivative[j][component][variable].neg()).mul(half));

  return [
    combine(0, 0, 1, 1),  // O1=(E1x+E2x)/2
    combine(0, 1, 1, -1), // O2=(E1y-E2y)/2
    combine(2, 0, 3, 1)   // O3=(E3x+E4x)/2
  ];
}

function certifyFullPlanarCorank(rootBox) {
  const built = buildPolynomialSystem(rootBox, intervalOps);
  const even = built.physicalJacobian.map(row => row.map(entry => entry.value));
  const evenMinor = cofactor(even, 1, 3);
  const odd = oddBlock(rootBox);
  const oddDeterminant = determinant(odd);
  const fullMinor = evenMinor.mul(oddDeterminant);
  return {
    evenMinor,
    odd,
    oddDeterminant,
    fullMinor,
    evenMinorExcludesZero: !evenMinor.containsZero(),
    oddDeterminantExcludesZero: !oddDeterminant.containsZero(),
    fullMinorExcludesZero: !fullMinor.containsZero()
  };
}

function main() {
  const solution = newtonSolve();
  const certificate = findCertificate(solution);
  if (!certificate.attempt) throw new Error("no Krawczyk root box available");
  const result = certifyFullPlanarCorank(certificate.attempt.image);
  const success = result.evenMinorExcludesZero
    && result.oddDeterminantExcludesZero
    && result.fullMinorExcludesZero;
  console.log(JSON.stringify({
    success,
    evenMinor: result.evenMinor.toDecimal(16),
    evenMinorExcludesZero: result.evenMinorExcludesZero,
    oddBlock: result.odd.map(row => row.map(entry => entry.toDecimal(12))),
    oddDeterminant: result.oddDeterminant.toDecimal(16),
    oddDeterminantExcludesZero: result.oddDeterminantExcludesZero,
    fullSixBySixMinor: result.fullMinor.toDecimal(16),
    fullMinorExcludesZero: result.fullMinorExcludesZero
  }, null, 2));
  if (!success) process.exitCode = 1;
}

if (require.main === module) main();

module.exports = { oddBlock, certifyFullPlanarCorank };

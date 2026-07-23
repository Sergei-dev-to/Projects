"use strict";

// Exact fixed-grid Krawczyk verifier for fold_certificate.js.  All decisions
// are made by BigInt comparisons.  Floating point is used only to choose an
// approximate inverse (the Krawczyk preconditioner may be any fixed matrix)
// and to print human-readable diagnostics.

const {
  DIMENSION,
  buildPolynomialSystem,
  evaluateNumber,
  newtonSolve,
  solveLinear
} = require("./fold_certificate.js");
const {
  PRECISION,
  SCALE,
  FixedInterval,
  intervalOps
} = require("./fixed_interval.js");

function pointFromNumber(value) {
  if (!Number.isFinite(value)) throw new Error(`nonfinite value ${value}`);
  return FixedInterval.point(value.toPrecision(17));
}

function numericInverse(matrix) {
  const n = matrix.length;
  const inverse = Array.from({ length: n }, () => Array(n).fill(0));
  for (let column = 0; column < n; column++) {
    const rhs = Array(n).fill(0);
    rhs[column] = 1;
    const solution = solveLinear(matrix, rhs, 1e-18);
    for (let row = 0; row < n; row++) inverse[row][column] = solution[row];
  }
  return inverse;
}

function intervalDot(left, right) {
  let sum = intervalOps.constant(0);
  for (let i = 0; i < left.length; i++) {
    sum = sum.add(left[i].mul(right[i]));
  }
  return sum;
}

function matrixVector(matrix, vector) {
  return matrix.map(row => intervalDot(row, vector));
}

function matrixMatrix(left, right) {
  const rows = left.length;
  const inner = right.length;
  const columns = right[0].length;
  return Array.from({ length: rows }, (_, i) =>
    Array.from({ length: columns }, (_, j) => {
      let sum = intervalOps.constant(0);
      for (let k = 0; k < inner; k++) sum = sum.add(left[i][k].mul(right[k][j]));
      return sum;
    }));
}

function identityMinus(matrix) {
  return matrix.map((row, i) => row.map((entry, j) =>
    intervalOps.constant(i === j ? 1 : 0).sub(entry)));
}

function intervalMatrixInfinityNormUpperGrid(matrix) {
  let maximum = 0n;
  for (const row of matrix) {
    let rowSum = 0n;
    for (const entry of row) {
      const lowerMagnitude = entry.lo < 0n ? -entry.lo : entry.lo;
      const upperMagnitude = entry.hi < 0n ? -entry.hi : entry.hi;
      rowSum += lowerMagnitude > upperMagnitude ? lowerMagnitude : upperMagnitude;
    }
    if (rowSum > maximum) maximum = rowSum;
  }
  return maximum;
}

function krawczykAtRadius(solution, radiusText) {
  const centerStrings = solution.point.map(value => value.toPrecision(17));
  const center = centerStrings.map(FixedInterval.point);
  const box = centerStrings.map(value => FixedInterval.around(value, radiusText));

  const centerEvaluation = buildPolynomialSystem(center, intervalOps);
  const boxEvaluation = buildPolynomialSystem(box, intervalOps);
  const fCenter = centerEvaluation.equations.map(equation => equation.value);
  const derivativeBox = boxEvaluation.equations.map(equation => equation.derivatives);

  const approximateInverse = numericInverse(evaluateNumber(solution.point).jacobian);
  const preconditioner = approximateInverse.map(row => row.map(pointFromNumber));
  const correction = matrixVector(preconditioner, fCenter);
  const constantTerm = center.map((entry, i) => entry.sub(correction[i]));
  const defect = identityMinus(matrixMatrix(preconditioner, derivativeBox));
  const contractionNormUpperGrid = intervalMatrixInfinityNormUpperGrid(defect);
  const contractionCertified = contractionNormUpperGrid < SCALE;
  const centeredBox = box.map((entry, i) => entry.sub(center[i]));
  const variableTerm = matrixVector(defect, centeredBox);
  const image = constantTerm.map((entry, i) => entry.add(variableTerm[i]));
  const included = image.map((entry, i) => entry.isStrictlyInside(box[i]));

  const approximateWidthRatios = image.map((entry, i) =>
    Number(entry.widthGridUnits()) / Number(box[i].widthGridUnits()));
  return {
    radiusText,
    centerStrings,
    center,
    box,
    image,
    included,
    allStrictlyIncluded: included.every(Boolean),
    contractionCertified,
    contractionNormUpperGrid,
    approximateContractionNormUpper: Number(contractionNormUpperGrid) / Number(SCALE),
    approximateWidthRatios,
    maximumApproximateWidthRatio: Math.max(...approximateWidthRatios),
    fCenter
  };
}

function findCertificate(solution, radii = ["1e-8", "1e-9", "1e-10", "1e-11", "1e-12"]) {
  const attempts = [];
  for (const radius of radii) {
    const attempt = krawczykAtRadius(solution, radius);
    attempts.push(attempt);
    if (attempt.allStrictlyIncluded && attempt.contractionCertified) return { attempt, attempts };
  }
  return { attempt: null, attempts };
}

function serializeAttempt(attempt, includeBoxes = false) {
  const result = {
    radius: attempt.radiusText,
    allStrictlyIncluded: attempt.allStrictlyIncluded,
    contractionCertified: attempt.contractionCertified,
    approximateContractionNormUpper: attempt.approximateContractionNormUpper,
    includedCoordinates: attempt.included,
    maximumApproximateWidthRatio: attempt.maximumApproximateWidthRatio,
    approximateWidthRatios: attempt.approximateWidthRatios
  };
  if (includeBoxes) {
    result.box = attempt.box.map(interval => interval.toDecimal(24));
    result.krawczykImage = attempt.image.map(interval => interval.toDecimal(24));
    result.centerResidualIntervals = attempt.fCenter.map(interval => interval.toDecimal(12));
  }
  return result;
}

function main() {
  const solution = newtonSolve();
  const result = findCertificate(solution);
  console.log(JSON.stringify({
    arithmetic: `BigInt fixed decimal, ${PRECISION} digits after the point`,
    numericalResidualInfinityNorm: solution.residualNorm,
    attempts: result.attempts.map(attempt => serializeAttempt(attempt)),
    certificate: result.attempt ? serializeAttempt(result.attempt, true) : null
  }, null, 2));
  if (!result.attempt) process.exitCode = 1;
}

if (require.main === module) main();

module.exports = {
  pointFromNumber,
  numericInverse,
  intervalDot,
  matrixVector,
  matrixMatrix,
  identityMinus,
  intervalMatrixInfinityNormUpperGrid,
  krawczykAtRadius,
  findCertificate
};

"use strict";

// A deliberately small, auditable interval-arithmetic kernel for polynomial
// certificates.  Endpoints are signed BigInts representing multiples of
// 10^-PRECISION.  Every multiplication rounds outwards using exact integer
// floor/ceiling division.  Addition and subtraction are exact on the grid.

const PRECISION = Number(process.env.CERT_INTERVAL_PRECISION || 90);
if (!Number.isInteger(PRECISION) || PRECISION < 30 || PRECISION > 500) {
  throw new Error(`invalid CERT_INTERVAL_PRECISION=${process.env.CERT_INTERVAL_PRECISION}`);
}
const SCALE = 10n ** BigInt(PRECISION);

function floorDiv(numerator, denominator) {
  if (denominator <= 0n) throw new Error("floorDiv requires a positive denominator");
  let quotient = numerator / denominator;
  const remainder = numerator % denominator;
  if (remainder !== 0n && numerator < 0n) quotient -= 1n;
  return quotient;
}

function ceilDiv(numerator, denominator) {
  if (denominator <= 0n) throw new Error("ceilDiv requires a positive denominator");
  let quotient = numerator / denominator;
  const remainder = numerator % denominator;
  if (remainder !== 0n && numerator > 0n) quotient += 1n;
  return quotient;
}

function floorRatio(numerator, denominator) {
  if (denominator === 0n) throw new Error("zero denominator");
  return denominator > 0n
    ? floorDiv(numerator, denominator)
    : floorDiv(-numerator, -denominator);
}

function ceilRatio(numerator, denominator) {
  if (denominator === 0n) throw new Error("zero denominator");
  return denominator > 0n
    ? ceilDiv(numerator, denominator)
    : ceilDiv(-numerator, -denominator);
}

function parseDecimalEndpoint(input, roundDown) {
  let text = String(input).trim().toLowerCase();
  if (!text) throw new Error("empty decimal");
  let sign = 1n;
  if (text[0] === "+") text = text.slice(1);
  else if (text[0] === "-") {
    sign = -1n;
    text = text.slice(1);
  }
  const pieces = text.split("e");
  if (pieces.length > 2) throw new Error(`invalid decimal ${input}`);
  const exponent = pieces.length === 2 ? Number(pieces[1]) : 0;
  if (!Number.isInteger(exponent)) throw new Error(`invalid exponent in ${input}`);
  const mantissa = pieces[0].split(".");
  if (mantissa.length > 2) throw new Error(`invalid decimal ${input}`);
  const whole = mantissa[0] || "0";
  const fraction = mantissa[1] || "";
  if (!/^\d+$/.test(whole) || (fraction && !/^\d+$/.test(fraction))) {
    throw new Error(`invalid decimal ${input}`);
  }
  const digits = BigInt((whole + fraction).replace(/^0+(?=\d)/, "") || "0") * sign;
  const gridExponent = PRECISION + exponent - fraction.length;
  if (gridExponent >= 0) return digits * (10n ** BigInt(gridExponent));
  const denominator = 10n ** BigInt(-gridExponent);
  return roundDown ? floorDiv(digits, denominator) : ceilDiv(digits, denominator);
}

class FixedInterval {
  constructor(lo, hi) {
    if (typeof lo !== "bigint" || typeof hi !== "bigint") {
      throw new Error("interval endpoints must be BigInts");
    }
    if (lo > hi) throw new Error("reversed interval");
    this.lo = lo;
    this.hi = hi;
    Object.freeze(this);
  }

  static point(input) {
    const lo = parseDecimalEndpoint(input, true);
    const hi = parseDecimalEndpoint(input, false);
    if (lo !== hi) throw new Error(`${input} is not exactly representable on the decimal grid`);
    return new FixedInterval(lo, hi);
  }

  static encloseDecimal(input) {
    return new FixedInterval(
      parseDecimalEndpoint(input, true),
      parseDecimalEndpoint(input, false)
    );
  }

  static bounds(lo, hi) {
    return new FixedInterval(
      parseDecimalEndpoint(lo, true),
      parseDecimalEndpoint(hi, false)
    );
  }

  static around(center, radius) {
    const c = FixedInterval.point(center);
    const r = FixedInterval.point(radius);
    if (r.lo < 0n) throw new Error("negative radius");
    return new FixedInterval(c.lo - r.lo, c.hi + r.hi);
  }

  add(other) {
    return new FixedInterval(this.lo + other.lo, this.hi + other.hi);
  }

  sub(other) {
    return new FixedInterval(this.lo - other.hi, this.hi - other.lo);
  }

  neg() {
    return new FixedInterval(-this.hi, -this.lo);
  }

  mul(other) {
    const products = [
      this.lo * other.lo,
      this.lo * other.hi,
      this.hi * other.lo,
      this.hi * other.hi
    ];
    let minimum = products[0], maximum = products[0];
    for (const product of products.slice(1)) {
      if (product < minimum) minimum = product;
      if (product > maximum) maximum = product;
    }
    return new FixedInterval(
      floorDiv(minimum, SCALE),
      ceilDiv(maximum, SCALE)
    );
  }

  reciprocal() {
    if (this.lo <= 0n && this.hi >= 0n) throw new Error("division by an interval containing zero");
    // Encoding 1/(x/S) on the same grid gives S^2/x.
    const numerator = SCALE * SCALE;
    return new FixedInterval(
      floorRatio(numerator, this.hi),
      ceilRatio(numerator, this.lo)
    );
  }

  div(other) {
    return this.mul(other.reciprocal());
  }

  containsZero() {
    return this.lo <= 0n && this.hi >= 0n;
  }

  isStrictlyInside(other) {
    return other.lo < this.lo && this.hi < other.hi;
  }

  widthGridUnits() {
    return this.hi - this.lo;
  }

  midpointNumber() {
    return (Number(this.lo) + Number(this.hi)) / (2 * Number(SCALE));
  }

  toDecimal(digits = 20) {
    if (!Number.isInteger(digits) || digits < 0 || digits > PRECISION) {
      throw new Error(`requested ${digits} digits at precision ${PRECISION}`);
    }
    const divisor = 10n ** BigInt(PRECISION - digits);
    const displayedLo = floorDiv(this.lo, divisor);
    const displayedHi = ceilDiv(this.hi, divisor);
    const render = endpoint => {
      const negative = endpoint < 0n;
      let raw = (negative ? -endpoint : endpoint).toString().padStart(digits + 1, "0");
      const whole = digits ? (raw.slice(0, -digits) || "0") : raw;
      const fraction = digits ? raw.slice(-digits).padStart(digits, "0") : "";
      return `${negative ? "-" : ""}${whole}${digits ? `.${fraction}` : ""}`;
    };
    return `[${render(displayedLo)}, ${render(displayedHi)}]`;
  }
}

const intervalOps = Object.freeze({
  constant: value => {
    if (!Number.isInteger(value)) throw new Error(`noninteger polynomial constant ${value}`);
    return new FixedInterval(BigInt(value) * SCALE, BigInt(value) * SCALE);
  },
  add: (x, y) => x.add(y),
  sub: (x, y) => x.sub(y),
  mul: (x, y) => x.mul(y),
  neg: x => x.neg()
});

module.exports = {
  PRECISION,
  SCALE,
  FixedInterval,
  intervalOps,
  floorDiv,
  ceilDiv,
  floorRatio,
  ceilRatio
};

"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getPartialAmountCeil = exports.getPartialAmountFloor = exports.safeGetPartialAmountCeil = exports.safeGetPartialAmountFloor = exports.isRoundingErrorCeil = exports.isRoundingErrorFloor = exports.safeDiv = exports.safeMul = exports.safeSub = exports.safeAdd = void 0;
const utils_1 = require("@0x/utils");
const MAX_UINT256 = new utils_1.BigNumber(2).pow(256).minus(1);
/**
 * Add two `uint256` values. Reverts on overflow.
 */
function safeAdd(a, b) {
    const r = a.plus(b);
    if (r.isGreaterThan(MAX_UINT256)) {
        throw new utils_1.SafeMathRevertErrors.Uint256BinOpError(utils_1.SafeMathRevertErrors.BinOpErrorCodes.AdditionOverflow, a, b);
    }
    return r;
}
exports.safeAdd = safeAdd;
/**
 * Subract two `uint256` values. Reverts on overflow.
 */
function safeSub(a, b) {
    const r = a.minus(b);
    if (r.isLessThan(0)) {
        throw new utils_1.SafeMathRevertErrors.Uint256BinOpError(utils_1.SafeMathRevertErrors.BinOpErrorCodes.SubtractionUnderflow, a, b);
    }
    return r;
}
exports.safeSub = safeSub;
/**
 * Multiplies two `uint256` values. Reverts on overflow.
 */
function safeMul(a, b) {
    const r = a.times(b);
    if (r.isGreaterThan(MAX_UINT256)) {
        throw new utils_1.SafeMathRevertErrors.Uint256BinOpError(utils_1.SafeMathRevertErrors.BinOpErrorCodes.MultiplicationOverflow, a, b);
    }
    return r;
}
exports.safeMul = safeMul;
/**
 * Divides two `uint256` values. Reverts on division by zero.
 */
function safeDiv(a, b) {
    if (b.isEqualTo(0)) {
        throw new utils_1.SafeMathRevertErrors.Uint256BinOpError(utils_1.SafeMathRevertErrors.BinOpErrorCodes.DivisionByZero, a, b);
    }
    return a.dividedToIntegerBy(b);
}
exports.safeDiv = safeDiv;
// LibMath
/**
 * Checks if rounding error >= 0.1% when rounding down.
 */
function isRoundingErrorFloor(numerator, denominator, target) {
    if (denominator.eq(0)) {
        throw new utils_1.LibMathRevertErrors.DivisionByZeroError();
    }
    if (numerator.eq(0) || target.eq(0)) {
        return false;
    }
    const remainder = numerator.times(target).mod(denominator);
    // Need to do this separately because solidity evaluates RHS of the comparison expression first.
    const rhs = safeMul(numerator, target);
    const lhs = safeMul(remainder, new utils_1.BigNumber(1000));
    return lhs.gte(rhs);
}
exports.isRoundingErrorFloor = isRoundingErrorFloor;
/**
 * Checks if rounding error >= 0.1% when rounding up.
 */
function isRoundingErrorCeil(numerator, denominator, target) {
    if (denominator.eq(0)) {
        throw new utils_1.LibMathRevertErrors.DivisionByZeroError();
    }
    if (numerator.eq(0) || target.eq(0)) {
        return false;
    }
    let remainder = numerator.times(target).mod(denominator);
    remainder = safeSub(denominator, remainder).mod(denominator);
    // Need to do this separately because solidity evaluates RHS of the comparison expression first.
    const rhs = safeMul(numerator, target);
    const lhs = safeMul(remainder, new utils_1.BigNumber(1000));
    return lhs.gte(rhs);
}
exports.isRoundingErrorCeil = isRoundingErrorCeil;
/**
 * Calculates partial value given a numerator and denominator rounded down.
 *      Reverts if rounding error is >= 0.1%
 */
function safeGetPartialAmountFloor(numerator, denominator, target) {
    if (isRoundingErrorFloor(numerator, denominator, target)) {
        throw new utils_1.LibMathRevertErrors.RoundingError(numerator, denominator, target);
    }
    return safeDiv(safeMul(numerator, target), denominator);
}
exports.safeGetPartialAmountFloor = safeGetPartialAmountFloor;
/**
 * Calculates partial value given a numerator and denominator rounded down.
 *      Reverts if rounding error is >= 0.1%
 */
function safeGetPartialAmountCeil(numerator, denominator, target) {
    if (isRoundingErrorCeil(numerator, denominator, target)) {
        throw new utils_1.LibMathRevertErrors.RoundingError(numerator, denominator, target);
    }
    return safeDiv(safeAdd(safeMul(numerator, target), safeSub(denominator, new utils_1.BigNumber(1))), denominator);
}
exports.safeGetPartialAmountCeil = safeGetPartialAmountCeil;
/**
 * Calculates partial value given a numerator and denominator rounded down.
 */
function getPartialAmountFloor(numerator, denominator, target) {
    return safeDiv(safeMul(numerator, target), denominator);
}
exports.getPartialAmountFloor = getPartialAmountFloor;
/**
 * Calculates partial value given a numerator and denominator rounded down.
 */
function getPartialAmountCeil(numerator, denominator, target) {
    const sub = safeSub(denominator, new utils_1.BigNumber(1)); // This is computed first to simulate Solidity's order of operations
    return safeDiv(safeAdd(safeMul(numerator, target), sub), denominator);
}
exports.getPartialAmountCeil = getPartialAmountCeil;
//# sourceMappingURL=reference_functions.js.map
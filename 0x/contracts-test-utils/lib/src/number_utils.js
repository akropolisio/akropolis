"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getPercentageOfValue = exports.toBaseUnitAmount = exports.assertIntegerRoughlyEquals = exports.assertRoughlyEquals = exports.getNumericalDivergence = exports.fromFixed = exports.toFixed = exports.FIXED_POINT_BASE = exports.getRandomFloat = exports.getRandomPortion = exports.getRandomInteger = exports.toDecimal = void 0;
const utils_1 = require("@0x/utils");
const web3_wrapper_1 = require("@0x/web3-wrapper");
const crypto = require("crypto");
const decimal_js_1 = require("decimal.js");
const chai_setup_1 = require("./chai_setup");
const constants_1 = require("./constants");
decimal_js_1.Decimal.set({ precision: 80 });
/**
 * Convert `x` to a `Decimal` type.
 */
function toDecimal(x) {
    if (utils_1.BigNumber.isBigNumber(x)) {
        return new decimal_js_1.Decimal(x.toString(10));
    }
    return new decimal_js_1.Decimal(x);
}
exports.toDecimal = toDecimal;
/**
 * Generate a random integer between `min` and `max`, inclusive.
 */
function getRandomInteger(min, max) {
    const range = new utils_1.BigNumber(max).minus(min);
    return getRandomPortion(range).plus(min);
}
exports.getRandomInteger = getRandomInteger;
/**
 * Generate a random integer between `0` and `total`, inclusive.
 */
function getRandomPortion(total) {
    return new utils_1.BigNumber(total).times(getRandomFloat(0, 1)).integerValue(utils_1.BigNumber.ROUND_HALF_UP);
}
exports.getRandomPortion = getRandomPortion;
/**
 * Generate a random, high-precision decimal between `min` and `max`, inclusive.
 */
function getRandomFloat(min, max) {
    // Generate a really high precision number between [0, 1]
    const r = new utils_1.BigNumber(crypto.randomBytes(32).toString('hex'), 16).dividedBy(new utils_1.BigNumber(2).pow(256).minus(1));
    return new utils_1.BigNumber(max)
        .minus(min)
        .times(r)
        .plus(min);
}
exports.getRandomFloat = getRandomFloat;
exports.FIXED_POINT_BASE = new utils_1.BigNumber(2).pow(127);
/**
 * Convert `n` to fixed-point integer represenatation.
 */
function toFixed(n) {
    return new utils_1.BigNumber(n).times(exports.FIXED_POINT_BASE).integerValue();
}
exports.toFixed = toFixed;
/**
 * Convert `n` from fixed-point integer represenatation.
 */
function fromFixed(n) {
    return new utils_1.BigNumber(n).dividedBy(exports.FIXED_POINT_BASE);
}
exports.fromFixed = fromFixed;
/**
 * Converts two decimal numbers to integers with `precision` digits, then returns
 * the absolute difference.
 */
function getNumericalDivergence(a, b, precision = 18) {
    const _a = new utils_1.BigNumber(a);
    const _b = new utils_1.BigNumber(b);
    const maxIntegerDigits = Math.max(_a.integerValue(utils_1.BigNumber.ROUND_DOWN).sd(true), _b.integerValue(utils_1.BigNumber.ROUND_DOWN).sd(true));
    const _toInteger = (n) => {
        const base = Math.pow(10, (precision - maxIntegerDigits));
        return n.times(base).integerValue(utils_1.BigNumber.ROUND_DOWN);
    };
    return _toInteger(_a)
        .minus(_toInteger(_b))
        .abs()
        .toNumber();
}
exports.getNumericalDivergence = getNumericalDivergence;
/**
 * Asserts that two numbers are equal up to `precision` digits.
 */
function assertRoughlyEquals(actual, expected, precision = 18) {
    if (getNumericalDivergence(actual, expected, precision) <= 1) {
        return;
    }
    chai_setup_1.expect(actual).to.bignumber.eq(expected);
}
exports.assertRoughlyEquals = assertRoughlyEquals;
/**
 * Asserts that two numbers are equal with up to `maxError` difference between them.
 */
function assertIntegerRoughlyEquals(actual, expected, maxError = 1, msg) {
    const diff = new utils_1.BigNumber(actual)
        .minus(expected)
        .abs()
        .toNumber();
    if (diff <= maxError) {
        return;
    }
    chai_setup_1.expect(actual, msg).to.bignumber.eq(expected);
}
exports.assertIntegerRoughlyEquals = assertIntegerRoughlyEquals;
/**
 * Converts `amount` into a base unit amount with 18 digits.
 */
function toBaseUnitAmount(amount, decimals) {
    const baseDecimals = decimals !== undefined ? decimals : 18;
    const amountAsBigNumber = new utils_1.BigNumber(amount);
    const baseUnitAmount = web3_wrapper_1.Web3Wrapper.toBaseUnitAmount(amountAsBigNumber, baseDecimals);
    return baseUnitAmount;
}
exports.toBaseUnitAmount = toBaseUnitAmount;
/**
 * Computes a percentage of `value`, first converting `percentage` to be expressed in 18 digits.
 */
function getPercentageOfValue(value, percentage) {
    const numerator = constants_1.constants.PERCENTAGE_DENOMINATOR.times(percentage).dividedToIntegerBy(100);
    const newValue = numerator.times(value).dividedToIntegerBy(constants_1.constants.PERCENTAGE_DENOMINATOR);
    return newValue;
}
exports.getPercentageOfValue = getPercentageOfValue;
//# sourceMappingURL=number_utils.js.map
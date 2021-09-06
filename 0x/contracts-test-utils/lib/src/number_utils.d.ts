import { BigNumber } from '@0x/utils';
import { Decimal } from 'decimal.js';
import { Numberish } from './types';
/**
 * Convert `x` to a `Decimal` type.
 */
export declare function toDecimal(x: Numberish): Decimal;
/**
 * Generate a random integer between `min` and `max`, inclusive.
 */
export declare function getRandomInteger(min: Numberish, max: Numberish): BigNumber;
/**
 * Generate a random integer between `0` and `total`, inclusive.
 */
export declare function getRandomPortion(total: Numberish): BigNumber;
/**
 * Generate a random, high-precision decimal between `min` and `max`, inclusive.
 */
export declare function getRandomFloat(min: Numberish, max: Numberish): BigNumber;
export declare const FIXED_POINT_BASE: BigNumber;
/**
 * Convert `n` to fixed-point integer represenatation.
 */
export declare function toFixed(n: Numberish): BigNumber;
/**
 * Convert `n` from fixed-point integer represenatation.
 */
export declare function fromFixed(n: Numberish): BigNumber;
/**
 * Converts two decimal numbers to integers with `precision` digits, then returns
 * the absolute difference.
 */
export declare function getNumericalDivergence(a: Numberish, b: Numberish, precision?: number): number;
/**
 * Asserts that two numbers are equal up to `precision` digits.
 */
export declare function assertRoughlyEquals(actual: Numberish, expected: Numberish, precision?: number): void;
/**
 * Asserts that two numbers are equal with up to `maxError` difference between them.
 */
export declare function assertIntegerRoughlyEquals(actual: Numberish, expected: Numberish, maxError?: number, msg?: string): void;
/**
 * Converts `amount` into a base unit amount with 18 digits.
 */
export declare function toBaseUnitAmount(amount: Numberish, decimals?: number): BigNumber;
/**
 * Computes a percentage of `value`, first converting `percentage` to be expressed in 18 digits.
 */
export declare function getPercentageOfValue(value: Numberish, percentage: Numberish): BigNumber;
//# sourceMappingURL=number_utils.d.ts.map
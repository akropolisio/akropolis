import { BigNumber } from '@0x/utils';
/**
 * Add two `uint256` values. Reverts on overflow.
 */
export declare function safeAdd(a: BigNumber, b: BigNumber): BigNumber;
/**
 * Subract two `uint256` values. Reverts on overflow.
 */
export declare function safeSub(a: BigNumber, b: BigNumber): BigNumber;
/**
 * Multiplies two `uint256` values. Reverts on overflow.
 */
export declare function safeMul(a: BigNumber, b: BigNumber): BigNumber;
/**
 * Divides two `uint256` values. Reverts on division by zero.
 */
export declare function safeDiv(a: BigNumber, b: BigNumber): BigNumber;
/**
 * Checks if rounding error >= 0.1% when rounding down.
 */
export declare function isRoundingErrorFloor(numerator: BigNumber, denominator: BigNumber, target: BigNumber): boolean;
/**
 * Checks if rounding error >= 0.1% when rounding up.
 */
export declare function isRoundingErrorCeil(numerator: BigNumber, denominator: BigNumber, target: BigNumber): boolean;
/**
 * Calculates partial value given a numerator and denominator rounded down.
 *      Reverts if rounding error is >= 0.1%
 */
export declare function safeGetPartialAmountFloor(numerator: BigNumber, denominator: BigNumber, target: BigNumber): BigNumber;
/**
 * Calculates partial value given a numerator and denominator rounded down.
 *      Reverts if rounding error is >= 0.1%
 */
export declare function safeGetPartialAmountCeil(numerator: BigNumber, denominator: BigNumber, target: BigNumber): BigNumber;
/**
 * Calculates partial value given a numerator and denominator rounded down.
 */
export declare function getPartialAmountFloor(numerator: BigNumber, denominator: BigNumber, target: BigNumber): BigNumber;
/**
 * Calculates partial value given a numerator and denominator rounded down.
 */
export declare function getPartialAmountCeil(numerator: BigNumber, denominator: BigNumber, target: BigNumber): BigNumber;
//# sourceMappingURL=reference_functions.d.ts.map
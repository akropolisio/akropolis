"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.testCombinatoriallyWithReferenceFunc = exports.bytes32Values = exports.uint256Values = void 0;
const utils_1 = require("@0x/utils");
const combinatorics = require("js-combinatorics");
const test_with_reference_1 = require("./test_with_reference");
// A set of values corresponding to the uint256 type in Solidity. This set
// contains some notable edge cases, including some values which will overflow
// the uint256 type when used in different mathematical operations.
exports.uint256Values = [
    new utils_1.BigNumber(0),
    new utils_1.BigNumber(1),
    new utils_1.BigNumber(2),
    // Non-trivial big number.
    new utils_1.BigNumber(2).pow(64),
    // Max that does not overflow when squared.
    new utils_1.BigNumber(2).pow(128).minus(1),
    // Min that does overflow when squared.
    new utils_1.BigNumber(2).pow(128),
    // Max that does not overflow when doubled.
    new utils_1.BigNumber(2).pow(255).minus(1),
    // Min that does overflow when doubled.
    new utils_1.BigNumber(2).pow(255),
    // Max that does not overflow.
    new utils_1.BigNumber(2).pow(256).minus(1),
];
// A set of values corresponding to the bytes32 type in Solidity.
exports.bytes32Values = [
    // Min
    '0x0000000000000000000000000000000000000000000000000000000000000000',
    '0x0000000000000000000000000000000000000000000000000000000000000001',
    '0x0000000000000000000000000000000000000000000000000000000000000002',
    // Non-trivial big number.
    '0x000000000000f000000000000000000000000000000000000000000000000000',
    // Max
    '0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff',
];
/**
 * Uses combinatorics to test the behavior of a test function by comparing it to
 * the expected behavior (defined by a reference function) for a large number of
 * possible input values.
 *
 * First generates test cases by taking the cartesian product of the given
 * values. Each test case is a set of N values corresponding to the N arguments
 * for the test func and the reference func. For each test case, first the
 * reference function will be called to obtain an "expected result", or if the
 * reference function throws/rejects, an "expected error". Next, the test
 * function will be called to obtain an "actual result", or if the test function
 * throws/rejects, an "actual error". Each test case passes if at least one of
 * the following conditions is met:
 *
 * 1) Neither the reference function or the test function throw and the
 * "expected result" equals the "actual result".
 *
 * 2) Both the reference function and the test function throw and the "actual
 * error" message *contains* the "expected error" message.
 *
 * The first test case which does not meet one of these conditions will cause
 * the entire test to fail and this function will throw/reject.
 *
 * @param referenceFuncAsync a reference function implemented in pure
 * JavaScript/TypeScript which accepts N arguments and returns the "expected
 * result" or "expected error" for a given test case.
 * @param testFuncAsync a test function which, e.g., makes a call or sends a
 * transaction to a contract. It accepts the same N arguments returns the
 * "actual result" or "actual error" for a given test case.
 * @param values an array of N arrays. Each inner array is a set of possible
 * values which are passed into both the reference function and the test
 * function.
 * @return A Promise that resolves if the test passes and rejects if the test
 * fails, according to the rules described above.
 */
function testCombinatoriallyWithReferenceFunc(name, referenceFuncAsync, testFuncAsync, allValues) {
    const testCases = combinatorics.cartesianProduct(...allValues);
    let counter = 0;
    testCases.forEach((testCase) => __awaiter(this, void 0, void 0, function* () {
        counter += 1;
        it(`${name} ${counter}/${testCases.length}`, () => __awaiter(this, void 0, void 0, function* () {
            yield test_with_reference_1.testWithReferenceFuncAsync(referenceFuncAsync, testFuncAsync, testCase);
        }));
    }));
}
exports.testCombinatoriallyWithReferenceFunc = testCombinatoriallyWithReferenceFunc;
//# sourceMappingURL=combinatorial_utils.js.map
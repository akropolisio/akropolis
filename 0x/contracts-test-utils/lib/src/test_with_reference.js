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
exports.testWithReferenceFuncAsync = void 0;
const utils_1 = require("@0x/utils");
const _ = require("lodash");
const chai_setup_1 = require("./chai_setup");
/**
 * Tests the behavior of a test function by comparing it to the expected
 * behavior (defined by a reference function).
 *
 * First the reference function will be called to obtain an "expected result",
 * or if the reference function throws/rejects, an "expected error". Next, the
 * test function will be called to obtain an "actual result", or if the test
 * function throws/rejects, an "actual error". The test passes if at least one
 * of the following conditions is met:
 *
 * 1) Neither the reference function or the test function throw and the
 * "expected result" equals the "actual result".
 *
 * 2) Both the reference function and the test function throw and the "actual
 * error" message *contains* the "expected error" message.
 *
 * @param referenceFuncAsync a reference function implemented in pure
 * JavaScript/TypeScript which accepts N arguments and returns the "expected
 * result" or throws/rejects with the "expected error".
 * @param testFuncAsync a test function which, e.g., makes a call or sends a
 * transaction to a contract. It accepts the same N arguments returns the
 * "actual result" or throws/rejects with the "actual error".
 * @param values an array of N values, where each value corresponds in-order to
 * an argument to both the test function and the reference function.
 * @return A Promise that resolves if the test passes and rejects if the test
 * fails, according to the rules described above.
 */
function testWithReferenceFuncAsync(referenceFuncAsync, testFuncAsync, values) {
    return __awaiter(this, void 0, void 0, function* () {
        // Measure correct behavior
        let expected;
        let expectedError;
        try {
            expected = yield referenceFuncAsync(...values);
        }
        catch (err) {
            expectedError = err;
        }
        // Measure actual behavior
        let actual;
        let actualError;
        try {
            actual = yield testFuncAsync(...values);
        }
        catch (err) {
            actualError = err;
        }
        const testCaseString = _getTestCaseString(referenceFuncAsync, values);
        // Compare behavior
        if (expectedError !== undefined) {
            // Expecting an error.
            if (actualError === undefined) {
                return chai_setup_1.expect.fail(actualError, expectedError, `${testCaseString}: expected failure but instead succeeded`);
            }
            else {
                if (expectedError instanceof utils_1.RevertError) {
                    // Expecting a RevertError.
                    if (actualError instanceof utils_1.RevertError) {
                        if (!actualError.equals(expectedError)) {
                            return chai_setup_1.expect.fail(actualError, expectedError, `${testCaseString}: expected error ${actualError.toString()} to equal ${expectedError.toString()}`);
                        }
                    }
                    else {
                        return chai_setup_1.expect.fail(actualError, expectedError, `${testCaseString}: expected a RevertError but received an Error`);
                    }
                }
                else {
                    // Expecing any Error type.
                    if (actualError.message !== expectedError.message) {
                        return chai_setup_1.expect.fail(actualError, expectedError, `${testCaseString}: expected error message '${actualError.message}' to equal '${expectedError.message}'`);
                    }
                }
            }
        }
        else {
            // Not expecting an error.
            if (actualError !== undefined) {
                return chai_setup_1.expect.fail(actualError, expectedError, `${testCaseString}: expected success but instead failed`);
            }
            if (expected instanceof utils_1.BigNumber) {
                // Technically we can do this with `deep.eq`, but this prints prettier
                // error messages for BigNumbers.
                chai_setup_1.expect(actual).to.bignumber.eq(expected, testCaseString);
            }
            else {
                chai_setup_1.expect(actual).to.deep.eq(expected, testCaseString);
            }
        }
    });
}
exports.testWithReferenceFuncAsync = testWithReferenceFuncAsync;
function _getTestCaseString(referenceFuncAsync, values) {
    const paramNames = _getParameterNames(referenceFuncAsync);
    while (paramNames.length < values.length) {
        paramNames.push(`${paramNames.length}`);
    }
    return JSON.stringify(_.zipObject(paramNames, values));
}
// Source: https://stackoverflow.com/questions/1007981/how-to-get-function-parameter-names-values-dynamically
function _getParameterNames(func) {
    return _.toString(func)
        .replace(/[/][/].*$/gm, '') // strip single-line comments
        .replace(/\s+/g, '') // strip white space
        .replace(/[/][*][^/*]*[*][/]/g, '') // strip multi-line comments
        .split(/\){|\)=>/, 1)[0]
        .replace(/^[^(]*[(]/, '') // extract the parameters
        .replace(/=[^,]+/g, '') // strip any ES6 defaults
        .split(',')
        .filter(Boolean); // split & filter [""]
}
//# sourceMappingURL=test_with_reference.js.map
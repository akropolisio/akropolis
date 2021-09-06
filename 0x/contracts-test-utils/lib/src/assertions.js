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
exports.expectContractCreationFailedWithoutReasonAsync = exports.expectContractCreationFailedAsync = exports.expectContractCallFailedWithoutReasonAsync = exports.expectContractCallFailedAsync = exports.expectTransactionFailedWithoutReasonAsync = exports.expectTransactionFailedAsync = exports.expectInsufficientFundsAsync = exports.getRevertReasonOrErrorMessageForSendTransactionAsync = exports.getInvalidOpcodeErrorMessageForCallAsync = void 0;
const utils_1 = require("@0x/utils");
const web3_wrapper_1 = require("@0x/web3-wrapper");
const chai = require("chai");
const _ = require("lodash");
const web3_wrapper_2 = require("./web3_wrapper");
const expect = chai.expect;
let nodeType;
/**
 * Returns ganacheError if the backing Ethereum node is Ganache and gethError
 * if it is Geth.
 * @param ganacheError the error to be returned if the backing node is Ganache.
 * @param gethError the error to be returned if the backing node is Geth.
 * @returns either the given ganacheError or gethError depending on the backing
 * node.
 */
function _getGanacheOrGethErrorAsync(ganacheError, gethError) {
    return __awaiter(this, void 0, void 0, function* () {
        if (nodeType === undefined) {
            nodeType = yield web3_wrapper_2.web3Wrapper.getNodeTypeAsync();
        }
        switch (nodeType) {
            case web3_wrapper_1.NodeType.Ganache:
                return ganacheError;
            case web3_wrapper_1.NodeType.Geth:
                return gethError;
            default:
                throw new Error(`Unknown node type: ${nodeType}`);
        }
    });
}
function _getInsufficientFundsErrorMessageAsync() {
    return __awaiter(this, void 0, void 0, function* () {
        return _getGanacheOrGethErrorAsync("sender doesn't have enough funds", 'insufficient funds');
    });
}
function _getTransactionFailedErrorMessageAsync() {
    return __awaiter(this, void 0, void 0, function* () {
        return _getGanacheOrGethErrorAsync('revert', 'always failing transaction');
    });
}
function _getContractCallFailedErrorMessageAsync() {
    return __awaiter(this, void 0, void 0, function* () {
        return _getGanacheOrGethErrorAsync('revert', 'Contract call failed');
    });
}
/**
 * Returns the expected error message for an 'invalid opcode' resulting from a
 * contract call. The exact error message depends on the backing Ethereum node.
 */
function getInvalidOpcodeErrorMessageForCallAsync() {
    return __awaiter(this, void 0, void 0, function* () {
        return _getGanacheOrGethErrorAsync('invalid opcode', 'Contract call failed');
    });
}
exports.getInvalidOpcodeErrorMessageForCallAsync = getInvalidOpcodeErrorMessageForCallAsync;
/**
 * Returns the expected error message for the given revert reason resulting from
 * a sendTransaction call. The exact error message depends on the backing
 * Ethereum node and whether it supports revert reasons.
 * @param reason a specific revert reason.
 * @returns the expected error message.
 */
function getRevertReasonOrErrorMessageForSendTransactionAsync(reason) {
    return __awaiter(this, void 0, void 0, function* () {
        return _getGanacheOrGethErrorAsync(reason, 'always failing transaction');
    });
}
exports.getRevertReasonOrErrorMessageForSendTransactionAsync = getRevertReasonOrErrorMessageForSendTransactionAsync;
/**
 * Rejects if the given Promise does not reject with an error indicating
 * insufficient funds.
 * @param p a promise resulting from a contract call or sendTransaction call.
 * @returns a new Promise which will reject if the conditions are not met and
 * otherwise resolve with no value.
 */
function expectInsufficientFundsAsync(p) {
    return __awaiter(this, void 0, void 0, function* () {
        const errMessage = yield _getInsufficientFundsErrorMessageAsync();
        return expect(p).to.be.rejectedWith(errMessage);
    });
}
exports.expectInsufficientFundsAsync = expectInsufficientFundsAsync;
/**
 * Resolves if the the sendTransaction call fails with the given revert reason.
 * However, since Geth does not support revert reasons for sendTransaction, this
 * falls back to expectTransactionFailedWithoutReasonAsync if the backing
 * Ethereum node is Geth.
 * @param p a Promise resulting from a sendTransaction call
 * @param reason a specific revert reason
 * @returns a new Promise which will reject if the conditions are not met and
 * otherwise resolve with no value.
 */
function expectTransactionFailedAsync(p, reason) {
    return __awaiter(this, void 0, void 0, function* () {
        // HACK(albrow): This dummy `catch` should not be necessary, but if you
        // remove it, there is an uncaught exception and the Node process will
        // forcibly exit. It's possible this is a false positive in
        // make-promises-safe.
        p.catch(e => {
            _.noop(e);
        });
        if (nodeType === undefined) {
            nodeType = yield web3_wrapper_2.web3Wrapper.getNodeTypeAsync();
        }
        switch (nodeType) {
            case web3_wrapper_1.NodeType.Ganache:
                const rejectionMessageRegex = new RegExp(`^VM Exception while processing transaction: revert ${reason}$`);
                return expect(p).to.be.rejectedWith(rejectionMessageRegex);
            case web3_wrapper_1.NodeType.Geth:
                utils_1.logUtils.warn('WARNING: Geth does not support revert reasons for sendTransaction. This test will pass if the transaction fails for any reason.');
                return expectTransactionFailedWithoutReasonAsync(p);
            default:
                throw new Error(`Unknown node type: ${nodeType}`);
        }
    });
}
exports.expectTransactionFailedAsync = expectTransactionFailedAsync;
/**
 * Resolves if the transaction fails without a revert reason, or if the
 * corresponding transactionReceipt has a status of 0 or '0', indicating
 * failure.
 * @param p a Promise resulting from a sendTransaction call
 * @returns a new Promise which will reject if the conditions are not met and
 * otherwise resolve with no value.
 */
function expectTransactionFailedWithoutReasonAsync(p) {
    return __awaiter(this, void 0, void 0, function* () {
        return p
            .then((result) => __awaiter(this, void 0, void 0, function* () {
            let txReceiptStatus;
            if (_.isString(result)) {
                // Result is a txHash. We need to make a web3 call to get the
                // receipt, then get the status from the receipt.
                const txReceipt = yield web3_wrapper_2.web3Wrapper.awaitTransactionMinedAsync(result);
                txReceiptStatus = txReceipt.status;
            }
            else if ('status' in result) {
                // Result is a transaction receipt, so we can get the status
                // directly.
                txReceiptStatus = result.status;
            }
            else {
                throw new Error(`Unexpected result type: ${typeof result}`);
            }
            expect(_.toString(txReceiptStatus)).to.equal('0', 'Expected transaction to fail but receipt had a non-zero status, indicating success');
        }))
            .catch((err) => __awaiter(this, void 0, void 0, function* () {
            // If the promise rejects, we expect a specific error message,
            // depending on the backing Ethereum node type.
            const errMessage = yield _getTransactionFailedErrorMessageAsync();
            expect(err.message).to.include(errMessage);
        }));
    });
}
exports.expectTransactionFailedWithoutReasonAsync = expectTransactionFailedWithoutReasonAsync;
/**
 * Resolves if the the contract call fails with the given revert reason.
 * @param p a Promise resulting from a contract call
 * @param reason a specific revert reason
 * @returns a new Promise which will reject if the conditions are not met and
 * otherwise resolve with no value.
 */
function expectContractCallFailedAsync(p, reason) {
    return __awaiter(this, void 0, void 0, function* () {
        const rejectionMessageRegex = new RegExp(`^VM Exception while processing transaction: revert ${reason}$`);
        return expect(p).to.be.rejectedWith(rejectionMessageRegex);
    });
}
exports.expectContractCallFailedAsync = expectContractCallFailedAsync;
/**
 * Resolves if the contract call fails without a revert reason.
 * @param p a Promise resulting from a contract call
 * @returns a new Promise which will reject if the conditions are not met and
 * otherwise resolve with no value.
 */
function expectContractCallFailedWithoutReasonAsync(p) {
    return __awaiter(this, void 0, void 0, function* () {
        const errMessage = yield _getContractCallFailedErrorMessageAsync();
        return expect(p).to.be.rejectedWith(errMessage);
    });
}
exports.expectContractCallFailedWithoutReasonAsync = expectContractCallFailedWithoutReasonAsync;
/**
 * Resolves if the contract creation/deployment fails without a revert reason.
 * @param p a Promise resulting from a contract creation/deployment
 * @returns a new Promise which will reject if the conditions are not met and
 * otherwise resolve with no value.
 */
function expectContractCreationFailedAsync(p, reason) {
    return __awaiter(this, void 0, void 0, function* () {
        return expectTransactionFailedAsync(p, reason);
    });
}
exports.expectContractCreationFailedAsync = expectContractCreationFailedAsync;
/**
 * Resolves if the contract creation/deployment fails without a revert reason.
 * @param p a Promise resulting from a contract creation/deployment
 * @returns a new Promise which will reject if the conditions are not met and
 * otherwise resolve with no value.
 */
function expectContractCreationFailedWithoutReasonAsync(p) {
    return __awaiter(this, void 0, void 0, function* () {
        const errMessage = yield _getTransactionFailedErrorMessageAsync();
        return expect(p).to.be.rejectedWith(errMessage);
    });
}
exports.expectContractCreationFailedWithoutReasonAsync = expectContractCreationFailedWithoutReasonAsync;
//# sourceMappingURL=assertions.js.map
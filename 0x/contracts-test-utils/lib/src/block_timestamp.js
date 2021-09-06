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
exports.getLatestBlockTimestampAsync = exports.increaseTimeAndMineBlockAsync = void 0;
const constants_1 = require("./constants");
const web3_wrapper_1 = require("./web3_wrapper");
let firstAccount;
/**
 * Increases time by the given number of seconds and then mines a block so that
 * the current block timestamp has the offset applied.
 * @param seconds the number of seconds by which to incrase the time offset.
 * @returns a new Promise which will resolve with the new total time offset or
 * reject if the time could not be increased.
 */
function increaseTimeAndMineBlockAsync(seconds) {
    return __awaiter(this, void 0, void 0, function* () {
        if (firstAccount === undefined) {
            const accounts = yield web3_wrapper_1.web3Wrapper.getAvailableAddressesAsync();
            firstAccount = accounts[0];
        }
        const offset = yield web3_wrapper_1.web3Wrapper.increaseTimeAsync(seconds);
        // Note: we need to send a transaction after increasing time so
        // that a block is actually mined. The contract looks at the
        // last mined block for the timestamp.
        yield web3_wrapper_1.web3Wrapper.awaitTransactionSuccessAsync(yield web3_wrapper_1.web3Wrapper.sendTransactionAsync({ from: firstAccount, to: firstAccount, value: 0 }), constants_1.constants.AWAIT_TRANSACTION_MINED_MS);
        return offset;
    });
}
exports.increaseTimeAndMineBlockAsync = increaseTimeAndMineBlockAsync;
/**
 * Returns the timestamp of the latest block in seconds since the Unix epoch.
 * @returns a new Promise which will resolve with the timestamp in seconds.
 */
function getLatestBlockTimestampAsync() {
    return __awaiter(this, void 0, void 0, function* () {
        const currentBlockIfExists = yield web3_wrapper_1.web3Wrapper.getBlockIfExistsAsync('latest');
        if (currentBlockIfExists === undefined) {
            throw new Error(`Unable to fetch latest block.`);
        }
        return currentBlockIfExists.timestamp;
    });
}
exports.getLatestBlockTimestampAsync = getLatestBlockTimestampAsync;
//# sourceMappingURL=block_timestamp.js.map
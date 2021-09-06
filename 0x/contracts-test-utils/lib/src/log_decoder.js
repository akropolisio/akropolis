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
exports.LogDecoder = void 0;
const utils_1 = require("@0x/utils");
const _ = require("lodash");
class LogDecoder {
    constructor(web3Wrapper, artifacts) {
        this._web3Wrapper = web3Wrapper;
        const abiArrays = [];
        _.forEach(artifacts, (artifact) => {
            const compilerOutput = artifact.compilerOutput;
            abiArrays.push(compilerOutput.abi);
        });
        this._abiDecoder = new utils_1.AbiDecoder(abiArrays);
    }
    static wrapLogBigNumbers(log) {
        const argNames = _.keys(log.args);
        for (const argName of argNames) {
            const isWeb3BigNumber = _.startsWith(log.args[argName].constructor.toString(), 'function BigNumber(');
            if (isWeb3BigNumber) {
                log.args[argName] = new utils_1.BigNumber(log.args[argName]);
            }
        }
    }
    decodeLogOrThrow(log) {
        const logWithDecodedArgsOrLog = this._abiDecoder.tryToDecodeLogOrNoop(log);
        // tslint:disable-next-line:no-unnecessary-type-assertion
        if (logWithDecodedArgsOrLog.args === undefined) {
            throw new Error(`Unable to decode log: ${JSON.stringify(log)}`);
        }
        LogDecoder.wrapLogBigNumbers(logWithDecodedArgsOrLog);
        return logWithDecodedArgsOrLog;
    }
    getTxWithDecodedLogsAsync(txHash) {
        return __awaiter(this, void 0, void 0, function* () {
            const receipt = yield this._web3Wrapper.awaitTransactionSuccessAsync(txHash);
            return this.decodeReceiptLogs(receipt);
        });
    }
    decodeReceiptLogs(receipt) {
        const decodedLogs = receipt.logs.map(log => this.decodeLogOrThrow(log));
        return _.merge({}, receipt, { logs: decodedLogs });
    }
}
exports.LogDecoder = LogDecoder;
//# sourceMappingURL=log_decoder.js.map
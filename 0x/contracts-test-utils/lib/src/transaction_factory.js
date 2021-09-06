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
exports.TransactionFactory = void 0;
const order_utils_1 = require("@0x/order-utils");
const types_1 = require("@0x/types");
const utils_1 = require("@0x/utils");
const ethUtil = require("ethereumjs-util");
const src_1 = require("../src");
const block_timestamp_1 = require("./block_timestamp");
const constants_1 = require("./constants");
const signing_utils_1 = require("./signing_utils");
class TransactionFactory {
    constructor(privateKey, exchangeAddress, chainId) {
        this._privateKey = privateKey;
        this._exchangeAddress = exchangeAddress;
        this._chainId = chainId;
        this._signerBuff = ethUtil.privateToAddress(this._privateKey);
    }
    newSignedTransactionAsync(customTransactionParams, signatureType = types_1.SignatureType.EthSign) {
        return __awaiter(this, void 0, void 0, function* () {
            if (customTransactionParams.data === undefined) {
                throw new Error('Error: ZeroExTransaction data field must be supplied');
            }
            const tenMinutesInSeconds = 10 * 60;
            const currentBlockTimestamp = yield block_timestamp_1.getLatestBlockTimestampAsync();
            const salt = order_utils_1.generatePseudoRandomSalt();
            const signerAddress = `0x${this._signerBuff.toString('hex')}`;
            const transaction = Object.assign({ salt,
                signerAddress, data: customTransactionParams.data, expirationTimeSeconds: new utils_1.BigNumber(currentBlockTimestamp).plus(tenMinutesInSeconds), gasPrice: new utils_1.BigNumber(constants_1.constants.DEFAULT_GAS_PRICE), domain: {
                    verifyingContract: this._exchangeAddress,
                    chainId: this._chainId,
                } }, customTransactionParams);
            const transactionHashBuffer = src_1.transactionHashUtils.getTransactionHashBuffer(transaction);
            const signature = signing_utils_1.signingUtils.signMessage(transactionHashBuffer, this._privateKey, signatureType);
            const signedTransaction = Object.assign(Object.assign({}, transaction), { signature: `0x${signature.toString('hex')}` });
            return signedTransaction;
        });
    }
}
exports.TransactionFactory = TransactionFactory;
//# sourceMappingURL=transaction_factory.js.map
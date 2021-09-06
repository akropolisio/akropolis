"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.transactionHashUtils = void 0;
const assert_1 = require("@0x/assert");
const json_schemas_1 = require("@0x/json-schemas");
const order_utils_1 = require("@0x/order-utils");
const utils_1 = require("@0x/utils");
exports.transactionHashUtils = {
    /**
     * Computes the transactionHash for a supplied 0x transaction.
     * @param   transaction   An object that conforms to the ZeroExTransaction or SignedZeroExTransaction interface definitions.
     * @return  Hex encoded string transactionHash from hashing the supplied order.
     */
    getTransactionHashHex(transaction) {
        assert_1.assert.doesConformToSchema('transaction', transaction, json_schemas_1.schemas.zeroExTransactionSchema, [json_schemas_1.schemas.hexSchema]);
        const transactionHashBuff = exports.transactionHashUtils.getTransactionHashBuffer(transaction);
        const transactionHashHex = `0x${transactionHashBuff.toString('hex')}`;
        return transactionHashHex;
    },
    /**
     * Computes the transactionHash for a supplied 0x transaction.
     * @param   transaction   An object that conforms to the ZeroExTransaction or SignedZeroExTransaction interface definitions.
     * @return  A Buffer containing the resulting transactionHash from hashing the supplied 0x transaction.
     */
    getTransactionHashBuffer(transaction) {
        const typedData = order_utils_1.eip712Utils.createZeroExTransactionTypedData(transaction);
        const transactionHashBuff = utils_1.signTypedDataUtils.generateTypedDataHash(typedData);
        return transactionHashBuff;
    },
};
//# sourceMappingURL=transaction_hash.js.map
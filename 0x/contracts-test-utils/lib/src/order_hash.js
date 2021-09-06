"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.orderHashUtils = void 0;
const assert_1 = require("@0x/assert");
const json_schemas_1 = require("@0x/json-schemas");
const order_utils_1 = require("@0x/order-utils");
const utils_1 = require("@0x/utils");
const _ = require("lodash");
const INVALID_TAKER_FORMAT = 'instance.takerAddress is not of a type(s) string';
const NULL_ADDRESS = '0x0000000000000000000000000000000000000000';
exports.orderHashUtils = {
    /**
     * Computes the orderHash for a supplied order.
     * @param   order   An object that conforms to the Order or SignedOrder interface definitions.
     * @return  Hex encoded string orderHash from hashing the supplied order.
     */
    getOrderHashHex(order) {
        try {
            assert_1.assert.doesConformToSchema('order', order, json_schemas_1.schemas.orderSchema, [json_schemas_1.schemas.hexSchema]);
        }
        catch (error) {
            if (_.includes(error.message, INVALID_TAKER_FORMAT)) {
                const errMsg = `Order taker must be of type string. If you want anyone to be able to fill an order - pass ${NULL_ADDRESS}`;
                throw new Error(errMsg);
            }
            throw error;
        }
        const orderHashBuff = exports.orderHashUtils.getOrderHashBuffer(order);
        const orderHashHex = `0x${orderHashBuff.toString('hex')}`;
        return orderHashHex;
    },
    /**
     * Computes the orderHash for a supplied order
     * @param   order   An object that conforms to the Order or SignedOrder interface definitions.
     * @return  A Buffer containing the resulting orderHash from hashing the supplied order
     */
    getOrderHashBuffer(order) {
        try {
            assert_1.assert.doesConformToSchema('order', order, json_schemas_1.schemas.orderSchema, [json_schemas_1.schemas.hexSchema]);
        }
        catch (error) {
            if (_.includes(error.message, INVALID_TAKER_FORMAT)) {
                const errMsg = `Order taker must be of type string. If you want anyone to be able to fill an order - pass ${NULL_ADDRESS}`;
                throw new Error(errMsg);
            }
            throw error;
        }
        const typedData = order_utils_1.eip712Utils.createOrderTypedData(order);
        const orderHashBuff = utils_1.signTypedDataUtils.generateTypedDataHash(typedData);
        return orderHashBuff;
    },
};
//# sourceMappingURL=order_hash.js.map
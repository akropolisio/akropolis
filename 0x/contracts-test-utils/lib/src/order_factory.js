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
exports.OrderFactory = void 0;
const order_utils_1 = require("@0x/order-utils");
const types_1 = require("@0x/types");
const utils_1 = require("@0x/utils");
const block_timestamp_1 = require("./block_timestamp");
const constants_1 = require("./constants");
const order_hash_1 = require("./order_hash");
const signing_utils_1 = require("./signing_utils");
class OrderFactory {
    constructor(privateKey, defaultOrderParams) {
        this._defaultOrderParams = defaultOrderParams;
        this._privateKey = privateKey;
    }
    newSignedOrderAsync(customOrderParams = {}, signatureType = types_1.SignatureType.EthSign) {
        return __awaiter(this, void 0, void 0, function* () {
            const fifteenMinutesInSeconds = 15 * 60;
            const currentBlockTimestamp = yield block_timestamp_1.getLatestBlockTimestampAsync();
            const order = Object.assign(Object.assign({ takerAddress: constants_1.constants.NULL_ADDRESS, senderAddress: constants_1.constants.NULL_ADDRESS, expirationTimeSeconds: new utils_1.BigNumber(currentBlockTimestamp).plus(fifteenMinutesInSeconds), salt: order_utils_1.generatePseudoRandomSalt() }, this._defaultOrderParams), customOrderParams); // tslint:disable-line:no-object-literal-type-assertion
            const orderHashBuff = order_hash_1.orderHashUtils.getOrderHashBuffer(order);
            const signature = signing_utils_1.signingUtils.signMessage(orderHashBuff, this._privateKey, signatureType);
            const signedOrder = Object.assign(Object.assign({}, order), { signature: `0x${signature.toString('hex')}` });
            return signedOrder;
        });
    }
}
exports.OrderFactory = OrderFactory;
//# sourceMappingURL=order_factory.js.map
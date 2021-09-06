"use strict";
var __rest = (this && this.__rest) || function (s, e) {
    var t = {};
    for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p) && e.indexOf(p) < 0)
        t[p] = s[p];
    if (s != null && typeof Object.getOwnPropertySymbols === "function")
        for (var i = 0, p = Object.getOwnPropertySymbols(s); i < p.length; i++) {
            if (e.indexOf(p[i]) < 0 && Object.prototype.propertyIsEnumerable.call(s, p[i]))
                t[p[i]] = s[p[i]];
        }
    return t;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.orderUtils = void 0;
const order_utils_1 = require("@0x/order-utils");
const utils_1 = require("@0x/utils");
const constants_1 = require("./constants");
exports.orderUtils = {
    getPartialAmountFloor(numerator, denominator, target) {
        const partialAmount = numerator
            .multipliedBy(target)
            .div(denominator)
            .integerValue(utils_1.BigNumber.ROUND_FLOOR);
        return partialAmount;
    },
    createFill: (signedOrder, takerAssetFillAmount) => {
        const fill = {
            order: signedOrder,
            takerAssetFillAmount: takerAssetFillAmount || signedOrder.takerAssetAmount,
            signature: signedOrder.signature,
        };
        return fill;
    },
    createCancel(signedOrder, takerAssetCancelAmount) {
        const cancel = {
            order: signedOrder,
            takerAssetCancelAmount: takerAssetCancelAmount || signedOrder.takerAssetAmount,
        };
        return cancel;
    },
    createOrderWithoutSignature(signedOrder) {
        const { signature } = signedOrder, order = __rest(signedOrder, ["signature"]);
        return order;
    },
    createBatchMatchOrders(signedOrdersLeft, signedOrdersRight) {
        return {
            leftOrders: signedOrdersLeft.map(order => exports.orderUtils.createOrderWithoutSignature(order)),
            rightOrders: signedOrdersRight.map(order => {
                const right = exports.orderUtils.createOrderWithoutSignature(order);
                right.makerAssetData = constants_1.constants.NULL_BYTES;
                right.takerAssetData = constants_1.constants.NULL_BYTES;
                return right;
            }),
            leftSignatures: signedOrdersLeft.map(order => order.signature),
            rightSignatures: signedOrdersRight.map(order => order.signature),
        };
    },
    createMatchOrders(signedOrderLeft, signedOrderRight) {
        const fill = {
            left: exports.orderUtils.createOrderWithoutSignature(signedOrderLeft),
            right: exports.orderUtils.createOrderWithoutSignature(signedOrderRight),
            leftSignature: signedOrderLeft.signature,
            rightSignature: signedOrderRight.signature,
        };
        fill.right.makerAssetData = constants_1.constants.NULL_BYTES;
        fill.right.takerAssetData = constants_1.constants.NULL_BYTES;
        return fill;
    },
    generatePseudoRandomOrderHash() {
        const randomBigNum = order_utils_1.generatePseudoRandomSalt();
        const randomHash = utils_1.hexUtils.hash(randomBigNum);
        return randomHash;
    },
};
//# sourceMappingURL=order_utils.js.map
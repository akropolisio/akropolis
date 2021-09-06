"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.typeEncodingUtils = void 0;
const utils_1 = require("@0x/utils");
const BN = require("bn.js");
const ethUtil = require("ethereumjs-util");
const constants_1 = require("./constants");
exports.typeEncodingUtils = {
    encodeUint256(value) {
        const base = 10;
        const formattedValue = new BN(value.toString(base));
        const encodedValue = ethUtil.toBuffer(formattedValue);
        // tslint:disable-next-line:custom-no-magic-numbers
        const paddedValue = ethUtil.setLengthLeft(encodedValue, constants_1.constants.WORD_LENGTH);
        return paddedValue;
    },
    decodeUint256(encodedValue) {
        const formattedValue = ethUtil.bufferToHex(encodedValue);
        const value = new utils_1.BigNumber(formattedValue, constants_1.constants.BASE_16);
        return value;
    },
};
//# sourceMappingURL=type_encoding_utils.js.map
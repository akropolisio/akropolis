"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.signingUtils = void 0;
const types_1 = require("@0x/types");
const ethUtil = require("ethereumjs-util");
exports.signingUtils = {
    signMessage(message, privateKey, signatureType) {
        if (signatureType === types_1.SignatureType.EthSign) {
            const prefixedMessage = ethUtil.hashPersonalMessage(message);
            const ecSignature = ethUtil.ecsign(prefixedMessage, privateKey);
            const signature = Buffer.concat([
                ethUtil.toBuffer(ecSignature.v),
                ecSignature.r,
                ecSignature.s,
                ethUtil.toBuffer(signatureType),
            ]);
            return signature;
        }
        else if (signatureType === types_1.SignatureType.EIP712) {
            const ecSignature = ethUtil.ecsign(message, privateKey);
            const signature = Buffer.concat([
                ethUtil.toBuffer(ecSignature.v),
                ecSignature.r,
                ecSignature.s,
                ethUtil.toBuffer(signatureType),
            ]);
            return signature;
        }
        else {
            throw new Error(`${signatureType} is not a valid signature type`);
        }
    },
};
//# sourceMappingURL=signing_utils.js.map
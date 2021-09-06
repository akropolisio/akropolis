"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.randomAddress = void 0;
const utils_1 = require("@0x/utils");
const constants_1 = require("./constants");
/**
 * Generates a random address.
 */
function randomAddress() {
    return utils_1.hexUtils.random(constants_1.constants.ADDRESS_LENGTH);
}
exports.randomAddress = randomAddress;
//# sourceMappingURL=address_utils.js.map
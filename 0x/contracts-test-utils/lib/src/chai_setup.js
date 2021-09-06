"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.expect = exports.chaiSetup = void 0;
const dev_utils_1 = require("@0x/dev-utils");
var dev_utils_2 = require("@0x/dev-utils");
Object.defineProperty(exports, "chaiSetup", { enumerable: true, get: function () { return dev_utils_2.chaiSetup; } });
const chai = require("chai");
// Set up chai.
dev_utils_1.chaiSetup.configure();
exports.expect = chai.expect;
//# sourceMappingURL=chai_setup.js.map
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.revertTrace = void 0;
const dev_utils_1 = require("@0x/dev-utils");
const sol_trace_1 = require("@0x/sol-trace");
let revertTraceSubprovider;
exports.revertTrace = {
    getRevertTraceSubproviderSingleton() {
        if (revertTraceSubprovider === undefined) {
            revertTraceSubprovider = exports.revertTrace._getRevertTraceSubprovider();
        }
        return revertTraceSubprovider;
    },
    _getRevertTraceSubprovider() {
        const defaultFromAddress = dev_utils_1.devConstants.TESTRPC_FIRST_ADDRESS;
        const solCompilerArtifactAdapter = new sol_trace_1.SolCompilerArtifactAdapter();
        const isVerbose = true;
        const subprovider = new sol_trace_1.RevertTraceSubprovider(solCompilerArtifactAdapter, defaultFromAddress, isVerbose);
        return subprovider;
    },
};
//# sourceMappingURL=revert_trace.js.map
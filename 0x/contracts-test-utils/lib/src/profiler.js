"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.profiler = void 0;
const dev_utils_1 = require("@0x/dev-utils");
const sol_profiler_1 = require("@0x/sol-profiler");
let profilerSubprovider;
exports.profiler = {
    start() {
        exports.profiler.getProfilerSubproviderSingleton().start();
    },
    stop() {
        exports.profiler.getProfilerSubproviderSingleton().stop();
    },
    getProfilerSubproviderSingleton() {
        if (profilerSubprovider === undefined) {
            profilerSubprovider = exports.profiler._getProfilerSubprovider();
        }
        return profilerSubprovider;
    },
    _getProfilerSubprovider() {
        const defaultFromAddress = dev_utils_1.devConstants.TESTRPC_FIRST_ADDRESS;
        const solCompilerArtifactAdapter = new sol_profiler_1.SolCompilerArtifactAdapter();
        const isVerbose = true;
        const subprovider = new sol_profiler_1.ProfilerSubprovider(solCompilerArtifactAdapter, defaultFromAddress, isVerbose);
        return subprovider;
    },
};
//# sourceMappingURL=profiler.js.map
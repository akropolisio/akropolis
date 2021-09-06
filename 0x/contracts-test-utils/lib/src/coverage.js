"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.coverage = void 0;
const dev_utils_1 = require("@0x/dev-utils");
const sol_coverage_1 = require("@0x/sol-coverage");
let coverageSubprovider;
exports.coverage = {
    getCoverageSubproviderSingleton() {
        if (coverageSubprovider === undefined) {
            coverageSubprovider = exports.coverage._getCoverageSubprovider();
        }
        return coverageSubprovider;
    },
    _getCoverageSubprovider() {
        const defaultFromAddress = dev_utils_1.devConstants.TESTRPC_FIRST_ADDRESS;
        const solCompilerArtifactAdapter = new sol_coverage_1.SolCompilerArtifactAdapter();
        const coverageSubproviderConfig = {
            isVerbose: true,
            ignoreFilesGlobs: ['**/node_modules/**', '**/interfaces/**', '**/test/**'],
        };
        const subprovider = new sol_coverage_1.CoverageSubprovider(solCompilerArtifactAdapter, defaultFromAddress, coverageSubproviderConfig);
        return subprovider;
    },
};
//# sourceMappingURL=coverage.js.map
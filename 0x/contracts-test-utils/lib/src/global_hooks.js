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
const dev_utils_1 = require("@0x/dev-utils");
const coverage_1 = require("./coverage");
const profiler_1 = require("./profiler");
after('generate coverage report', () => __awaiter(void 0, void 0, void 0, function* () {
    if (dev_utils_1.env.parseBoolean(dev_utils_1.EnvVars.SolidityCoverage)) {
        const coverageSubprovider = coverage_1.coverage.getCoverageSubproviderSingleton();
        yield coverageSubprovider.writeCoverageAsync();
    }
    if (dev_utils_1.env.parseBoolean(dev_utils_1.EnvVars.SolidityProfiler)) {
        const profilerSubprovider = profiler_1.profiler.getProfilerSubproviderSingleton();
        yield profilerSubprovider.writeProfilerOutputAsync();
    }
}));
//# sourceMappingURL=global_hooks.js.map
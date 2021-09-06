"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.web3Wrapper = exports.provider = exports.providerConfigs = exports.txDefaults = void 0;
const dev_utils_1 = require("@0x/dev-utils");
const subproviders_1 = require("@0x/subproviders");
const utils_1 = require("@0x/utils");
const web3_wrapper_1 = require("@0x/web3-wrapper");
const _ = require("lodash");
const constants_1 = require("./constants");
const coverage_1 = require("./coverage");
const profiler_1 = require("./profiler");
const revert_trace_1 = require("./revert_trace");
exports.txDefaults = {
    from: dev_utils_1.devConstants.TESTRPC_FIRST_ADDRESS,
    gas: dev_utils_1.devConstants.GAS_LIMIT,
    gasPrice: constants_1.constants.DEFAULT_GAS_PRICE,
};
exports.providerConfigs = {
    total_accounts: constants_1.constants.NUM_TEST_ACCOUNTS,
    shouldUseInProcessGanache: true,
    shouldAllowUnlimitedContractSize: true,
    hardfork: 'istanbul',
    gasLimit: 100e6,
    unlocked_accounts: [
        '0x6cc5f688a315f3dc28a7781717a9a798a59fda7b',
        '0x55dc8f21d20d4c6ed3c82916a438a413ca68e335',
        '0x8ed95d1746bf1e4dab58d8ed4724f1ef95b20db0',
        '0xf977814e90da44bfa03b6295a0616a897441acec', // Binance: USDC, TUSD
    ],
};
exports.provider = dev_utils_1.web3Factory.getRpcProvider(exports.providerConfigs);
exports.provider.stop();
const isCoverageEnabled = dev_utils_1.env.parseBoolean(dev_utils_1.EnvVars.SolidityCoverage);
const isProfilerEnabled = dev_utils_1.env.parseBoolean(dev_utils_1.EnvVars.SolidityProfiler);
const isRevertTraceEnabled = dev_utils_1.env.parseBoolean(dev_utils_1.EnvVars.SolidityRevertTrace);
const enabledSubproviderCount = _.filter([isCoverageEnabled, isProfilerEnabled, isRevertTraceEnabled], _.identity.bind(_)).length;
if (enabledSubproviderCount > 1) {
    throw new Error(`Only one of coverage, profiler, or revert trace subproviders can be enabled at a time`);
}
if (isCoverageEnabled) {
    const coverageSubprovider = coverage_1.coverage.getCoverageSubproviderSingleton();
    subproviders_1.prependSubprovider(exports.provider, coverageSubprovider);
}
if (isProfilerEnabled) {
    const profilerSubprovider = profiler_1.profiler.getProfilerSubproviderSingleton();
    utils_1.logUtils.log("By default profilerSubprovider is stopped so that you don't get noise from setup code. Don't forget to start it before the code you want to profile and stop it afterwards");
    profilerSubprovider.stop();
    subproviders_1.prependSubprovider(exports.provider, profilerSubprovider);
}
if (isRevertTraceEnabled) {
    const revertTraceSubprovider = revert_trace_1.revertTrace.getRevertTraceSubproviderSingleton();
    subproviders_1.prependSubprovider(exports.provider, revertTraceSubprovider);
}
exports.web3Wrapper = new web3_wrapper_1.Web3Wrapper(exports.provider);
//# sourceMappingURL=web3_wrapper.js.map
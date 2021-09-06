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
exports.blockchainTests = exports.describe = exports.LiveBlockchainTestsEnvironmentSingleton = exports.ForkedBlockchainTestsEnvironmentSingleton = exports.StandardBlockchainTestsEnvironmentSingleton = void 0;
const dev_utils_1 = require("@0x/dev-utils");
const subproviders_1 = require("@0x/subproviders");
const utils_1 = require("@0x/utils");
const web3_wrapper_1 = require("@0x/web3-wrapper");
const _ = require("lodash");
const process = require("process");
const web3_wrapper_2 = require("./web3_wrapper");
let TEST_ENV_CONFIG = {};
class BlockchainTestsEnvironmentBase {
    getChainIdAsync() {
        return __awaiter(this, void 0, void 0, function* () {
            return utils_1.providerUtils.getChainIdAsync(this.provider);
        });
    }
    getAccountAddressesAsync() {
        return __awaiter(this, void 0, void 0, function* () {
            return this.web3Wrapper.getAvailableAddressesAsync();
        });
    }
}
/**
 * `BlockchainTestsEnvironment` that uses the default ganache provider.
 */
class StandardBlockchainTestsEnvironmentSingleton extends BlockchainTestsEnvironmentBase {
    constructor() {
        super();
        this.blockchainLifecycle = new dev_utils_1.BlockchainLifecycle(web3_wrapper_2.web3Wrapper);
        this.provider = web3_wrapper_2.provider;
        this.txDefaults = web3_wrapper_2.txDefaults;
        this.web3Wrapper = web3_wrapper_2.web3Wrapper;
    }
    // Create or retrieve the singleton instance of this class.
    static create() {
        if (StandardBlockchainTestsEnvironmentSingleton._instance === undefined) {
            StandardBlockchainTestsEnvironmentSingleton._instance = new StandardBlockchainTestsEnvironmentSingleton();
        }
        return StandardBlockchainTestsEnvironmentSingleton._instance;
    }
    // Reset the singleton.
    static reset() {
        StandardBlockchainTestsEnvironmentSingleton._instance = undefined;
    }
    // Get the singleton instance of this class.
    static getInstance() {
        return StandardBlockchainTestsEnvironmentSingleton._instance;
    }
}
exports.StandardBlockchainTestsEnvironmentSingleton = StandardBlockchainTestsEnvironmentSingleton;
/**
 * `BlockchainTestsEnvironment` that uses a forked ganache provider.
 */
class ForkedBlockchainTestsEnvironmentSingleton extends BlockchainTestsEnvironmentBase {
    constructor() {
        super();
        this.txDefaults = web3_wrapper_2.txDefaults;
        this.provider = process.env.FORK_RPC_URL
            ? ForkedBlockchainTestsEnvironmentSingleton._createWeb3Provider(process.env.FORK_RPC_URL)
            : // Create a dummy provider if no RPC backend supplied.
                createDummyProvider();
        this.web3Wrapper = new web3_wrapper_1.Web3Wrapper(this.provider);
        this.blockchainLifecycle = new dev_utils_1.BlockchainLifecycle(this.web3Wrapper);
    }
    // Create or retrieve the singleton instance of this class.
    static create() {
        if (ForkedBlockchainTestsEnvironmentSingleton._instance === undefined) {
            ForkedBlockchainTestsEnvironmentSingleton._instance = new ForkedBlockchainTestsEnvironmentSingleton();
        }
        return ForkedBlockchainTestsEnvironmentSingleton._instance;
    }
    // Reset the singleton.
    static reset() {
        ForkedBlockchainTestsEnvironmentSingleton._instance = undefined;
    }
    static _createWeb3Provider(forkHost) {
        const forkConfig = TEST_ENV_CONFIG.fork || {};
        const unlockedAccounts = forkConfig.unlockedAccounts;
        return dev_utils_1.web3Factory.getRpcProvider(Object.assign(Object.assign(Object.assign({}, web3_wrapper_2.providerConfigs), { fork: forkHost, blockTime: 0 }), (unlockedAccounts ? { unlocked_accounts: unlockedAccounts } : {})));
    }
    // Get the singleton instance of this class.
    static getInstance() {
        return ForkedBlockchainTestsEnvironmentSingleton._instance;
    }
}
exports.ForkedBlockchainTestsEnvironmentSingleton = ForkedBlockchainTestsEnvironmentSingleton;
/**
 * `BlockchainTestsEnvironment` that uses a live web3 provider.
 */
class LiveBlockchainTestsEnvironmentSingleton extends BlockchainTestsEnvironmentBase {
    constructor() {
        super();
        this.txDefaults = web3_wrapper_2.txDefaults;
        this.provider = process.env.LIVE_RPC_URL
            ? LiveBlockchainTestsEnvironmentSingleton._createWeb3Provider(process.env.LIVE_RPC_URL)
            : // Create a dummy provider if no RPC backend supplied.
                createDummyProvider();
        this.web3Wrapper = new web3_wrapper_1.Web3Wrapper(this.provider);
        const snapshotHandlerAsync = () => __awaiter(this, void 0, void 0, function* () {
            throw new Error('Snapshots are not supported with a live provider.');
        });
        this.blockchainLifecycle = {
            startAsync: snapshotHandlerAsync,
            revertAsync: snapshotHandlerAsync,
        };
    }
    // Create or retrieve the singleton instance of this class.
    static create() {
        if (LiveBlockchainTestsEnvironmentSingleton._instance === undefined) {
            LiveBlockchainTestsEnvironmentSingleton._instance = new LiveBlockchainTestsEnvironmentSingleton();
        }
        return LiveBlockchainTestsEnvironmentSingleton._instance;
    }
    // Reset the singleton.
    static reset() {
        LiveBlockchainTestsEnvironmentSingleton._instance = undefined;
    }
    static _createWeb3Provider(rpcHost) {
        const providerEngine = new subproviders_1.Web3ProviderEngine();
        providerEngine.addProvider(new subproviders_1.RPCSubprovider(rpcHost));
        utils_1.providerUtils.startProviderEngine(providerEngine);
        return providerEngine;
    }
    // Get the singleton instance of this class.
    static getInstance() {
        return LiveBlockchainTestsEnvironmentSingleton._instance;
    }
}
exports.LiveBlockchainTestsEnvironmentSingleton = LiveBlockchainTestsEnvironmentSingleton;
// The original `describe()` global provided by mocha.
const mochaDescribe = global.describe;
/**
 * An augmented version of mocha's `describe()`.
 */
exports.describe = _.assign(mochaDescribe, {
    optional(description, callback) {
        const describeCall = process.env.TEST_ALL ? mochaDescribe : mochaDescribe.skip;
        return describeCall(description, callback);
    },
});
/**
 * Like mocha's `describe()`, but sets up a blockchain environment for you.
 */
exports.blockchainTests = _.assign(function (description, callback) {
    return defineBlockchainSuite(StandardBlockchainTestsEnvironmentSingleton, description, callback, exports.describe);
}, {
    configure(config) {
        // Update the global config and reset all environment singletons.
        TEST_ENV_CONFIG = Object.assign(Object.assign({}, TEST_ENV_CONFIG), config);
        ForkedBlockchainTestsEnvironmentSingleton.reset();
        StandardBlockchainTestsEnvironmentSingleton.reset();
        LiveBlockchainTestsEnvironmentSingleton.reset();
    },
    only(description, callback) {
        return defineBlockchainSuite(StandardBlockchainTestsEnvironmentSingleton, description, callback, exports.describe.only);
    },
    skip(description, callback) {
        return defineBlockchainSuite(StandardBlockchainTestsEnvironmentSingleton, description, callback, exports.describe.skip);
    },
    optional(description, callback) {
        return defineBlockchainSuite(StandardBlockchainTestsEnvironmentSingleton, description, callback, process.env.TEST_ALL ? exports.describe : exports.describe.skip);
    },
    fork: _.assign(function (description, callback) {
        return defineBlockchainSuite(ForkedBlockchainTestsEnvironmentSingleton, description, callback, process.env.FORK_RPC_URL ? exports.describe : exports.describe.skip);
    }, {
        only(description, callback) {
            return defineBlockchainSuite(ForkedBlockchainTestsEnvironmentSingleton, description, callback, process.env.FORK_RPC_URL ? exports.describe.only : exports.describe.skip);
        },
        skip(description, callback) {
            return defineBlockchainSuite(ForkedBlockchainTestsEnvironmentSingleton, description, callback, exports.describe.skip);
        },
        optional(description, callback) {
            return defineBlockchainSuite(ForkedBlockchainTestsEnvironmentSingleton, description, callback, process.env.FORK_RPC_URL ? exports.describe.optional : exports.describe.skip);
        },
        resets(description, callback) {
            return defineResetsBlockchainSuite(ForkedBlockchainTestsEnvironmentSingleton, description, callback, process.env.FORK_RPC_URL ? exports.describe : exports.describe.skip);
        },
    }),
    live: _.assign(function (description, callback) {
        return defineBlockchainSuite(LiveBlockchainTestsEnvironmentSingleton, description, callback, process.env.LIVE_RPC_URL ? exports.describe : exports.describe.skip);
    }, {
        only(description, callback) {
            return defineBlockchainSuite(LiveBlockchainTestsEnvironmentSingleton, description, callback, process.env.LIVE_RPC_URL ? exports.describe.only : exports.describe.skip);
        },
        skip(description, callback) {
            return defineBlockchainSuite(LiveBlockchainTestsEnvironmentSingleton, description, callback, exports.describe.skip);
        },
        optional(description, callback) {
            return defineBlockchainSuite(LiveBlockchainTestsEnvironmentSingleton, description, callback, process.env.LIVE_RPC_URL ? exports.describe.optional : exports.describe.skip);
        },
    }),
    resets: _.assign(function (description, callback) {
        return defineResetsBlockchainSuite(StandardBlockchainTestsEnvironmentSingleton, description, callback, exports.describe);
    }, {
        only(description, callback) {
            return defineResetsBlockchainSuite(StandardBlockchainTestsEnvironmentSingleton, description, callback, exports.describe.only);
        },
        skip(description, callback) {
            return defineResetsBlockchainSuite(StandardBlockchainTestsEnvironmentSingleton, description, callback, exports.describe.skip);
        },
        optional(description, callback) {
            return defineResetsBlockchainSuite(StandardBlockchainTestsEnvironmentSingleton, description, callback, exports.describe.optional);
        },
    }),
});
function defineBlockchainSuite(envFactory, description, callback, describeCall) {
    return describeCall(description, function () {
        callback.call(this, envFactory.create());
    });
}
function defineResetsBlockchainSuite(envFactory, description, callback, describeCall) {
    return describeCall(description, function () {
        const env = envFactory.create();
        beforeEach(() => __awaiter(this, void 0, void 0, function* () { return env.blockchainLifecycle.startAsync(); }));
        afterEach(() => __awaiter(this, void 0, void 0, function* () { return env.blockchainLifecycle.revertAsync(); }));
        callback.call(this, env);
    });
}
function createDummyProvider() {
    return {
        addProvider: _.noop,
        on: _.noop,
        send: _.noop,
        sendAsync: _.noop,
        start: _.noop,
        stop: _.noop,
    };
}
//# sourceMappingURL=mocha_blockchain.js.map
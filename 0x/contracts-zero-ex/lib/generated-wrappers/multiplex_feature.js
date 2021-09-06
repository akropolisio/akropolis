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
exports.MultiplexFeatureContract = exports.MultiplexFeatureEvents = void 0;
// tslint:disable:no-consecutive-blank-lines ordered-imports align trailing-comma enum-naming
// tslint:disable:whitespace no-unbound-method no-trailing-whitespace
// tslint:disable:no-unused-variable
const base_contract_1 = require("@0x/base-contract");
const json_schemas_1 = require("@0x/json-schemas");
const utils_1 = require("@0x/utils");
const web3_wrapper_1 = require("@0x/web3-wrapper");
const assert_1 = require("@0x/assert");
const ethers = require("ethers");
var MultiplexFeatureEvents;
(function (MultiplexFeatureEvents) {
    MultiplexFeatureEvents["ExpiredOtcOrder"] = "ExpiredOtcOrder";
    MultiplexFeatureEvents["ExpiredRfqOrder"] = "ExpiredRfqOrder";
    MultiplexFeatureEvents["LiquidityProviderSwap"] = "LiquidityProviderSwap";
})(MultiplexFeatureEvents = exports.MultiplexFeatureEvents || (exports.MultiplexFeatureEvents = {}));
/* istanbul ignore next */
// tslint:disable:array-type
// tslint:disable:no-parameter-reassignment
// tslint:disable-next-line:class-name
class MultiplexFeatureContract extends base_contract_1.BaseContract {
    constructor(address, supportedProvider, txDefaults, logDecodeDependencies, deployedBytecode = MultiplexFeatureContract.deployedBytecode, encoderOverrides) {
        super('MultiplexFeature', MultiplexFeatureContract.ABI(), address, supportedProvider, txDefaults, logDecodeDependencies, deployedBytecode, encoderOverrides);
        this._methodABIIndex = {};
        utils_1.classUtils.bindAll(this, ['_abiEncoderByFunctionSignature', 'address', '_web3Wrapper']);
        this._subscriptionManager = new base_contract_1.SubscriptionManager(MultiplexFeatureContract.ABI(), this._web3Wrapper);
        MultiplexFeatureContract.ABI().forEach((item, index) => {
            if (item.type === 'function') {
                const methodAbi = item;
                this._methodABIIndex[methodAbi.name] = index;
            }
        });
    }
    static deployFrom0xArtifactAsync(artifact, supportedProvider, txDefaults, logDecodeDependencies, zeroExAddress, weth, sandbox, uniswapFactory, sushiswapFactory, uniswapPairInitCodeHash, sushiswapPairInitCodeHash) {
        return __awaiter(this, void 0, void 0, function* () {
            assert_1.assert.doesConformToSchema('txDefaults', txDefaults, json_schemas_1.schemas.txDataSchema);
            if (artifact.compilerOutput === undefined) {
                throw new Error('Compiler output not found in the artifact file');
            }
            const provider = utils_1.providerUtils.standardizeOrThrow(supportedProvider);
            const bytecode = artifact.compilerOutput.evm.bytecode.object;
            const abi = artifact.compilerOutput.abi;
            const logDecodeDependenciesAbiOnly = {};
            if (Object.keys(logDecodeDependencies) !== undefined) {
                for (const key of Object.keys(logDecodeDependencies)) {
                    logDecodeDependenciesAbiOnly[key] = logDecodeDependencies[key].compilerOutput.abi;
                }
            }
            return MultiplexFeatureContract.deployAsync(bytecode, abi, provider, txDefaults, logDecodeDependenciesAbiOnly, zeroExAddress, weth, sandbox, uniswapFactory, sushiswapFactory, uniswapPairInitCodeHash, sushiswapPairInitCodeHash);
        });
    }
    static deployWithLibrariesFrom0xArtifactAsync(artifact, libraryArtifacts, supportedProvider, txDefaults, logDecodeDependencies, zeroExAddress, weth, sandbox, uniswapFactory, sushiswapFactory, uniswapPairInitCodeHash, sushiswapPairInitCodeHash) {
        return __awaiter(this, void 0, void 0, function* () {
            assert_1.assert.doesConformToSchema('txDefaults', txDefaults, json_schemas_1.schemas.txDataSchema);
            if (artifact.compilerOutput === undefined) {
                throw new Error('Compiler output not found in the artifact file');
            }
            const provider = utils_1.providerUtils.standardizeOrThrow(supportedProvider);
            const abi = artifact.compilerOutput.abi;
            const logDecodeDependenciesAbiOnly = {};
            if (Object.keys(logDecodeDependencies) !== undefined) {
                for (const key of Object.keys(logDecodeDependencies)) {
                    logDecodeDependenciesAbiOnly[key] = logDecodeDependencies[key].compilerOutput.abi;
                }
            }
            const libraryAddresses = yield MultiplexFeatureContract._deployLibrariesAsync(artifact, libraryArtifacts, new web3_wrapper_1.Web3Wrapper(provider), txDefaults);
            const bytecode = base_contract_1.linkLibrariesInBytecode(artifact, libraryAddresses);
            return MultiplexFeatureContract.deployAsync(bytecode, abi, provider, txDefaults, logDecodeDependenciesAbiOnly, zeroExAddress, weth, sandbox, uniswapFactory, sushiswapFactory, uniswapPairInitCodeHash, sushiswapPairInitCodeHash);
        });
    }
    static deployAsync(bytecode, abi, supportedProvider, txDefaults, logDecodeDependencies, zeroExAddress, weth, sandbox, uniswapFactory, sushiswapFactory, uniswapPairInitCodeHash, sushiswapPairInitCodeHash) {
        return __awaiter(this, void 0, void 0, function* () {
            assert_1.assert.isHexString('bytecode', bytecode);
            assert_1.assert.doesConformToSchema('txDefaults', txDefaults, json_schemas_1.schemas.txDataSchema);
            const provider = utils_1.providerUtils.standardizeOrThrow(supportedProvider);
            const constructorAbi = base_contract_1.BaseContract._lookupConstructorAbi(abi);
            [zeroExAddress,
                weth,
                sandbox,
                uniswapFactory,
                sushiswapFactory,
                uniswapPairInitCodeHash,
                sushiswapPairInitCodeHash
            ] = base_contract_1.BaseContract._formatABIDataItemList(constructorAbi.inputs, [zeroExAddress,
                weth,
                sandbox,
                uniswapFactory,
                sushiswapFactory,
                uniswapPairInitCodeHash,
                sushiswapPairInitCodeHash
            ], base_contract_1.BaseContract._bigNumberToString);
            const iface = new ethers.utils.Interface(abi);
            const deployInfo = iface.deployFunction;
            const txData = deployInfo.encode(bytecode, [zeroExAddress,
                weth,
                sandbox,
                uniswapFactory,
                sushiswapFactory,
                uniswapPairInitCodeHash,
                sushiswapPairInitCodeHash
            ]);
            const web3Wrapper = new web3_wrapper_1.Web3Wrapper(provider);
            const txDataWithDefaults = yield base_contract_1.BaseContract._applyDefaultsToContractTxDataAsync(Object.assign({ data: txData }, txDefaults), web3Wrapper.estimateGasAsync.bind(web3Wrapper));
            const txHash = yield web3Wrapper.sendTransactionAsync(txDataWithDefaults);
            utils_1.logUtils.log(`transactionHash: ${txHash}`);
            const txReceipt = yield web3Wrapper.awaitTransactionSuccessAsync(txHash);
            utils_1.logUtils.log(`MultiplexFeature successfully deployed at ${txReceipt.contractAddress}`);
            const contractInstance = new MultiplexFeatureContract(txReceipt.contractAddress, provider, txDefaults, logDecodeDependencies);
            contractInstance.constructorArgs = [zeroExAddress,
                weth,
                sandbox,
                uniswapFactory,
                sushiswapFactory,
                uniswapPairInitCodeHash,
                sushiswapPairInitCodeHash
            ];
            return contractInstance;
        });
    }
    /**
     * @returns      The contract ABI
     */
    static ABI() {
        const abi = [
            {
                inputs: [
                    {
                        name: 'zeroExAddress',
                        type: 'address',
                    },
                    {
                        name: 'weth',
                        type: 'address',
                    },
                    {
                        name: 'sandbox',
                        type: 'address',
                    },
                    {
                        name: 'uniswapFactory',
                        type: 'address',
                    },
                    {
                        name: 'sushiswapFactory',
                        type: 'address',
                    },
                    {
                        name: 'uniswapPairInitCodeHash',
                        type: 'bytes32',
                    },
                    {
                        name: 'sushiswapPairInitCodeHash',
                        type: 'bytes32',
                    },
                ],
                outputs: [],
                stateMutability: 'nonpayable',
                type: 'constructor',
            },
            {
                anonymous: false,
                inputs: [
                    {
                        name: 'orderHash',
                        type: 'bytes32',
                        indexed: false,
                    },
                    {
                        name: 'maker',
                        type: 'address',
                        indexed: false,
                    },
                    {
                        name: 'expiry',
                        type: 'uint64',
                        indexed: false,
                    },
                ],
                name: 'ExpiredOtcOrder',
                outputs: [],
                type: 'event',
            },
            {
                anonymous: false,
                inputs: [
                    {
                        name: 'orderHash',
                        type: 'bytes32',
                        indexed: false,
                    },
                    {
                        name: 'maker',
                        type: 'address',
                        indexed: false,
                    },
                    {
                        name: 'expiry',
                        type: 'uint64',
                        indexed: false,
                    },
                ],
                name: 'ExpiredRfqOrder',
                outputs: [],
                type: 'event',
            },
            {
                anonymous: false,
                inputs: [
                    {
                        name: 'inputToken',
                        type: 'address',
                        indexed: false,
                    },
                    {
                        name: 'outputToken',
                        type: 'address',
                        indexed: false,
                    },
                    {
                        name: 'inputTokenAmount',
                        type: 'uint256',
                        indexed: false,
                    },
                    {
                        name: 'outputTokenAmount',
                        type: 'uint256',
                        indexed: false,
                    },
                    {
                        name: 'provider',
                        type: 'address',
                        indexed: false,
                    },
                    {
                        name: 'recipient',
                        type: 'address',
                        indexed: false,
                    },
                ],
                name: 'LiquidityProviderSwap',
                outputs: [],
                type: 'event',
            },
            {
                inputs: [],
                name: 'EIP712_DOMAIN_SEPARATOR',
                outputs: [
                    {
                        name: '',
                        type: 'bytes32',
                    },
                ],
                stateMutability: 'view',
                type: 'function',
            },
            {
                inputs: [],
                name: 'FEATURE_NAME',
                outputs: [
                    {
                        name: '',
                        type: 'string',
                    },
                ],
                stateMutability: 'view',
                type: 'function',
            },
            {
                inputs: [],
                name: 'FEATURE_VERSION',
                outputs: [
                    {
                        name: '',
                        type: 'uint256',
                    },
                ],
                stateMutability: 'view',
                type: 'function',
            },
            {
                inputs: [
                    {
                        name: 'params',
                        type: 'tuple',
                        components: [
                            {
                                name: 'inputToken',
                                type: 'address',
                            },
                            {
                                name: 'outputToken',
                                type: 'address',
                            },
                            {
                                name: 'sellAmount',
                                type: 'uint256',
                            },
                            {
                                name: 'calls',
                                type: 'tuple[]',
                                components: [
                                    {
                                        name: 'id',
                                        type: 'uint8',
                                    },
                                    {
                                        name: 'sellAmount',
                                        type: 'uint256',
                                    },
                                    {
                                        name: 'data',
                                        type: 'bytes',
                                    },
                                ]
                            },
                            {
                                name: 'useSelfBalance',
                                type: 'bool',
                            },
                            {
                                name: 'recipient',
                                type: 'address',
                            },
                        ]
                    },
                    {
                        name: 'wrappedCallData',
                        type: 'bytes',
                    },
                    {
                        name: 'sellAmount',
                        type: 'uint256',
                    },
                ],
                name: '_batchSellLiquidityProviderExternal',
                outputs: [
                    {
                        name: 'boughtAmount',
                        type: 'uint256',
                    },
                ],
                stateMutability: 'payable',
                type: 'function',
            },
            {
                inputs: [
                    {
                        name: 'params',
                        type: 'tuple',
                        components: [
                            {
                                name: 'inputToken',
                                type: 'address',
                            },
                            {
                                name: 'outputToken',
                                type: 'address',
                            },
                            {
                                name: 'sellAmount',
                                type: 'uint256',
                            },
                            {
                                name: 'calls',
                                type: 'tuple[]',
                                components: [
                                    {
                                        name: 'id',
                                        type: 'uint8',
                                    },
                                    {
                                        name: 'sellAmount',
                                        type: 'uint256',
                                    },
                                    {
                                        name: 'data',
                                        type: 'bytes',
                                    },
                                ]
                            },
                            {
                                name: 'useSelfBalance',
                                type: 'bool',
                            },
                            {
                                name: 'recipient',
                                type: 'address',
                            },
                        ]
                    },
                    {
                        name: 'wrappedCallData',
                        type: 'bytes',
                    },
                    {
                        name: 'sellAmount',
                        type: 'uint256',
                    },
                ],
                name: '_batchSellUniswapV2External',
                outputs: [
                    {
                        name: 'boughtAmount',
                        type: 'uint256',
                    },
                ],
                stateMutability: 'payable',
                type: 'function',
            },
            {
                inputs: [],
                name: 'migrate',
                outputs: [
                    {
                        name: 'success',
                        type: 'bytes4',
                    },
                ],
                stateMutability: 'nonpayable',
                type: 'function',
            },
            {
                inputs: [
                    {
                        name: 'outputToken',
                        type: 'address',
                    },
                    {
                        name: 'calls',
                        type: 'tuple[]',
                        components: [
                            {
                                name: 'id',
                                type: 'uint8',
                            },
                            {
                                name: 'sellAmount',
                                type: 'uint256',
                            },
                            {
                                name: 'data',
                                type: 'bytes',
                            },
                        ]
                    },
                    {
                        name: 'minBuyAmount',
                        type: 'uint256',
                    },
                ],
                name: 'multiplexBatchSellEthForToken',
                outputs: [
                    {
                        name: 'boughtAmount',
                        type: 'uint256',
                    },
                ],
                stateMutability: 'payable',
                type: 'function',
            },
            {
                inputs: [
                    {
                        name: 'inputToken',
                        type: 'address',
                    },
                    {
                        name: 'calls',
                        type: 'tuple[]',
                        components: [
                            {
                                name: 'id',
                                type: 'uint8',
                            },
                            {
                                name: 'sellAmount',
                                type: 'uint256',
                            },
                            {
                                name: 'data',
                                type: 'bytes',
                            },
                        ]
                    },
                    {
                        name: 'sellAmount',
                        type: 'uint256',
                    },
                    {
                        name: 'minBuyAmount',
                        type: 'uint256',
                    },
                ],
                name: 'multiplexBatchSellTokenForEth',
                outputs: [
                    {
                        name: 'boughtAmount',
                        type: 'uint256',
                    },
                ],
                stateMutability: 'nonpayable',
                type: 'function',
            },
            {
                inputs: [
                    {
                        name: 'inputToken',
                        type: 'address',
                    },
                    {
                        name: 'outputToken',
                        type: 'address',
                    },
                    {
                        name: 'calls',
                        type: 'tuple[]',
                        components: [
                            {
                                name: 'id',
                                type: 'uint8',
                            },
                            {
                                name: 'sellAmount',
                                type: 'uint256',
                            },
                            {
                                name: 'data',
                                type: 'bytes',
                            },
                        ]
                    },
                    {
                        name: 'sellAmount',
                        type: 'uint256',
                    },
                    {
                        name: 'minBuyAmount',
                        type: 'uint256',
                    },
                ],
                name: 'multiplexBatchSellTokenForToken',
                outputs: [
                    {
                        name: 'boughtAmount',
                        type: 'uint256',
                    },
                ],
                stateMutability: 'nonpayable',
                type: 'function',
            },
            {
                inputs: [
                    {
                        name: 'tokens',
                        type: 'address[]',
                    },
                    {
                        name: 'calls',
                        type: 'tuple[]',
                        components: [
                            {
                                name: 'id',
                                type: 'uint8',
                            },
                            {
                                name: 'data',
                                type: 'bytes',
                            },
                        ]
                    },
                    {
                        name: 'minBuyAmount',
                        type: 'uint256',
                    },
                ],
                name: 'multiplexMultiHopSellEthForToken',
                outputs: [
                    {
                        name: 'boughtAmount',
                        type: 'uint256',
                    },
                ],
                stateMutability: 'payable',
                type: 'function',
            },
            {
                inputs: [
                    {
                        name: 'tokens',
                        type: 'address[]',
                    },
                    {
                        name: 'calls',
                        type: 'tuple[]',
                        components: [
                            {
                                name: 'id',
                                type: 'uint8',
                            },
                            {
                                name: 'data',
                                type: 'bytes',
                            },
                        ]
                    },
                    {
                        name: 'sellAmount',
                        type: 'uint256',
                    },
                    {
                        name: 'minBuyAmount',
                        type: 'uint256',
                    },
                ],
                name: 'multiplexMultiHopSellTokenForEth',
                outputs: [
                    {
                        name: 'boughtAmount',
                        type: 'uint256',
                    },
                ],
                stateMutability: 'nonpayable',
                type: 'function',
            },
            {
                inputs: [
                    {
                        name: 'tokens',
                        type: 'address[]',
                    },
                    {
                        name: 'calls',
                        type: 'tuple[]',
                        components: [
                            {
                                name: 'id',
                                type: 'uint8',
                            },
                            {
                                name: 'data',
                                type: 'bytes',
                            },
                        ]
                    },
                    {
                        name: 'sellAmount',
                        type: 'uint256',
                    },
                    {
                        name: 'minBuyAmount',
                        type: 'uint256',
                    },
                ],
                name: 'multiplexMultiHopSellTokenForToken',
                outputs: [
                    {
                        name: 'boughtAmount',
                        type: 'uint256',
                    },
                ],
                stateMutability: 'nonpayable',
                type: 'function',
            },
        ];
        return abi;
    }
    static _deployLibrariesAsync(artifact, libraryArtifacts, web3Wrapper, txDefaults, libraryAddresses = {}) {
        return __awaiter(this, void 0, void 0, function* () {
            const links = artifact.compilerOutput.evm.bytecode.linkReferences;
            // Go through all linked libraries, recursively deploying them if necessary.
            for (const link of Object.values(links)) {
                for (const libraryName of Object.keys(link)) {
                    if (!libraryAddresses[libraryName]) {
                        // Library not yet deployed.
                        const libraryArtifact = libraryArtifacts[libraryName];
                        if (!libraryArtifact) {
                            throw new Error(`Missing artifact for linked library "${libraryName}"`);
                        }
                        // Deploy any dependent libraries used by this library.
                        yield MultiplexFeatureContract._deployLibrariesAsync(libraryArtifact, libraryArtifacts, web3Wrapper, txDefaults, libraryAddresses);
                        // Deploy this library.
                        const linkedLibraryBytecode = base_contract_1.linkLibrariesInBytecode(libraryArtifact, libraryAddresses);
                        const txDataWithDefaults = yield base_contract_1.BaseContract._applyDefaultsToContractTxDataAsync(Object.assign({ data: linkedLibraryBytecode }, txDefaults), web3Wrapper.estimateGasAsync.bind(web3Wrapper));
                        const txHash = yield web3Wrapper.sendTransactionAsync(txDataWithDefaults);
                        utils_1.logUtils.log(`transactionHash: ${txHash}`);
                        const { contractAddress } = yield web3Wrapper.awaitTransactionSuccessAsync(txHash);
                        utils_1.logUtils.log(`${libraryArtifact.contractName} successfully deployed at ${contractAddress}`);
                        libraryAddresses[libraryArtifact.contractName] = contractAddress;
                    }
                }
            }
            return libraryAddresses;
        });
    }
    getFunctionSignature(methodName) {
        const index = this._methodABIIndex[methodName];
        const methodAbi = MultiplexFeatureContract.ABI()[index]; // tslint:disable-line:no-unnecessary-type-assertion
        const functionSignature = base_contract_1.methodAbiToFunctionSignature(methodAbi);
        return functionSignature;
    }
    getABIDecodedTransactionData(methodName, callData) {
        const functionSignature = this.getFunctionSignature(methodName);
        const self = this;
        const abiEncoder = self._lookupAbiEncoder(functionSignature);
        const abiDecodedCallData = abiEncoder.strictDecode(callData);
        return abiDecodedCallData;
    }
    getABIDecodedReturnData(methodName, callData) {
        if (this._encoderOverrides.decodeOutput) {
            return this._encoderOverrides.decodeOutput(methodName, callData);
        }
        const functionSignature = this.getFunctionSignature(methodName);
        const self = this;
        const abiEncoder = self._lookupAbiEncoder(functionSignature);
        const abiDecodedCallData = abiEncoder.strictDecodeReturnValue(callData);
        return abiDecodedCallData;
    }
    getSelector(methodName) {
        const functionSignature = this.getFunctionSignature(methodName);
        const self = this;
        const abiEncoder = self._lookupAbiEncoder(functionSignature);
        return abiEncoder.getSelector();
    }
    EIP712_DOMAIN_SEPARATOR() {
        const self = this;
        const functionSignature = 'EIP712_DOMAIN_SEPARATOR()';
        return {
            sendTransactionAsync(txData, opts = { shouldValidate: true }) {
                return __awaiter(this, void 0, void 0, function* () {
                    const txDataWithDefaults = yield self._applyDefaultsToTxDataAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, txData), this.estimateGasAsync.bind(this));
                    if (opts.shouldValidate !== false) {
                        yield this.callAsync(txDataWithDefaults);
                    }
                    return self._web3Wrapper.sendTransactionAsync(txDataWithDefaults);
                });
            },
            awaitTransactionSuccessAsync(txData, opts = { shouldValidate: true }) {
                return self._promiseWithTransactionHash(this.sendTransactionAsync(txData, opts), opts);
            },
            estimateGasAsync(txData) {
                return __awaiter(this, void 0, void 0, function* () {
                    const txDataWithDefaults = yield self._applyDefaultsToTxDataAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, txData));
                    return self._web3Wrapper.estimateGasAsync(txDataWithDefaults);
                });
            },
            createAccessListAsync(txData, defaultBlock) {
                return __awaiter(this, void 0, void 0, function* () {
                    const txDataWithDefaults = yield self._applyDefaultsToTxDataAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, txData));
                    return self._web3Wrapper.createAccessListAsync(txDataWithDefaults, defaultBlock);
                });
            },
            callAsync(callData = {}, defaultBlock) {
                return __awaiter(this, void 0, void 0, function* () {
                    base_contract_1.BaseContract._assertCallParams(callData, defaultBlock);
                    const rawCallResult = yield self._performCallAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, callData), defaultBlock);
                    const abiEncoder = self._lookupAbiEncoder(functionSignature);
                    base_contract_1.BaseContract._throwIfUnexpectedEmptyCallResult(rawCallResult, abiEncoder);
                    return abiEncoder.strictDecodeReturnValue(rawCallResult);
                });
            },
            getABIEncodedTransactionData() {
                return self._strictEncodeArguments(functionSignature, []);
            },
        };
    }
    ;
    FEATURE_NAME() {
        const self = this;
        const functionSignature = 'FEATURE_NAME()';
        return {
            sendTransactionAsync(txData, opts = { shouldValidate: true }) {
                return __awaiter(this, void 0, void 0, function* () {
                    const txDataWithDefaults = yield self._applyDefaultsToTxDataAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, txData), this.estimateGasAsync.bind(this));
                    if (opts.shouldValidate !== false) {
                        yield this.callAsync(txDataWithDefaults);
                    }
                    return self._web3Wrapper.sendTransactionAsync(txDataWithDefaults);
                });
            },
            awaitTransactionSuccessAsync(txData, opts = { shouldValidate: true }) {
                return self._promiseWithTransactionHash(this.sendTransactionAsync(txData, opts), opts);
            },
            estimateGasAsync(txData) {
                return __awaiter(this, void 0, void 0, function* () {
                    const txDataWithDefaults = yield self._applyDefaultsToTxDataAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, txData));
                    return self._web3Wrapper.estimateGasAsync(txDataWithDefaults);
                });
            },
            createAccessListAsync(txData, defaultBlock) {
                return __awaiter(this, void 0, void 0, function* () {
                    const txDataWithDefaults = yield self._applyDefaultsToTxDataAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, txData));
                    return self._web3Wrapper.createAccessListAsync(txDataWithDefaults, defaultBlock);
                });
            },
            callAsync(callData = {}, defaultBlock) {
                return __awaiter(this, void 0, void 0, function* () {
                    base_contract_1.BaseContract._assertCallParams(callData, defaultBlock);
                    const rawCallResult = yield self._performCallAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, callData), defaultBlock);
                    const abiEncoder = self._lookupAbiEncoder(functionSignature);
                    base_contract_1.BaseContract._throwIfUnexpectedEmptyCallResult(rawCallResult, abiEncoder);
                    return abiEncoder.strictDecodeReturnValue(rawCallResult);
                });
            },
            getABIEncodedTransactionData() {
                return self._strictEncodeArguments(functionSignature, []);
            },
        };
    }
    ;
    FEATURE_VERSION() {
        const self = this;
        const functionSignature = 'FEATURE_VERSION()';
        return {
            sendTransactionAsync(txData, opts = { shouldValidate: true }) {
                return __awaiter(this, void 0, void 0, function* () {
                    const txDataWithDefaults = yield self._applyDefaultsToTxDataAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, txData), this.estimateGasAsync.bind(this));
                    if (opts.shouldValidate !== false) {
                        yield this.callAsync(txDataWithDefaults);
                    }
                    return self._web3Wrapper.sendTransactionAsync(txDataWithDefaults);
                });
            },
            awaitTransactionSuccessAsync(txData, opts = { shouldValidate: true }) {
                return self._promiseWithTransactionHash(this.sendTransactionAsync(txData, opts), opts);
            },
            estimateGasAsync(txData) {
                return __awaiter(this, void 0, void 0, function* () {
                    const txDataWithDefaults = yield self._applyDefaultsToTxDataAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, txData));
                    return self._web3Wrapper.estimateGasAsync(txDataWithDefaults);
                });
            },
            createAccessListAsync(txData, defaultBlock) {
                return __awaiter(this, void 0, void 0, function* () {
                    const txDataWithDefaults = yield self._applyDefaultsToTxDataAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, txData));
                    return self._web3Wrapper.createAccessListAsync(txDataWithDefaults, defaultBlock);
                });
            },
            callAsync(callData = {}, defaultBlock) {
                return __awaiter(this, void 0, void 0, function* () {
                    base_contract_1.BaseContract._assertCallParams(callData, defaultBlock);
                    const rawCallResult = yield self._performCallAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, callData), defaultBlock);
                    const abiEncoder = self._lookupAbiEncoder(functionSignature);
                    base_contract_1.BaseContract._throwIfUnexpectedEmptyCallResult(rawCallResult, abiEncoder);
                    return abiEncoder.strictDecodeReturnValue(rawCallResult);
                });
            },
            getABIEncodedTransactionData() {
                return self._strictEncodeArguments(functionSignature, []);
            },
        };
    }
    ;
    _batchSellLiquidityProviderExternal(params, wrappedCallData, sellAmount) {
        const self = this;
        assert_1.assert.isString('wrappedCallData', wrappedCallData);
        assert_1.assert.isBigNumber('sellAmount', sellAmount);
        const functionSignature = '_batchSellLiquidityProviderExternal((address,address,uint256,(uint8,uint256,bytes)[],bool,address),bytes,uint256)';
        return {
            sendTransactionAsync(txData, opts = { shouldValidate: true }) {
                return __awaiter(this, void 0, void 0, function* () {
                    const txDataWithDefaults = yield self._applyDefaultsToTxDataAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, txData), this.estimateGasAsync.bind(this));
                    if (opts.shouldValidate !== false) {
                        yield this.callAsync(txDataWithDefaults);
                    }
                    return self._web3Wrapper.sendTransactionAsync(txDataWithDefaults);
                });
            },
            awaitTransactionSuccessAsync(txData, opts = { shouldValidate: true }) {
                return self._promiseWithTransactionHash(this.sendTransactionAsync(txData, opts), opts);
            },
            estimateGasAsync(txData) {
                return __awaiter(this, void 0, void 0, function* () {
                    const txDataWithDefaults = yield self._applyDefaultsToTxDataAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, txData));
                    return self._web3Wrapper.estimateGasAsync(txDataWithDefaults);
                });
            },
            createAccessListAsync(txData, defaultBlock) {
                return __awaiter(this, void 0, void 0, function* () {
                    const txDataWithDefaults = yield self._applyDefaultsToTxDataAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, txData));
                    return self._web3Wrapper.createAccessListAsync(txDataWithDefaults, defaultBlock);
                });
            },
            callAsync(callData = {}, defaultBlock) {
                return __awaiter(this, void 0, void 0, function* () {
                    base_contract_1.BaseContract._assertCallParams(callData, defaultBlock);
                    const rawCallResult = yield self._performCallAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, callData), defaultBlock);
                    const abiEncoder = self._lookupAbiEncoder(functionSignature);
                    base_contract_1.BaseContract._throwIfUnexpectedEmptyCallResult(rawCallResult, abiEncoder);
                    return abiEncoder.strictDecodeReturnValue(rawCallResult);
                });
            },
            getABIEncodedTransactionData() {
                return self._strictEncodeArguments(functionSignature, [params,
                    wrappedCallData,
                    sellAmount
                ]);
            },
        };
    }
    ;
    _batchSellUniswapV2External(params, wrappedCallData, sellAmount) {
        const self = this;
        assert_1.assert.isString('wrappedCallData', wrappedCallData);
        assert_1.assert.isBigNumber('sellAmount', sellAmount);
        const functionSignature = '_batchSellUniswapV2External((address,address,uint256,(uint8,uint256,bytes)[],bool,address),bytes,uint256)';
        return {
            sendTransactionAsync(txData, opts = { shouldValidate: true }) {
                return __awaiter(this, void 0, void 0, function* () {
                    const txDataWithDefaults = yield self._applyDefaultsToTxDataAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, txData), this.estimateGasAsync.bind(this));
                    if (opts.shouldValidate !== false) {
                        yield this.callAsync(txDataWithDefaults);
                    }
                    return self._web3Wrapper.sendTransactionAsync(txDataWithDefaults);
                });
            },
            awaitTransactionSuccessAsync(txData, opts = { shouldValidate: true }) {
                return self._promiseWithTransactionHash(this.sendTransactionAsync(txData, opts), opts);
            },
            estimateGasAsync(txData) {
                return __awaiter(this, void 0, void 0, function* () {
                    const txDataWithDefaults = yield self._applyDefaultsToTxDataAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, txData));
                    return self._web3Wrapper.estimateGasAsync(txDataWithDefaults);
                });
            },
            createAccessListAsync(txData, defaultBlock) {
                return __awaiter(this, void 0, void 0, function* () {
                    const txDataWithDefaults = yield self._applyDefaultsToTxDataAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, txData));
                    return self._web3Wrapper.createAccessListAsync(txDataWithDefaults, defaultBlock);
                });
            },
            callAsync(callData = {}, defaultBlock) {
                return __awaiter(this, void 0, void 0, function* () {
                    base_contract_1.BaseContract._assertCallParams(callData, defaultBlock);
                    const rawCallResult = yield self._performCallAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, callData), defaultBlock);
                    const abiEncoder = self._lookupAbiEncoder(functionSignature);
                    base_contract_1.BaseContract._throwIfUnexpectedEmptyCallResult(rawCallResult, abiEncoder);
                    return abiEncoder.strictDecodeReturnValue(rawCallResult);
                });
            },
            getABIEncodedTransactionData() {
                return self._strictEncodeArguments(functionSignature, [params,
                    wrappedCallData,
                    sellAmount
                ]);
            },
        };
    }
    ;
    /**
     * Initialize and register this feature.
 * Should be delegatecalled by `Migrate.migrate()`.
     */
    migrate() {
        const self = this;
        const functionSignature = 'migrate()';
        return {
            sendTransactionAsync(txData, opts = { shouldValidate: true }) {
                return __awaiter(this, void 0, void 0, function* () {
                    const txDataWithDefaults = yield self._applyDefaultsToTxDataAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, txData), this.estimateGasAsync.bind(this));
                    if (opts.shouldValidate !== false) {
                        yield this.callAsync(txDataWithDefaults);
                    }
                    return self._web3Wrapper.sendTransactionAsync(txDataWithDefaults);
                });
            },
            awaitTransactionSuccessAsync(txData, opts = { shouldValidate: true }) {
                return self._promiseWithTransactionHash(this.sendTransactionAsync(txData, opts), opts);
            },
            estimateGasAsync(txData) {
                return __awaiter(this, void 0, void 0, function* () {
                    const txDataWithDefaults = yield self._applyDefaultsToTxDataAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, txData));
                    return self._web3Wrapper.estimateGasAsync(txDataWithDefaults);
                });
            },
            createAccessListAsync(txData, defaultBlock) {
                return __awaiter(this, void 0, void 0, function* () {
                    const txDataWithDefaults = yield self._applyDefaultsToTxDataAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, txData));
                    return self._web3Wrapper.createAccessListAsync(txDataWithDefaults, defaultBlock);
                });
            },
            callAsync(callData = {}, defaultBlock) {
                return __awaiter(this, void 0, void 0, function* () {
                    base_contract_1.BaseContract._assertCallParams(callData, defaultBlock);
                    const rawCallResult = yield self._performCallAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, callData), defaultBlock);
                    const abiEncoder = self._lookupAbiEncoder(functionSignature);
                    base_contract_1.BaseContract._throwIfUnexpectedEmptyCallResult(rawCallResult, abiEncoder);
                    return abiEncoder.strictDecodeReturnValue(rawCallResult);
                });
            },
            getABIEncodedTransactionData() {
                return self._strictEncodeArguments(functionSignature, []);
            },
        };
    }
    ;
    /**
     * Sells attached ETH for `outputToken` using the provided
 * calls.
      * @param outputToken The token to buy.
      * @param calls The calls to use to sell the attached ETH.
      * @param minBuyAmount The minimum amount of `outputToken` that        must be
     *     bought for this function to not revert.
     */
    multiplexBatchSellEthForToken(outputToken, calls, minBuyAmount) {
        const self = this;
        assert_1.assert.isString('outputToken', outputToken);
        assert_1.assert.isArray('calls', calls);
        assert_1.assert.isBigNumber('minBuyAmount', minBuyAmount);
        const functionSignature = 'multiplexBatchSellEthForToken(address,(uint8,uint256,bytes)[],uint256)';
        return {
            sendTransactionAsync(txData, opts = { shouldValidate: true }) {
                return __awaiter(this, void 0, void 0, function* () {
                    const txDataWithDefaults = yield self._applyDefaultsToTxDataAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, txData), this.estimateGasAsync.bind(this));
                    if (opts.shouldValidate !== false) {
                        yield this.callAsync(txDataWithDefaults);
                    }
                    return self._web3Wrapper.sendTransactionAsync(txDataWithDefaults);
                });
            },
            awaitTransactionSuccessAsync(txData, opts = { shouldValidate: true }) {
                return self._promiseWithTransactionHash(this.sendTransactionAsync(txData, opts), opts);
            },
            estimateGasAsync(txData) {
                return __awaiter(this, void 0, void 0, function* () {
                    const txDataWithDefaults = yield self._applyDefaultsToTxDataAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, txData));
                    return self._web3Wrapper.estimateGasAsync(txDataWithDefaults);
                });
            },
            createAccessListAsync(txData, defaultBlock) {
                return __awaiter(this, void 0, void 0, function* () {
                    const txDataWithDefaults = yield self._applyDefaultsToTxDataAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, txData));
                    return self._web3Wrapper.createAccessListAsync(txDataWithDefaults, defaultBlock);
                });
            },
            callAsync(callData = {}, defaultBlock) {
                return __awaiter(this, void 0, void 0, function* () {
                    base_contract_1.BaseContract._assertCallParams(callData, defaultBlock);
                    const rawCallResult = yield self._performCallAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, callData), defaultBlock);
                    const abiEncoder = self._lookupAbiEncoder(functionSignature);
                    base_contract_1.BaseContract._throwIfUnexpectedEmptyCallResult(rawCallResult, abiEncoder);
                    return abiEncoder.strictDecodeReturnValue(rawCallResult);
                });
            },
            getABIEncodedTransactionData() {
                return self._strictEncodeArguments(functionSignature, [outputToken.toLowerCase(),
                    calls,
                    minBuyAmount
                ]);
            },
        };
    }
    ;
    /**
     * Sells `sellAmount` of the given `inputToken` for ETH
 * using the provided calls.
      * @param inputToken The token to sell.
      * @param calls The calls to use to sell the input tokens.
      * @param sellAmount The amount of `inputToken` to sell.
      * @param minBuyAmount The minimum amount of ETH that        must be bought for
     *     this function to not revert.
     */
    multiplexBatchSellTokenForEth(inputToken, calls, sellAmount, minBuyAmount) {
        const self = this;
        assert_1.assert.isString('inputToken', inputToken);
        assert_1.assert.isArray('calls', calls);
        assert_1.assert.isBigNumber('sellAmount', sellAmount);
        assert_1.assert.isBigNumber('minBuyAmount', minBuyAmount);
        const functionSignature = 'multiplexBatchSellTokenForEth(address,(uint8,uint256,bytes)[],uint256,uint256)';
        return {
            sendTransactionAsync(txData, opts = { shouldValidate: true }) {
                return __awaiter(this, void 0, void 0, function* () {
                    const txDataWithDefaults = yield self._applyDefaultsToTxDataAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, txData), this.estimateGasAsync.bind(this));
                    if (opts.shouldValidate !== false) {
                        yield this.callAsync(txDataWithDefaults);
                    }
                    return self._web3Wrapper.sendTransactionAsync(txDataWithDefaults);
                });
            },
            awaitTransactionSuccessAsync(txData, opts = { shouldValidate: true }) {
                return self._promiseWithTransactionHash(this.sendTransactionAsync(txData, opts), opts);
            },
            estimateGasAsync(txData) {
                return __awaiter(this, void 0, void 0, function* () {
                    const txDataWithDefaults = yield self._applyDefaultsToTxDataAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, txData));
                    return self._web3Wrapper.estimateGasAsync(txDataWithDefaults);
                });
            },
            createAccessListAsync(txData, defaultBlock) {
                return __awaiter(this, void 0, void 0, function* () {
                    const txDataWithDefaults = yield self._applyDefaultsToTxDataAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, txData));
                    return self._web3Wrapper.createAccessListAsync(txDataWithDefaults, defaultBlock);
                });
            },
            callAsync(callData = {}, defaultBlock) {
                return __awaiter(this, void 0, void 0, function* () {
                    base_contract_1.BaseContract._assertCallParams(callData, defaultBlock);
                    const rawCallResult = yield self._performCallAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, callData), defaultBlock);
                    const abiEncoder = self._lookupAbiEncoder(functionSignature);
                    base_contract_1.BaseContract._throwIfUnexpectedEmptyCallResult(rawCallResult, abiEncoder);
                    return abiEncoder.strictDecodeReturnValue(rawCallResult);
                });
            },
            getABIEncodedTransactionData() {
                return self._strictEncodeArguments(functionSignature, [inputToken.toLowerCase(),
                    calls,
                    sellAmount,
                    minBuyAmount
                ]);
            },
        };
    }
    ;
    /**
     * Sells `sellAmount` of the given `inputToken` for
 * `outputToken` using the provided calls.
      * @param inputToken The token to sell.
      * @param outputToken The token to buy.
      * @param calls The calls to use to sell the input tokens.
      * @param sellAmount The amount of `inputToken` to sell.
      * @param minBuyAmount The minimum amount of `outputToken`        that must be
     *     bought for this function to not revert.
     */
    multiplexBatchSellTokenForToken(inputToken, outputToken, calls, sellAmount, minBuyAmount) {
        const self = this;
        assert_1.assert.isString('inputToken', inputToken);
        assert_1.assert.isString('outputToken', outputToken);
        assert_1.assert.isArray('calls', calls);
        assert_1.assert.isBigNumber('sellAmount', sellAmount);
        assert_1.assert.isBigNumber('minBuyAmount', minBuyAmount);
        const functionSignature = 'multiplexBatchSellTokenForToken(address,address,(uint8,uint256,bytes)[],uint256,uint256)';
        return {
            sendTransactionAsync(txData, opts = { shouldValidate: true }) {
                return __awaiter(this, void 0, void 0, function* () {
                    const txDataWithDefaults = yield self._applyDefaultsToTxDataAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, txData), this.estimateGasAsync.bind(this));
                    if (opts.shouldValidate !== false) {
                        yield this.callAsync(txDataWithDefaults);
                    }
                    return self._web3Wrapper.sendTransactionAsync(txDataWithDefaults);
                });
            },
            awaitTransactionSuccessAsync(txData, opts = { shouldValidate: true }) {
                return self._promiseWithTransactionHash(this.sendTransactionAsync(txData, opts), opts);
            },
            estimateGasAsync(txData) {
                return __awaiter(this, void 0, void 0, function* () {
                    const txDataWithDefaults = yield self._applyDefaultsToTxDataAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, txData));
                    return self._web3Wrapper.estimateGasAsync(txDataWithDefaults);
                });
            },
            createAccessListAsync(txData, defaultBlock) {
                return __awaiter(this, void 0, void 0, function* () {
                    const txDataWithDefaults = yield self._applyDefaultsToTxDataAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, txData));
                    return self._web3Wrapper.createAccessListAsync(txDataWithDefaults, defaultBlock);
                });
            },
            callAsync(callData = {}, defaultBlock) {
                return __awaiter(this, void 0, void 0, function* () {
                    base_contract_1.BaseContract._assertCallParams(callData, defaultBlock);
                    const rawCallResult = yield self._performCallAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, callData), defaultBlock);
                    const abiEncoder = self._lookupAbiEncoder(functionSignature);
                    base_contract_1.BaseContract._throwIfUnexpectedEmptyCallResult(rawCallResult, abiEncoder);
                    return abiEncoder.strictDecodeReturnValue(rawCallResult);
                });
            },
            getABIEncodedTransactionData() {
                return self._strictEncodeArguments(functionSignature, [inputToken.toLowerCase(),
                    outputToken.toLowerCase(),
                    calls,
                    sellAmount,
                    minBuyAmount
                ]);
            },
        };
    }
    ;
    /**
     * Sells attached ETH via the given sequence of tokens
 * and calls. `tokens[0]` must be WETH.
 * The last token in `tokens` is the output token that
 * will ultimately be sent to `msg.sender`
      * @param tokens The sequence of tokens to use for the sell,        i.e.
     *     `tokens[i]` will be sold for `tokens[i+1]` via        `calls[i]`.
      * @param calls The sequence of calls to use for the sell.
      * @param minBuyAmount The minimum amount of output tokens that        must be
     *     bought for this function to not revert.
     */
    multiplexMultiHopSellEthForToken(tokens, calls, minBuyAmount) {
        const self = this;
        assert_1.assert.isArray('tokens', tokens);
        assert_1.assert.isArray('calls', calls);
        assert_1.assert.isBigNumber('minBuyAmount', minBuyAmount);
        const functionSignature = 'multiplexMultiHopSellEthForToken(address[],(uint8,bytes)[],uint256)';
        return {
            sendTransactionAsync(txData, opts = { shouldValidate: true }) {
                return __awaiter(this, void 0, void 0, function* () {
                    const txDataWithDefaults = yield self._applyDefaultsToTxDataAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, txData), this.estimateGasAsync.bind(this));
                    if (opts.shouldValidate !== false) {
                        yield this.callAsync(txDataWithDefaults);
                    }
                    return self._web3Wrapper.sendTransactionAsync(txDataWithDefaults);
                });
            },
            awaitTransactionSuccessAsync(txData, opts = { shouldValidate: true }) {
                return self._promiseWithTransactionHash(this.sendTransactionAsync(txData, opts), opts);
            },
            estimateGasAsync(txData) {
                return __awaiter(this, void 0, void 0, function* () {
                    const txDataWithDefaults = yield self._applyDefaultsToTxDataAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, txData));
                    return self._web3Wrapper.estimateGasAsync(txDataWithDefaults);
                });
            },
            createAccessListAsync(txData, defaultBlock) {
                return __awaiter(this, void 0, void 0, function* () {
                    const txDataWithDefaults = yield self._applyDefaultsToTxDataAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, txData));
                    return self._web3Wrapper.createAccessListAsync(txDataWithDefaults, defaultBlock);
                });
            },
            callAsync(callData = {}, defaultBlock) {
                return __awaiter(this, void 0, void 0, function* () {
                    base_contract_1.BaseContract._assertCallParams(callData, defaultBlock);
                    const rawCallResult = yield self._performCallAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, callData), defaultBlock);
                    const abiEncoder = self._lookupAbiEncoder(functionSignature);
                    base_contract_1.BaseContract._throwIfUnexpectedEmptyCallResult(rawCallResult, abiEncoder);
                    return abiEncoder.strictDecodeReturnValue(rawCallResult);
                });
            },
            getABIEncodedTransactionData() {
                return self._strictEncodeArguments(functionSignature, [tokens,
                    calls,
                    minBuyAmount
                ]);
            },
        };
    }
    ;
    /**
     * Sells `sellAmount` of the input token (`tokens[0]`)
 * for ETH via the given sequence of tokens and calls.
 * The last token in `tokens` must be WETH.
      * @param tokens The sequence of tokens to use for the sell,        i.e.
     *     `tokens[i]` will be sold for `tokens[i+1]` via        `calls[i]`.
      * @param calls The sequence of calls to use for the sell.
      * @param sellAmount The amount of `inputToken` to sell.
      * @param minBuyAmount The minimum amount of ETH that        must be bought for
     *     this function to not revert.
     */
    multiplexMultiHopSellTokenForEth(tokens, calls, sellAmount, minBuyAmount) {
        const self = this;
        assert_1.assert.isArray('tokens', tokens);
        assert_1.assert.isArray('calls', calls);
        assert_1.assert.isBigNumber('sellAmount', sellAmount);
        assert_1.assert.isBigNumber('minBuyAmount', minBuyAmount);
        const functionSignature = 'multiplexMultiHopSellTokenForEth(address[],(uint8,bytes)[],uint256,uint256)';
        return {
            sendTransactionAsync(txData, opts = { shouldValidate: true }) {
                return __awaiter(this, void 0, void 0, function* () {
                    const txDataWithDefaults = yield self._applyDefaultsToTxDataAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, txData), this.estimateGasAsync.bind(this));
                    if (opts.shouldValidate !== false) {
                        yield this.callAsync(txDataWithDefaults);
                    }
                    return self._web3Wrapper.sendTransactionAsync(txDataWithDefaults);
                });
            },
            awaitTransactionSuccessAsync(txData, opts = { shouldValidate: true }) {
                return self._promiseWithTransactionHash(this.sendTransactionAsync(txData, opts), opts);
            },
            estimateGasAsync(txData) {
                return __awaiter(this, void 0, void 0, function* () {
                    const txDataWithDefaults = yield self._applyDefaultsToTxDataAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, txData));
                    return self._web3Wrapper.estimateGasAsync(txDataWithDefaults);
                });
            },
            createAccessListAsync(txData, defaultBlock) {
                return __awaiter(this, void 0, void 0, function* () {
                    const txDataWithDefaults = yield self._applyDefaultsToTxDataAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, txData));
                    return self._web3Wrapper.createAccessListAsync(txDataWithDefaults, defaultBlock);
                });
            },
            callAsync(callData = {}, defaultBlock) {
                return __awaiter(this, void 0, void 0, function* () {
                    base_contract_1.BaseContract._assertCallParams(callData, defaultBlock);
                    const rawCallResult = yield self._performCallAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, callData), defaultBlock);
                    const abiEncoder = self._lookupAbiEncoder(functionSignature);
                    base_contract_1.BaseContract._throwIfUnexpectedEmptyCallResult(rawCallResult, abiEncoder);
                    return abiEncoder.strictDecodeReturnValue(rawCallResult);
                });
            },
            getABIEncodedTransactionData() {
                return self._strictEncodeArguments(functionSignature, [tokens,
                    calls,
                    sellAmount,
                    minBuyAmount
                ]);
            },
        };
    }
    ;
    /**
     * Sells `sellAmount` of the input token (`tokens[0]`)
 * via the given sequence of tokens and calls.
 * The last token in `tokens` is the output token that
 * will ultimately be sent to `msg.sender`
      * @param tokens The sequence of tokens to use for the sell,        i.e.
     *     `tokens[i]` will be sold for `tokens[i+1]` via        `calls[i]`.
      * @param calls The sequence of calls to use for the sell.
      * @param sellAmount The amount of `inputToken` to sell.
      * @param minBuyAmount The minimum amount of output tokens that        must be
     *     bought for this function to not revert.
     */
    multiplexMultiHopSellTokenForToken(tokens, calls, sellAmount, minBuyAmount) {
        const self = this;
        assert_1.assert.isArray('tokens', tokens);
        assert_1.assert.isArray('calls', calls);
        assert_1.assert.isBigNumber('sellAmount', sellAmount);
        assert_1.assert.isBigNumber('minBuyAmount', minBuyAmount);
        const functionSignature = 'multiplexMultiHopSellTokenForToken(address[],(uint8,bytes)[],uint256,uint256)';
        return {
            sendTransactionAsync(txData, opts = { shouldValidate: true }) {
                return __awaiter(this, void 0, void 0, function* () {
                    const txDataWithDefaults = yield self._applyDefaultsToTxDataAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, txData), this.estimateGasAsync.bind(this));
                    if (opts.shouldValidate !== false) {
                        yield this.callAsync(txDataWithDefaults);
                    }
                    return self._web3Wrapper.sendTransactionAsync(txDataWithDefaults);
                });
            },
            awaitTransactionSuccessAsync(txData, opts = { shouldValidate: true }) {
                return self._promiseWithTransactionHash(this.sendTransactionAsync(txData, opts), opts);
            },
            estimateGasAsync(txData) {
                return __awaiter(this, void 0, void 0, function* () {
                    const txDataWithDefaults = yield self._applyDefaultsToTxDataAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, txData));
                    return self._web3Wrapper.estimateGasAsync(txDataWithDefaults);
                });
            },
            createAccessListAsync(txData, defaultBlock) {
                return __awaiter(this, void 0, void 0, function* () {
                    const txDataWithDefaults = yield self._applyDefaultsToTxDataAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, txData));
                    return self._web3Wrapper.createAccessListAsync(txDataWithDefaults, defaultBlock);
                });
            },
            callAsync(callData = {}, defaultBlock) {
                return __awaiter(this, void 0, void 0, function* () {
                    base_contract_1.BaseContract._assertCallParams(callData, defaultBlock);
                    const rawCallResult = yield self._performCallAsync(Object.assign({ data: this.getABIEncodedTransactionData() }, callData), defaultBlock);
                    const abiEncoder = self._lookupAbiEncoder(functionSignature);
                    base_contract_1.BaseContract._throwIfUnexpectedEmptyCallResult(rawCallResult, abiEncoder);
                    return abiEncoder.strictDecodeReturnValue(rawCallResult);
                });
            },
            getABIEncodedTransactionData() {
                return self._strictEncodeArguments(functionSignature, [tokens,
                    calls,
                    sellAmount,
                    minBuyAmount
                ]);
            },
        };
    }
    ;
    /**
     * Subscribe to an event type emitted by the MultiplexFeature contract.
     * @param eventName The MultiplexFeature contract event you would like to subscribe to.
     * @param indexFilterValues An object where the keys are indexed args returned by the event and
     * the value is the value you are interested in. E.g `{maker: aUserAddressHex}`
     * @param callback Callback that gets called when a log is added/removed
     * @param isVerbose Enable verbose subscription warnings (e.g recoverable network issues encountered)
     * @return Subscription token used later to unsubscribe
     */
    subscribe(eventName, indexFilterValues, callback, isVerbose = false, blockPollingIntervalMs) {
        assert_1.assert.doesBelongToStringEnum('eventName', eventName, MultiplexFeatureEvents);
        assert_1.assert.doesConformToSchema('indexFilterValues', indexFilterValues, json_schemas_1.schemas.indexFilterValuesSchema);
        assert_1.assert.isFunction('callback', callback);
        const subscriptionToken = this._subscriptionManager.subscribe(this.address, eventName, indexFilterValues, MultiplexFeatureContract.ABI(), callback, isVerbose, blockPollingIntervalMs);
        return subscriptionToken;
    }
    /**
     * Cancel a subscription
     * @param subscriptionToken Subscription token returned by `subscribe()`
     */
    unsubscribe(subscriptionToken) {
        this._subscriptionManager.unsubscribe(subscriptionToken);
    }
    /**
     * Cancels all existing subscriptions
     */
    unsubscribeAll() {
        this._subscriptionManager.unsubscribeAll();
    }
    /**
     * Gets historical logs without creating a subscription
     * @param eventName The MultiplexFeature contract event you would like to subscribe to.
     * @param blockRange Block range to get logs from.
     * @param indexFilterValues An object where the keys are indexed args returned by the event and
     * the value is the value you are interested in. E.g `{_from: aUserAddressHex}`
     * @return Array of logs that match the parameters
     */
    getLogsAsync(eventName, blockRange, indexFilterValues) {
        return __awaiter(this, void 0, void 0, function* () {
            assert_1.assert.doesBelongToStringEnum('eventName', eventName, MultiplexFeatureEvents);
            assert_1.assert.doesConformToSchema('blockRange', blockRange, json_schemas_1.schemas.blockRangeSchema);
            assert_1.assert.doesConformToSchema('indexFilterValues', indexFilterValues, json_schemas_1.schemas.indexFilterValuesSchema);
            const logs = yield this._subscriptionManager.getLogsAsync(this.address, eventName, blockRange, indexFilterValues, MultiplexFeatureContract.ABI());
            return logs;
        });
    }
}
exports.MultiplexFeatureContract = MultiplexFeatureContract;
MultiplexFeatureContract.contractName = 'MultiplexFeature';
// tslint:disable:max-file-line-count
// tslint:enable:no-unbound-method no-parameter-reassignment no-consecutive-blank-lines ordered-imports align
// tslint:enable:trailing-comma whitespace no-trailing-whitespace
//# sourceMappingURL=multiplex_feature.js.map
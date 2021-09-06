import { EncoderOverrides, ContractTxFunctionObj, BaseContract } from '@0x/base-contract';
import { BlockRange, ContractAbi, ContractArtifact, DecodedLogArgs, LogWithDecodedArgs, TxData, SupportedProvider } from 'ethereum-types';
import { BigNumber } from '@0x/utils';
import { EventCallback, IndexedFilterValues, SimpleContractArtifact } from '@0x/types';
import { Web3Wrapper } from '@0x/web3-wrapper';
export declare type MultiplexFeatureEventArgs = MultiplexFeatureExpiredOtcOrderEventArgs | MultiplexFeatureExpiredRfqOrderEventArgs | MultiplexFeatureLiquidityProviderSwapEventArgs;
export declare enum MultiplexFeatureEvents {
    ExpiredOtcOrder = "ExpiredOtcOrder",
    ExpiredRfqOrder = "ExpiredRfqOrder",
    LiquidityProviderSwap = "LiquidityProviderSwap"
}
export interface MultiplexFeatureExpiredOtcOrderEventArgs extends DecodedLogArgs {
    orderHash: string;
    maker: string;
    expiry: BigNumber;
}
export interface MultiplexFeatureExpiredRfqOrderEventArgs extends DecodedLogArgs {
    orderHash: string;
    maker: string;
    expiry: BigNumber;
}
export interface MultiplexFeatureLiquidityProviderSwapEventArgs extends DecodedLogArgs {
    inputToken: string;
    outputToken: string;
    inputTokenAmount: BigNumber;
    outputTokenAmount: BigNumber;
    provider: string;
    recipient: string;
}
export declare class MultiplexFeatureContract extends BaseContract {
    /**
     * @ignore
     */
    static deployedBytecode: string | undefined;
    static contractName: string;
    private readonly _methodABIIndex;
    private readonly _subscriptionManager;
    static deployFrom0xArtifactAsync(artifact: ContractArtifact | SimpleContractArtifact, supportedProvider: SupportedProvider, txDefaults: Partial<TxData>, logDecodeDependencies: {
        [contractName: string]: (ContractArtifact | SimpleContractArtifact);
    }, zeroExAddress: string, weth: string, sandbox: string, uniswapFactory: string, sushiswapFactory: string, uniswapPairInitCodeHash: string, sushiswapPairInitCodeHash: string): Promise<MultiplexFeatureContract>;
    static deployWithLibrariesFrom0xArtifactAsync(artifact: ContractArtifact, libraryArtifacts: {
        [libraryName: string]: ContractArtifact;
    }, supportedProvider: SupportedProvider, txDefaults: Partial<TxData>, logDecodeDependencies: {
        [contractName: string]: (ContractArtifact | SimpleContractArtifact);
    }, zeroExAddress: string, weth: string, sandbox: string, uniswapFactory: string, sushiswapFactory: string, uniswapPairInitCodeHash: string, sushiswapPairInitCodeHash: string): Promise<MultiplexFeatureContract>;
    static deployAsync(bytecode: string, abi: ContractAbi, supportedProvider: SupportedProvider, txDefaults: Partial<TxData>, logDecodeDependencies: {
        [contractName: string]: ContractAbi;
    }, zeroExAddress: string, weth: string, sandbox: string, uniswapFactory: string, sushiswapFactory: string, uniswapPairInitCodeHash: string, sushiswapPairInitCodeHash: string): Promise<MultiplexFeatureContract>;
    /**
     * @returns      The contract ABI
     */
    static ABI(): ContractAbi;
    protected static _deployLibrariesAsync(artifact: ContractArtifact, libraryArtifacts: {
        [libraryName: string]: ContractArtifact;
    }, web3Wrapper: Web3Wrapper, txDefaults: Partial<TxData>, libraryAddresses?: {
        [libraryName: string]: string;
    }): Promise<{
        [libraryName: string]: string;
    }>;
    getFunctionSignature(methodName: string): string;
    getABIDecodedTransactionData<T>(methodName: string, callData: string): T;
    getABIDecodedReturnData<T>(methodName: string, callData: string): T;
    getSelector(methodName: string): string;
    EIP712_DOMAIN_SEPARATOR(): ContractTxFunctionObj<string>;
    FEATURE_NAME(): ContractTxFunctionObj<string>;
    FEATURE_VERSION(): ContractTxFunctionObj<BigNumber>;
    _batchSellLiquidityProviderExternal(params: {
        inputToken: string;
        outputToken: string;
        sellAmount: BigNumber;
        calls: Array<{
            id: number | BigNumber;
            sellAmount: BigNumber;
            data: string;
        }>;
        useSelfBalance: boolean;
        recipient: string;
    }, wrappedCallData: string, sellAmount: BigNumber): ContractTxFunctionObj<BigNumber>;
    _batchSellUniswapV2External(params: {
        inputToken: string;
        outputToken: string;
        sellAmount: BigNumber;
        calls: Array<{
            id: number | BigNumber;
            sellAmount: BigNumber;
            data: string;
        }>;
        useSelfBalance: boolean;
        recipient: string;
    }, wrappedCallData: string, sellAmount: BigNumber): ContractTxFunctionObj<BigNumber>;
    /**
     * Initialize and register this feature.
 * Should be delegatecalled by `Migrate.migrate()`.
     */
    migrate(): ContractTxFunctionObj<string>;
    /**
     * Sells attached ETH for `outputToken` using the provided
 * calls.
      * @param outputToken The token to buy.
      * @param calls The calls to use to sell the attached ETH.
      * @param minBuyAmount The minimum amount of `outputToken` that        must be
     *     bought for this function to not revert.
     */
    multiplexBatchSellEthForToken(outputToken: string, calls: Array<{
        id: number | BigNumber;
        sellAmount: BigNumber;
        data: string;
    }>, minBuyAmount: BigNumber): ContractTxFunctionObj<BigNumber>;
    /**
     * Sells `sellAmount` of the given `inputToken` for ETH
 * using the provided calls.
      * @param inputToken The token to sell.
      * @param calls The calls to use to sell the input tokens.
      * @param sellAmount The amount of `inputToken` to sell.
      * @param minBuyAmount The minimum amount of ETH that        must be bought for
     *     this function to not revert.
     */
    multiplexBatchSellTokenForEth(inputToken: string, calls: Array<{
        id: number | BigNumber;
        sellAmount: BigNumber;
        data: string;
    }>, sellAmount: BigNumber, minBuyAmount: BigNumber): ContractTxFunctionObj<BigNumber>;
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
    multiplexBatchSellTokenForToken(inputToken: string, outputToken: string, calls: Array<{
        id: number | BigNumber;
        sellAmount: BigNumber;
        data: string;
    }>, sellAmount: BigNumber, minBuyAmount: BigNumber): ContractTxFunctionObj<BigNumber>;
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
    multiplexMultiHopSellEthForToken(tokens: string[], calls: Array<{
        id: number | BigNumber;
        data: string;
    }>, minBuyAmount: BigNumber): ContractTxFunctionObj<BigNumber>;
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
    multiplexMultiHopSellTokenForEth(tokens: string[], calls: Array<{
        id: number | BigNumber;
        data: string;
    }>, sellAmount: BigNumber, minBuyAmount: BigNumber): ContractTxFunctionObj<BigNumber>;
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
    multiplexMultiHopSellTokenForToken(tokens: string[], calls: Array<{
        id: number | BigNumber;
        data: string;
    }>, sellAmount: BigNumber, minBuyAmount: BigNumber): ContractTxFunctionObj<BigNumber>;
    /**
     * Subscribe to an event type emitted by the MultiplexFeature contract.
     * @param eventName The MultiplexFeature contract event you would like to subscribe to.
     * @param indexFilterValues An object where the keys are indexed args returned by the event and
     * the value is the value you are interested in. E.g `{maker: aUserAddressHex}`
     * @param callback Callback that gets called when a log is added/removed
     * @param isVerbose Enable verbose subscription warnings (e.g recoverable network issues encountered)
     * @return Subscription token used later to unsubscribe
     */
    subscribe<ArgsType extends MultiplexFeatureEventArgs>(eventName: MultiplexFeatureEvents, indexFilterValues: IndexedFilterValues, callback: EventCallback<ArgsType>, isVerbose?: boolean, blockPollingIntervalMs?: number): string;
    /**
     * Cancel a subscription
     * @param subscriptionToken Subscription token returned by `subscribe()`
     */
    unsubscribe(subscriptionToken: string): void;
    /**
     * Cancels all existing subscriptions
     */
    unsubscribeAll(): void;
    /**
     * Gets historical logs without creating a subscription
     * @param eventName The MultiplexFeature contract event you would like to subscribe to.
     * @param blockRange Block range to get logs from.
     * @param indexFilterValues An object where the keys are indexed args returned by the event and
     * the value is the value you are interested in. E.g `{_from: aUserAddressHex}`
     * @return Array of logs that match the parameters
     */
    getLogsAsync<ArgsType extends MultiplexFeatureEventArgs>(eventName: MultiplexFeatureEvents, blockRange: BlockRange, indexFilterValues: IndexedFilterValues): Promise<Array<LogWithDecodedArgs<ArgsType>>>;
    constructor(address: string, supportedProvider: SupportedProvider, txDefaults?: Partial<TxData>, logDecodeDependencies?: {
        [contractName: string]: ContractAbi;
    }, deployedBytecode?: string | undefined, encoderOverrides?: Partial<EncoderOverrides>);
}
//# sourceMappingURL=multiplex_feature.d.ts.map
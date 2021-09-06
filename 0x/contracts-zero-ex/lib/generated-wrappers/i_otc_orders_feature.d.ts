import { EncoderOverrides, ContractTxFunctionObj, BaseContract } from '@0x/base-contract';
import { BlockRange, ContractAbi, ContractArtifact, DecodedLogArgs, LogWithDecodedArgs, TxData, SupportedProvider } from 'ethereum-types';
import { BigNumber } from '@0x/utils';
import { EventCallback, IndexedFilterValues, SimpleContractArtifact } from '@0x/types';
import { Web3Wrapper } from '@0x/web3-wrapper';
export declare type IOtcOrdersFeatureEventArgs = IOtcOrdersFeatureOtcOrderFilledEventArgs;
export declare enum IOtcOrdersFeatureEvents {
    OtcOrderFilled = "OtcOrderFilled"
}
export interface IOtcOrdersFeatureOtcOrderFilledEventArgs extends DecodedLogArgs {
    orderHash: string;
    maker: string;
    taker: string;
    makerToken: string;
    takerToken: string;
    makerTokenFilledAmount: BigNumber;
    takerTokenFilledAmount: BigNumber;
}
export declare class IOtcOrdersFeatureContract extends BaseContract {
    /**
     * @ignore
     */
    static deployedBytecode: string | undefined;
    static contractName: string;
    private readonly _methodABIIndex;
    private readonly _subscriptionManager;
    static deployFrom0xArtifactAsync(artifact: ContractArtifact | SimpleContractArtifact, supportedProvider: SupportedProvider, txDefaults: Partial<TxData>, logDecodeDependencies: {
        [contractName: string]: (ContractArtifact | SimpleContractArtifact);
    }): Promise<IOtcOrdersFeatureContract>;
    static deployWithLibrariesFrom0xArtifactAsync(artifact: ContractArtifact, libraryArtifacts: {
        [libraryName: string]: ContractArtifact;
    }, supportedProvider: SupportedProvider, txDefaults: Partial<TxData>, logDecodeDependencies: {
        [contractName: string]: (ContractArtifact | SimpleContractArtifact);
    }): Promise<IOtcOrdersFeatureContract>;
    static deployAsync(bytecode: string, abi: ContractAbi, supportedProvider: SupportedProvider, txDefaults: Partial<TxData>, logDecodeDependencies: {
        [contractName: string]: ContractAbi;
    }): Promise<IOtcOrdersFeatureContract>;
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
    /**
     * Fill an OTC order for up to `takerTokenFillAmount` taker tokens.
 * Internal variant.
      * @param order The OTC order.
      * @param makerSignature The order signature from the maker.
      * @param takerTokenFillAmount Maximum taker token amount to fill this
     *     order with.
      * @param taker The address to fill the order in the context of.
      * @param useSelfBalance Whether to use the Exchange Proxy's balance        of
     *     input tokens.
      * @param recipient The recipient of the bought maker tokens.
     */
    _fillOtcOrder(order: {
        makerToken: string;
        takerToken: string;
        makerAmount: BigNumber;
        takerAmount: BigNumber;
        maker: string;
        taker: string;
        txOrigin: string;
        expiryAndNonce: BigNumber;
    }, makerSignature: {
        signatureType: number | BigNumber;
        v: number | BigNumber;
        r: string;
        s: string;
    }, takerTokenFillAmount: BigNumber, taker: string, useSelfBalance: boolean, recipient: string): ContractTxFunctionObj<[BigNumber, BigNumber]>;
    /**
     * Fills multiple taker-signed OTC orders.
      * @param orders Array of OTC orders.
      * @param makerSignatures Array of maker signatures for each order.
      * @param takerSignatures Array of taker signatures for each order.
      * @param unwrapWeth Array of booleans representing whether or not         to
     *     unwrap bought WETH into ETH for each order. Should be set         to
     *     false if the maker token is not WETH.
     */
    batchFillTakerSignedOtcOrders(orders: Array<{
        makerToken: string;
        takerToken: string;
        makerAmount: BigNumber;
        takerAmount: BigNumber;
        maker: string;
        taker: string;
        txOrigin: string;
        expiryAndNonce: BigNumber;
    }>, makerSignatures: Array<{
        signatureType: number | BigNumber;
        v: number | BigNumber;
        r: string;
        s: string;
    }>, takerSignatures: Array<{
        signatureType: number | BigNumber;
        v: number | BigNumber;
        r: string;
        s: string;
    }>, unwrapWeth: boolean[]): ContractTxFunctionObj<boolean[]>;
    /**
     * Fill an OTC order for up to `takerTokenFillAmount` taker tokens.
      * @param order The OTC order.
      * @param makerSignature The order signature from the maker.
      * @param takerTokenFillAmount Maximum taker token amount to fill this
     *     order with.
     */
    fillOtcOrder(order: {
        makerToken: string;
        takerToken: string;
        makerAmount: BigNumber;
        takerAmount: BigNumber;
        maker: string;
        taker: string;
        txOrigin: string;
        expiryAndNonce: BigNumber;
    }, makerSignature: {
        signatureType: number | BigNumber;
        v: number | BigNumber;
        r: string;
        s: string;
    }, takerTokenFillAmount: BigNumber): ContractTxFunctionObj<[BigNumber, BigNumber]>;
    /**
     * Fill an OTC order for up to `takerTokenFillAmount` taker tokens.
 * Unwraps bought WETH into ETH before sending it to
 * the taker.
      * @param order The OTC order.
      * @param makerSignature The order signature from the maker.
      * @param takerTokenFillAmount Maximum taker token amount to fill this
     *     order with.
     */
    fillOtcOrderForEth(order: {
        makerToken: string;
        takerToken: string;
        makerAmount: BigNumber;
        takerAmount: BigNumber;
        maker: string;
        taker: string;
        txOrigin: string;
        expiryAndNonce: BigNumber;
    }, makerSignature: {
        signatureType: number | BigNumber;
        v: number | BigNumber;
        r: string;
        s: string;
    }, takerTokenFillAmount: BigNumber): ContractTxFunctionObj<[BigNumber, BigNumber]>;
    /**
     * Fill an OTC order whose taker token is WETH for up
 * to `msg.value`.
      * @param order The OTC order.
      * @param makerSignature The order signature from the maker.
     */
    fillOtcOrderWithEth(order: {
        makerToken: string;
        takerToken: string;
        makerAmount: BigNumber;
        takerAmount: BigNumber;
        maker: string;
        taker: string;
        txOrigin: string;
        expiryAndNonce: BigNumber;
    }, makerSignature: {
        signatureType: number | BigNumber;
        v: number | BigNumber;
        r: string;
        s: string;
    }): ContractTxFunctionObj<[BigNumber, BigNumber]>;
    /**
     * Fully fill an OTC order. "Meta-transaction" variant,
 * requires order to be signed by both maker and taker.
      * @param order The OTC order.
      * @param makerSignature The order signature from the maker.
      * @param takerSignature The order signature from the taker.
     */
    fillTakerSignedOtcOrder(order: {
        makerToken: string;
        takerToken: string;
        makerAmount: BigNumber;
        takerAmount: BigNumber;
        maker: string;
        taker: string;
        txOrigin: string;
        expiryAndNonce: BigNumber;
    }, makerSignature: {
        signatureType: number | BigNumber;
        v: number | BigNumber;
        r: string;
        s: string;
    }, takerSignature: {
        signatureType: number | BigNumber;
        v: number | BigNumber;
        r: string;
        s: string;
    }): ContractTxFunctionObj<void>;
    /**
     * Fully fill an OTC order. "Meta-transaction" variant,
 * requires order to be signed by both maker and taker.
 * Unwraps bought WETH into ETH before sending it to
 * the taker.
      * @param order The OTC order.
      * @param makerSignature The order signature from the maker.
      * @param takerSignature The order signature from the taker.
     */
    fillTakerSignedOtcOrderForEth(order: {
        makerToken: string;
        takerToken: string;
        makerAmount: BigNumber;
        takerAmount: BigNumber;
        maker: string;
        taker: string;
        txOrigin: string;
        expiryAndNonce: BigNumber;
    }, makerSignature: {
        signatureType: number | BigNumber;
        v: number | BigNumber;
        r: string;
        s: string;
    }, takerSignature: {
        signatureType: number | BigNumber;
        v: number | BigNumber;
        r: string;
        s: string;
    }): ContractTxFunctionObj<void>;
    /**
     * Get the canonical hash of an OTC order.
      * @param order The OTC order.
     */
    getOtcOrderHash(order: {
        makerToken: string;
        takerToken: string;
        makerAmount: BigNumber;
        takerAmount: BigNumber;
        maker: string;
        taker: string;
        txOrigin: string;
        expiryAndNonce: BigNumber;
    }): ContractTxFunctionObj<string>;
    /**
     * Get the order info for an OTC order.
      * @param order The OTC order.
     */
    getOtcOrderInfo(order: {
        makerToken: string;
        takerToken: string;
        makerAmount: BigNumber;
        takerAmount: BigNumber;
        maker: string;
        taker: string;
        txOrigin: string;
        expiryAndNonce: BigNumber;
    }): ContractTxFunctionObj<{
        orderHash: string;
        status: number;
    }>;
    /**
     * Get the last nonce used for a particular
 * tx.origin address and nonce bucket.
      * @param txOrigin The address.
      * @param nonceBucket The nonce bucket index.
     */
    lastOtcTxOriginNonce(txOrigin: string, nonceBucket: BigNumber): ContractTxFunctionObj<BigNumber>;
    /**
     * Subscribe to an event type emitted by the IOtcOrdersFeature contract.
     * @param eventName The IOtcOrdersFeature contract event you would like to subscribe to.
     * @param indexFilterValues An object where the keys are indexed args returned by the event and
     * the value is the value you are interested in. E.g `{maker: aUserAddressHex}`
     * @param callback Callback that gets called when a log is added/removed
     * @param isVerbose Enable verbose subscription warnings (e.g recoverable network issues encountered)
     * @return Subscription token used later to unsubscribe
     */
    subscribe<ArgsType extends IOtcOrdersFeatureEventArgs>(eventName: IOtcOrdersFeatureEvents, indexFilterValues: IndexedFilterValues, callback: EventCallback<ArgsType>, isVerbose?: boolean, blockPollingIntervalMs?: number): string;
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
     * @param eventName The IOtcOrdersFeature contract event you would like to subscribe to.
     * @param blockRange Block range to get logs from.
     * @param indexFilterValues An object where the keys are indexed args returned by the event and
     * the value is the value you are interested in. E.g `{_from: aUserAddressHex}`
     * @return Array of logs that match the parameters
     */
    getLogsAsync<ArgsType extends IOtcOrdersFeatureEventArgs>(eventName: IOtcOrdersFeatureEvents, blockRange: BlockRange, indexFilterValues: IndexedFilterValues): Promise<Array<LogWithDecodedArgs<ArgsType>>>;
    constructor(address: string, supportedProvider: SupportedProvider, txDefaults?: Partial<TxData>, logDecodeDependencies?: {
        [contractName: string]: ContractAbi;
    }, deployedBytecode?: string | undefined, encoderOverrides?: Partial<EncoderOverrides>);
}
//# sourceMappingURL=i_otc_orders_feature.d.ts.map
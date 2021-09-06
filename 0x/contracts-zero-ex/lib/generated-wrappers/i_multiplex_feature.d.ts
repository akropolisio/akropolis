import { EncoderOverrides, ContractTxFunctionObj, BaseContract } from '@0x/base-contract';
import { ContractAbi, ContractArtifact, TxData, SupportedProvider } from 'ethereum-types';
import { BigNumber } from '@0x/utils';
import { SimpleContractArtifact } from '@0x/types';
import { Web3Wrapper } from '@0x/web3-wrapper';
export declare class IMultiplexFeatureContract extends BaseContract {
    /**
     * @ignore
     */
    static deployedBytecode: string | undefined;
    static contractName: string;
    private readonly _methodABIIndex;
    static deployFrom0xArtifactAsync(artifact: ContractArtifact | SimpleContractArtifact, supportedProvider: SupportedProvider, txDefaults: Partial<TxData>, logDecodeDependencies: {
        [contractName: string]: (ContractArtifact | SimpleContractArtifact);
    }): Promise<IMultiplexFeatureContract>;
    static deployWithLibrariesFrom0xArtifactAsync(artifact: ContractArtifact, libraryArtifacts: {
        [libraryName: string]: ContractArtifact;
    }, supportedProvider: SupportedProvider, txDefaults: Partial<TxData>, logDecodeDependencies: {
        [contractName: string]: (ContractArtifact | SimpleContractArtifact);
    }): Promise<IMultiplexFeatureContract>;
    static deployAsync(bytecode: string, abi: ContractAbi, supportedProvider: SupportedProvider, txDefaults: Partial<TxData>, logDecodeDependencies: {
        [contractName: string]: ContractAbi;
    }): Promise<IMultiplexFeatureContract>;
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
      * @param minBuyAmount The minimum amount of output tokens that        must be
     *     bought for this function to not revert.
     */
    multiplexMultiHopSellTokenForToken(tokens: string[], calls: Array<{
        id: number | BigNumber;
        data: string;
    }>, sellAmount: BigNumber, minBuyAmount: BigNumber): ContractTxFunctionObj<BigNumber>;
    constructor(address: string, supportedProvider: SupportedProvider, txDefaults?: Partial<TxData>, logDecodeDependencies?: {
        [contractName: string]: ContractAbi;
    }, deployedBytecode?: string | undefined, encoderOverrides?: Partial<EncoderOverrides>);
}
//# sourceMappingURL=i_multiplex_feature.d.ts.map
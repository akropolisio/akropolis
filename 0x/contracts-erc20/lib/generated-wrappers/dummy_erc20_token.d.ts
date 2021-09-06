import { EncoderOverrides, ContractFunctionObj, ContractTxFunctionObj, BaseContract } from '@0x/base-contract';
import { BlockRange, ContractAbi, ContractArtifact, DecodedLogArgs, LogWithDecodedArgs, TxData, SupportedProvider } from 'ethereum-types';
import { BigNumber } from '@0x/utils';
import { EventCallback, IndexedFilterValues, SimpleContractArtifact } from '@0x/types';
import { Web3Wrapper } from '@0x/web3-wrapper';
export declare type DummyERC20TokenEventArgs = DummyERC20TokenApprovalEventArgs | DummyERC20TokenOwnershipTransferredEventArgs | DummyERC20TokenTransferEventArgs;
export declare enum DummyERC20TokenEvents {
    Approval = "Approval",
    OwnershipTransferred = "OwnershipTransferred",
    Transfer = "Transfer"
}
export interface DummyERC20TokenApprovalEventArgs extends DecodedLogArgs {
    _owner: string;
    _spender: string;
    _value: BigNumber;
}
export interface DummyERC20TokenOwnershipTransferredEventArgs extends DecodedLogArgs {
    previousOwner: string;
    newOwner: string;
}
export interface DummyERC20TokenTransferEventArgs extends DecodedLogArgs {
    _from: string;
    _to: string;
    _value: BigNumber;
}
export declare class DummyERC20TokenContract extends BaseContract {
    /**
     * @ignore
     */
    static deployedBytecode: string | undefined;
    static contractName: string;
    private readonly _methodABIIndex;
    private readonly _subscriptionManager;
    static deployFrom0xArtifactAsync(artifact: ContractArtifact | SimpleContractArtifact, supportedProvider: SupportedProvider, txDefaults: Partial<TxData>, logDecodeDependencies: {
        [contractName: string]: (ContractArtifact | SimpleContractArtifact);
    }, _name: string, _symbol: string, _decimals: BigNumber, _totalSupply: BigNumber): Promise<DummyERC20TokenContract>;
    static deployWithLibrariesFrom0xArtifactAsync(artifact: ContractArtifact, libraryArtifacts: {
        [libraryName: string]: ContractArtifact;
    }, supportedProvider: SupportedProvider, txDefaults: Partial<TxData>, logDecodeDependencies: {
        [contractName: string]: (ContractArtifact | SimpleContractArtifact);
    }, _name: string, _symbol: string, _decimals: BigNumber, _totalSupply: BigNumber): Promise<DummyERC20TokenContract>;
    static deployAsync(bytecode: string, abi: ContractAbi, supportedProvider: SupportedProvider, txDefaults: Partial<TxData>, logDecodeDependencies: {
        [contractName: string]: ContractAbi;
    }, _name: string, _symbol: string, _decimals: BigNumber, _totalSupply: BigNumber): Promise<DummyERC20TokenContract>;
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
    MAX_MINT_AMOUNT(): ContractFunctionObj<BigNumber>;
    allowance(_owner: string, _spender: string): ContractFunctionObj<BigNumber>;
    /**
     * `msg.sender` approves `_spender` to spend `_value` tokens
      * @param _spender The address of the account able to transfer the tokens
      * @param _value The amount of wei to be approved for transfer
    * @returns Always true if the call has enough gas to complete execution
     */
    approve(_spender: string, _value: BigNumber): ContractTxFunctionObj<boolean>;
    /**
     * Query the balance of owner
      * @param _owner The address from which the balance will be retrieved
    * @returns Balance of owner
     */
    balanceOf(_owner: string): ContractFunctionObj<BigNumber>;
    decimals(): ContractFunctionObj<BigNumber>;
    /**
     * Mints new tokens for sender
      * @param _value Amount of tokens to mint
     */
    mint(_value: BigNumber): ContractTxFunctionObj<void>;
    name(): ContractFunctionObj<string>;
    owner(): ContractFunctionObj<string>;
    /**
     * Sets the balance of target address
      * @param _target Address or which balance will be updated
      * @param _value New balance of target address
     */
    setBalance(_target: string, _value: BigNumber): ContractTxFunctionObj<void>;
    symbol(): ContractFunctionObj<string>;
    /**
     * Query total supply of token
    * @returns Total supply of token
     */
    totalSupply(): ContractFunctionObj<BigNumber>;
    /**
     * send `value` token to `to` from `msg.sender`
      * @param _to The address of the recipient
      * @param _value The amount of token to be transferred
    * @returns True if transfer was successful
     */
    transfer(_to: string, _value: BigNumber): ContractTxFunctionObj<boolean>;
    /**
     * ERC20 transferFrom, modified such that an allowance of MAX_UINT represents an unlimited allowance. See https://github.com/ethereum/EIPs/issues/717
      * @param _from Address to transfer from.
      * @param _to Address to transfer to.
      * @param _value Amount to transfer.
    * @returns Success of transfer.
     */
    transferFrom(_from: string, _to: string, _value: BigNumber): ContractTxFunctionObj<boolean>;
    /**
     * Change the owner of this contract.
      * @param newOwner New owner address.
     */
    transferOwnership(newOwner: string): ContractTxFunctionObj<void>;
    /**
     * Subscribe to an event type emitted by the DummyERC20Token contract.
     * @param eventName The DummyERC20Token contract event you would like to subscribe to.
     * @param indexFilterValues An object where the keys are indexed args returned by the event and
     * the value is the value you are interested in. E.g `{maker: aUserAddressHex}`
     * @param callback Callback that gets called when a log is added/removed
     * @param isVerbose Enable verbose subscription warnings (e.g recoverable network issues encountered)
     * @return Subscription token used later to unsubscribe
     */
    subscribe<ArgsType extends DummyERC20TokenEventArgs>(eventName: DummyERC20TokenEvents, indexFilterValues: IndexedFilterValues, callback: EventCallback<ArgsType>, isVerbose?: boolean, blockPollingIntervalMs?: number): string;
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
     * @param eventName The DummyERC20Token contract event you would like to subscribe to.
     * @param blockRange Block range to get logs from.
     * @param indexFilterValues An object where the keys are indexed args returned by the event and
     * the value is the value you are interested in. E.g `{_from: aUserAddressHex}`
     * @return Array of logs that match the parameters
     */
    getLogsAsync<ArgsType extends DummyERC20TokenEventArgs>(eventName: DummyERC20TokenEvents, blockRange: BlockRange, indexFilterValues: IndexedFilterValues): Promise<Array<LogWithDecodedArgs<ArgsType>>>;
    constructor(address: string, supportedProvider: SupportedProvider, txDefaults?: Partial<TxData>, logDecodeDependencies?: {
        [contractName: string]: ContractAbi;
    }, deployedBytecode?: string | undefined, encoderOverrides?: Partial<EncoderOverrides>);
}
//# sourceMappingURL=dummy_erc20_token.d.ts.map
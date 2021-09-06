/// <reference types="web3-provider-engine" />
import { BlockchainLifecycle } from '@0x/dev-utils';
import { Web3ProviderEngine } from '@0x/subproviders';
import { TxData, Web3Wrapper } from '@0x/web3-wrapper';
import * as mocha from 'mocha';
export declare type ISuite = mocha.ISuite;
export declare type ISuiteCallbackContext = mocha.ISuiteCallbackContext;
export declare type SuiteCallback = (this: ISuiteCallbackContext) => void;
export declare type ContextDefinitionCallback<T> = (description: string, callback: SuiteCallback) => T;
export declare type BlockchainSuiteCallback = (this: ISuiteCallbackContext, env: BlockchainTestsEnvironment) => void;
export declare type BlockchainContextDefinitionCallback<T> = (description: string, callback: BlockchainSuiteCallback) => T;
export interface ContextDefinition extends mocha.IContextDefinition {
    optional: ContextDefinitionCallback<ISuite | void>;
}
/**
 * `blockchainTests()` config options.
 */
export interface BlockchainContextConfig {
    fork: Partial<{
        unlockedAccounts: string[];
    }>;
}
/**
 * Interface for `blockchainTests()`.
 */
export interface BlockchainContextDefinition {
    (description: string, callback: BlockchainSuiteCallback): ISuite;
    configure: (config?: Partial<BlockchainContextConfig>) => void;
    only: BlockchainContextDefinitionCallback<ISuite>;
    skip: BlockchainContextDefinitionCallback<void>;
    optional: BlockchainContextDefinitionCallback<ISuite | void>;
    resets: BlockchainContextDefinitionCallback<ISuite | void> & {
        only: BlockchainContextDefinitionCallback<ISuite>;
        skip: BlockchainContextDefinitionCallback<void>;
        optional: BlockchainContextDefinitionCallback<ISuite | void>;
    };
    fork: BlockchainContextDefinitionCallback<ISuite | void> & {
        only: BlockchainContextDefinitionCallback<ISuite>;
        skip: BlockchainContextDefinitionCallback<void>;
        optional: BlockchainContextDefinitionCallback<ISuite | void>;
        resets: BlockchainContextDefinitionCallback<ISuite | void>;
    };
    live: BlockchainContextDefinitionCallback<ISuite | void> & {
        only: BlockchainContextDefinitionCallback<ISuite>;
        skip: BlockchainContextDefinitionCallback<void>;
        optional: BlockchainContextDefinitionCallback<ISuite | void>;
    };
}
/**
 * Describes the environment object passed into the `blockchainTests()` callback.
 */
export interface BlockchainTestsEnvironment {
    blockchainLifecycle: BlockchainLifecycle;
    provider: Web3ProviderEngine;
    txDefaults: Partial<TxData>;
    web3Wrapper: Web3Wrapper;
    getChainIdAsync(): Promise<number>;
    getAccountAddressesAsync(): Promise<string[]>;
}
declare class BlockchainTestsEnvironmentBase {
    blockchainLifecycle: BlockchainLifecycle;
    provider: Web3ProviderEngine;
    txDefaults: Partial<TxData>;
    web3Wrapper: Web3Wrapper;
    getChainIdAsync(): Promise<number>;
    getAccountAddressesAsync(): Promise<string[]>;
}
/**
 * `BlockchainTestsEnvironment` that uses the default ganache provider.
 */
export declare class StandardBlockchainTestsEnvironmentSingleton extends BlockchainTestsEnvironmentBase {
    private static _instance;
    static create(): StandardBlockchainTestsEnvironmentSingleton;
    static reset(): void;
    static getInstance(): StandardBlockchainTestsEnvironmentSingleton | undefined;
    protected constructor();
}
/**
 * `BlockchainTestsEnvironment` that uses a forked ganache provider.
 */
export declare class ForkedBlockchainTestsEnvironmentSingleton extends BlockchainTestsEnvironmentBase {
    private static _instance;
    static create(): ForkedBlockchainTestsEnvironmentSingleton;
    static reset(): void;
    protected static _createWeb3Provider(forkHost: string): Web3ProviderEngine;
    static getInstance(): ForkedBlockchainTestsEnvironmentSingleton | undefined;
    protected constructor();
}
/**
 * `BlockchainTestsEnvironment` that uses a live web3 provider.
 */
export declare class LiveBlockchainTestsEnvironmentSingleton extends BlockchainTestsEnvironmentBase {
    private static _instance;
    static create(): LiveBlockchainTestsEnvironmentSingleton;
    static reset(): void;
    protected static _createWeb3Provider(rpcHost: string): Web3ProviderEngine;
    static getInstance(): LiveBlockchainTestsEnvironmentSingleton | undefined;
    protected constructor();
}
/**
 * An augmented version of mocha's `describe()`.
 */
export declare const describe: ContextDefinition;
/**
 * Like mocha's `describe()`, but sets up a blockchain environment for you.
 */
export declare const blockchainTests: BlockchainContextDefinition;
export {};
//# sourceMappingURL=mocha_blockchain.d.ts.map
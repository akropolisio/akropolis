/// <reference types="node" />
import { SignatureType, SignedZeroExTransaction, ZeroExTransaction } from '@0x/types';
export declare class TransactionFactory {
    private readonly _signerBuff;
    private readonly _exchangeAddress;
    private readonly _privateKey;
    private readonly _chainId;
    constructor(privateKey: Buffer, exchangeAddress: string, chainId: number);
    newSignedTransactionAsync(customTransactionParams: Partial<ZeroExTransaction>, signatureType?: SignatureType): Promise<SignedZeroExTransaction>;
}
//# sourceMappingURL=transaction_factory.d.ts.map
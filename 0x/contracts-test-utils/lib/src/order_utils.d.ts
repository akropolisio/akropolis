import { Order, SignedOrder } from '@0x/types';
import { BigNumber } from '@0x/utils';
import { BatchMatchOrder, CancelOrder, MatchOrder } from './types';
export declare const orderUtils: {
    getPartialAmountFloor(numerator: BigNumber, denominator: BigNumber, target: BigNumber): BigNumber;
    createFill: (signedOrder: SignedOrder, takerAssetFillAmount?: BigNumber | undefined) => {
        order: SignedOrder;
        takerAssetFillAmount: BigNumber;
        signature: string;
    };
    createCancel(signedOrder: SignedOrder, takerAssetCancelAmount?: BigNumber | undefined): CancelOrder;
    createOrderWithoutSignature(signedOrder: SignedOrder): Order;
    createBatchMatchOrders(signedOrdersLeft: SignedOrder[], signedOrdersRight: SignedOrder[]): BatchMatchOrder;
    createMatchOrders(signedOrderLeft: SignedOrder, signedOrderRight: SignedOrder): MatchOrder;
    generatePseudoRandomOrderHash(): string;
};
//# sourceMappingURL=order_utils.d.ts.map
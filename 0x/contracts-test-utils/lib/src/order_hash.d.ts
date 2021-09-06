/// <reference types="node" />
import { Order, SignedOrder } from '@0x/types';
export declare const orderHashUtils: {
    /**
     * Computes the orderHash for a supplied order.
     * @param   order   An object that conforms to the Order or SignedOrder interface definitions.
     * @return  Hex encoded string orderHash from hashing the supplied order.
     */
    getOrderHashHex(order: SignedOrder | Order): string;
    /**
     * Computes the orderHash for a supplied order
     * @param   order   An object that conforms to the Order or SignedOrder interface definitions.
     * @return  A Buffer containing the resulting orderHash from hashing the supplied order
     */
    getOrderHashBuffer(order: SignedOrder | Order): Buffer;
};
//# sourceMappingURL=order_hash.d.ts.map
import { BigNumber } from '@0x/utils';
export declare const uint256Values: BigNumber[];
export declare const bytes32Values: string[];
export declare function testCombinatoriallyWithReferenceFunc<P0, P1, R>(name: string, referenceFunc: (p0: P0, p1: P1) => Promise<R>, testFunc: (p0: P0, p1: P1) => Promise<R>, allValues: [P0[], P1[]]): void;
export declare function testCombinatoriallyWithReferenceFunc<P0, P1, P2, R>(name: string, referenceFunc: (p0: P0, p1: P1, p2: P2) => Promise<R>, testFunc: (p0: P0, p1: P1, p2: P2) => Promise<R>, allValues: [P0[], P1[], P2[]]): void;
export declare function testCombinatoriallyWithReferenceFunc<P0, P1, P2, P3, R>(name: string, referenceFunc: (p0: P0, p1: P1, p2: P2, p3: P3) => Promise<R>, testFunc: (p0: P0, p1: P1, p2: P2, p3: P3) => Promise<R>, allValues: [P0[], P1[], P2[], P3[]]): void;
export declare function testCombinatoriallyWithReferenceFunc<P0, P1, P2, P3, P4, R>(name: string, referenceFunc: (p0: P0, p1: P1, p2: P2, p3: P3, p4: P4) => Promise<R>, testFunc: (p0: P0, p1: P1, p2: P2, p3: P3, p4: P4) => Promise<R>, allValues: [P0[], P1[], P2[], P3[], P4[]]): void;
//# sourceMappingURL=combinatorial_utils.d.ts.map
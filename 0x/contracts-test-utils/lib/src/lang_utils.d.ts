import * as _ from 'lodash';
/**
 * _.zip() that clips to the shortest array.
 */
export declare function shortZip<T1, T2>(a: T1[], b: T2[]): Array<[T1, T2]>;
/**
 * Replaces the keys in a deeply nested object. Adapted from https://stackoverflow.com/a/39126851
 */
export declare function replaceKeysDeep(obj: {}, mapKeys: (key: string) => string | void): _.Dictionary<{}>;
//# sourceMappingURL=lang_utils.d.ts.map
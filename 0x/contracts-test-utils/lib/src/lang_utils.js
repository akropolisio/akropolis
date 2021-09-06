"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.replaceKeysDeep = exports.shortZip = void 0;
const _ = require("lodash");
/**
 * _.zip() that clips to the shortest array.
 */
function shortZip(a, b) {
    const minLength = Math.min(a.length, b.length);
    return _.zip(a.slice(0, minLength), b.slice(0, minLength));
}
exports.shortZip = shortZip;
/**
 * Replaces the keys in a deeply nested object. Adapted from https://stackoverflow.com/a/39126851
 */
function replaceKeysDeep(obj, mapKeys) {
    return _.transform(obj, (result, value, key) => {
        const currentKey = mapKeys(key) || key;
        result[currentKey] = _.isObject(value) ? replaceKeysDeep(value, mapKeys) : value;
    });
}
exports.replaceKeysDeep = replaceKeysDeep;
//# sourceMappingURL=lang_utils.js.map
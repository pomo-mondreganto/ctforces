function isString(value) {
    return typeof value === 'string' || value instanceof String;
}

function isNumber(value) {
    return typeof value === 'number' && isFinite(value);
}

function isArray(value) {
    return value && typeof value === 'object' && value.constructor === Array;
}

function isFunction(value) {
    return typeof value === 'function';
}

function isObject(value) {
    return value && typeof value === 'object' && value.constructor === Object;
}
function isNull(value) {
    return value === null;
}

function isUndefined(value) {
    return typeof value === 'undefined';
}

function isBoolean(value) {
    return typeof value === 'boolean';
}

function isRegExp(value) {
    return value && typeof value === 'object' && value.constructor === RegExp;
}

export {
    isString,
    isNumber,
    isArray,
    isFunction,
    isObject,
    isNull,
    isUndefined,
    isBoolean,
    isRegExp,
};

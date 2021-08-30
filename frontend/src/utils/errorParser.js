import { isString, isUndefined } from '@/utils/types';

function parse(errors) {
    let result = {};
    for (let key in errors) {
        if (isString(errors[key])) {
            result[key] = [errors[key]];
        } else {
            result[key] = errors[key];
        }
    }
    if (!isUndefined(result.non_field_errors)) {
        result.detail = result.non_field_errors;
        delete result.non_field_errors;
    }
    return result;
}

export default parse;

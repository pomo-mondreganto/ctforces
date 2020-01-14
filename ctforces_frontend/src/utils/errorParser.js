import { isString } from '@/utils/types';

function parse(errors) {
    let result = {};
    for (let key in errors) {
        if (isString(errors[key])) {
            result[key] = [errors[key]];
        } else {
            result[key] = errors[key];
        }
    }
    return result;
}

export default parse;

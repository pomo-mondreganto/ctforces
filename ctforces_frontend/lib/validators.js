export function validate(data, validators) {
    let errors = [];
    validators.forEach(validator => {
        let result = validator(data);
        if (result) {
            errors.push(result);
        }
    });
    if (errors.length) {
        return errors;
    } else {
        return false;
    }
}

export default function validateFields(fields, validators) {
    let verdicts = {};
    let ok = true;
    for (let fieldName in validators) {
        let bad = false;
        let errors = [];
        validators[fieldName].forEach(validator => {
            let result = validator(fields[fieldName]);
            if (result) {
                bad = true;
                errors.push(result);
            }
        });
        if (bad) {
            verdicts[fieldName] = errors;
            ok = false;
        }
    }
    return {
        ok: ok,
        verdicts: verdicts
    };
}

export function validateOk() {
    return {
        ok: true,
        verdicts: {}
    };
}

export function required(data) {
    if (data === '') {
        return 'Required';
    } else {
        return false;
    }
}

export function lengthGt(ln) {
    return function(data) {
        if (data.length <= ln) {
            return `Length must be greater than ${ln}`;
        } else {
            return false;
        }
    };
}

export function lengthGte(ln) {
    return function(data) {
        if (data.length < ln) {
            return `Length must be greater or equal to ${ln}`;
        } else {
            return false;
        }
    };
}

export function lengthLt(ln) {
    return function(data) {
        if (data.length >= ln) {
            return `Length must be lower than ${ln}`;
        } else {
            return false;
        }
    };
}

export function lengthLte(ln) {
    return function(data) {
        if (data.length > ln) {
            return `Length must be lower or equal to ${ln}`;
        } else {
            return false;
        }
    };
}

export function lengthBetween(lnmn, lnmx) {
    return function(data) {
        if (data.length < lnmn || data.length > lnmx) {
            return `Length must be between ${lnmn} and ${lnmx}`;
        } else {
            return false;
        }
    };
}

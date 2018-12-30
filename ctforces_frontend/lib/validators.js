export default function validate(data, validators, fieldValues) {
    let errors = [];
    validators.forEach(validator => {
        let result = validator(data, fieldValues);
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

export function equalTo(fieldName) {
    return function(data, fieldValues) {
        if (data !== fieldValues[fieldName]) {
            return `Must be equal to ${fieldName}`;
        } else {
            return false;
        }
    };
}

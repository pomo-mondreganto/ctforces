import React from 'react';

import { Input, FormGroup, FormFeedback } from 'reactstrap';

const Component = ({ field, form, ...props }) => {
    const name = 'detail';
    const invalid = form.errors[name] && form.errors[name] && true;

    return (
        <FormGroup>
            <Input
                name={name}
                value={field.value}
                disabled={form.isSubmitting}
                onChange={field.onChange}
                onBlur={field.onBlur}
                invalid={invalid}
                {...props}
                hidden
            />
            <FormFeedback>{form.errors[name]}</FormFeedback>
        </FormGroup>
    );
};

export default Component;

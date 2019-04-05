import React from 'react';

import { Input, FormGroup, FormFeedback } from 'reactstrap';

import 'styles/components/Form/TextInput.scss';

const Component = ({ field, form, ...props }) => {
    const { name } = field;
    const invalid = form.errors[name] && true;

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
            />
            <FormFeedback>{form.errors[name]}</FormFeedback>
        </FormGroup>
    );
};

export default Component;

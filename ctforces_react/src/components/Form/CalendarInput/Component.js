import React from 'react';

import { FormGroup, FormFeedback } from 'reactstrap';
import DatePicker from 'react-datetime';

import 'styles/components/Form/Calendar.scss';

const Component = ({
    field, form, handleChange, ...props
}) => {
    const { name } = field;
    const invalid = form.errors[name] && form.errors[name] && true;

    return (
        <FormGroup>
            <DatePicker
                name={name}
                value={field.value}
                disabled={form.isSubmitting}
                onChange={handleChange}
                invalid={invalid}
                {...props}
            />
            <FormFeedback>{form.errors[name]}</FormFeedback>
        </FormGroup>
    );
};

export default Component;

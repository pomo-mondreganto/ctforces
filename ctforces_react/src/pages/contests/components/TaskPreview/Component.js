import React from 'react';

import { Input, FormGroup, FormFeedback } from 'reactstrap';

const Component = ({
    field, form, handleChange, ...props
}) => {
    const { name } = field;
    const invalid = form.errors[name] && form.errors[name] && true;

    const task = field.value;
    return (
        <FormGroup>
            <Input
                name={`${field.name}`}
                value={task.id}
                disabled={form.isSubmitting}
                onChange={handleChange}
                onBlur={field.onBlur}
                invalid={invalid}
                {...props}
            />
            <span>{task.name}</span>
            <span>{task.cost}</span>
            <span>{task.main_tag}</span>
            <FormFeedback>{form.errors[name]}</FormFeedback>
        </FormGroup>
    );
};

export default Component;

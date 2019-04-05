import React from 'react';

import TagsInput from 'react-tagsinput';
import { FormGroup, FormFeedback } from 'reactstrap';

import 'react-tagsinput/react-tagsinput.css';

const Component = ({ field, form, ...props }) => {
    const { name } = field;
    const invalid = form.errors[name] && true;

    return (
        <FormGroup>
            <TagsInput value={field.value} onChange={props.handleChange} />
            <span className={`${invalid ? 'is-invalid' : ''} form-control`} hidden></span>
            <FormFeedback>{form.errors[name]}</FormFeedback>
        </FormGroup>
    );
};

export default Component;

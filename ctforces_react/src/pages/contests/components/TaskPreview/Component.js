import React from 'react';

import { Input, FormFeedback } from 'reactstrap';
import Select from 'react-select';

const Component = ({
    field, form, handleChange, handleMainTagChange, tags, ...props
}) => {
    const { name } = field;
    const invalid = form.errors[name] && form.errors[name] && true;

    const task = field.value;

    return (
        <div className="mb-3 task-add-info">
            <Input
                placeholder="Task id"
                name={field.name}
                value={task.id}
                disabled={form.isSubmitting}
                onChange={handleChange}
                onBlur={field.onBlur}
                invalid={invalid}
                {...props}
            />
            <Input value={task.name} disabled readOnly />
            <Input name={`${field.name}.cost`}
                disabled={task.id === ''}
                onChange={field.onChange}
                value={task.cost}
            />
            <Select
                value={{ value: task.main_tag.id, label: task.main_tag.name }}
                options={tags.map(obj => ({ value: obj.id, label: obj.name }))}
                isDisabled={task.id === ''}
                onChange={handleMainTagChange}
            />
            <FormFeedback>{form.errors[name]}</FormFeedback>
        </div>
    );
};

export default Component;

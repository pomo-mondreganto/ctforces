import React from 'react';

import axios from 'axios';
import Component from './Component';

class TaskPreviewContainer extends React.Component {
    handleChange = async (e) => {
        const { name } = e.target;
        const value = parseInt(e.target.value, 10);

        this.props.form.setFieldValue(`${name}.id`, value);
        const id = value;
        try {
            const response = await axios.get(`/tasks/${id}/`);
            const task = response.data;
            this.props.form.setFieldValue(`${name}.cost`, task.cost);
            this.props.form.setFieldValue(`${name}.name`, task.name);
            this.props.form.setFieldValue(
                `${name}.main_tag`,
                task.tags_details.length > 0 ? task.tags_details[0].id : '',
            );
        } catch {
            this.props.form.setFieldValue(`${name}.cost`, '');
            this.props.form.setFieldValue(`${name}.name`, '');
            this.props.form.setFieldValue(`${name}.main_tag`, '');
        }
    };

    render() {
        return <Component handleChange={this.handleChange} {...this.props} />;
    }
}

export default TaskPreviewContainer;

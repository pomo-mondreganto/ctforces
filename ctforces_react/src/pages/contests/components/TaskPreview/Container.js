import React from 'react';

import Component from './Component';
import axios from 'axios';

class TaskPreviewContainer extends React.Component {
    constructor(props) {
        super(props);
    }

    handleChange = async e => {
        const name = e.target.name;
        const value = parseInt(e.target.value);

        this.props.form.setFieldValue(`${name}.id`, value);
        const id = value;
        try {
            const response = await axios.get(`/tasks/${id}/`);
            const task = response.data;
            this.props.form.setFieldValue(`${name}.cost`, task.cost);
            this.props.form.setFieldValue(`${name}.name`, task.name);
            this.props.form.setFieldValue(
                `${name}.main_tag`,
                task.tags_details.length > 0 ? task.tags_details[0].id : ''
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

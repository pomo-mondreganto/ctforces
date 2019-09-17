import React from 'react';

import axios from 'axios';
import Component from './Component';

class TaskPreviewContainer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            tags: [],
            name: '',
        };
    }

    handleMainTagChange = (tag) => {
        this.props.form.setFieldValue(`${this.state.name}.main_tag`,
            this.state.tags.find(obj => obj.name === tag.label));
    }

    handleChange = async (e) => {
        const { name } = e.target;

        this.setState({ name });

        try {
            const value = parseInt(e.target.value, 10);

            if (Number.isNaN(value)) {
                this.props.form.setFieldValue(`${name}.id`, '');
                throw new Error('Not a number');
            }

            this.props.form.setFieldValue(`${name}.id`, value);
            const id = value;
            const response = await axios.get(`/tasks/${id}/`);
            const task = response.data;
            this.props.form.setFieldValue(`${name}.cost`, task.cost);
            this.props.form.setFieldValue(`${name}.name`, task.name);
            this.props.form.setFieldValue(`${name}.main_tag`, task.tags_details[0]);
            this.setState({
                tags: task.tags_details,
            });
        } catch {
            this.props.form.setFieldValue(`${name}.cost`, '');
            this.props.form.setFieldValue(`${name}.name`, '');
            this.props.form.setFieldValue(`${name}.main_tag`, '');
            this.setState({
                tags: [],
            });
        }
    };

    render() {
        return <Component {...this.props}
            handleChange={this.handleChange}
            tags={this.state.tags}
            handleMainTagChange={this.handleMainTagChange} />;
    }
}

export default TaskPreviewContainer;

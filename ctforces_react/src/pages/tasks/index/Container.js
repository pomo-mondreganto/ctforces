import React from 'react';

import axios from 'axios';
import Component from './Component';


class TaskViewContainer extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            task: null,
        };
    }

    async componentDidMount() {
        const { id } = this.props.match.params;
        const response = await axios.get(`/tasks/${id}/`);
        this.setState({
            task: response.data,
        });
    }

    handleSubmit = async ({ values, actions }) => {
        try {
            await axios.post(`/tasks/${this.state.task.id}/submit/`, values);
            const { task } = this.state;
            task.is_solved_by_user = true;
            this.setState({ task });
            actions.setSubmitting(false);
        } catch (error) {
            const errorData = error.response.data;
            Object.keys(errorData).forEach((key) => {
                actions.setFieldError(key, errorData[key]);
                actions.setFieldTouched(key, true, false);
            });
            actions.setSubmitting(false);
        }
    }

    render() {
        return <Component
            task={this.state.task}
            handleSubmit={this.handleSubmit}
        />;
    }
}

export default TaskViewContainer;

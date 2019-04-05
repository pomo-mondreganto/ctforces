import React from 'react';

import axios from 'axios';
import Component from './Component';


class ContestTaskViewContainer extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            task: null,
        };
    }

    async componentDidMount() {
        const { id, task_id: taskId } = this.props.match.params;
        const response = await axios.get(`/contests/${id}/tasks/${taskId}/`);
        this.setState({
            task: response.data,
            contestId: id,
            taskId,
        });
    }

    handleSubmit = async ({ values, actions }) => {
        try {
            await axios.post(`/contests/${this.state.contestId}/tasks/${this.state.taskId}/submit/`, values);
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

export default ContestTaskViewContainer;

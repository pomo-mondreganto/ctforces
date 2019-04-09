import React from 'react';

import axios from 'axios';
import { success } from 'lib/toasts';
import { Redirect } from 'react-router-dom';
import Component from './Component';


class TaskViewContainer extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            task: null,
            redirect: null,
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
            success('Success!');
            actions.setSubmitting(false);
            this.setState({
                redirect: '/tasks/',
            });
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
        if (this.state.redirect !== null) {
            return <Redirect to={this.state.redirect} />;
        }

        return <Component
            task={this.state.task}
            handleSubmit={this.handleSubmit}
        />;
    }
}

export default TaskViewContainer;

import React from 'react';

import axios from 'axios';
import { Redirect } from 'react-router-dom';
import Component from './Component';

class ContestCreateContainer extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            contest: null,
            redirect: null,
        };
    }

    async componentDidMount() {
        const { id } = this.props.match.params;
        const response = await axios.get(`/contests/${id}/full/`);
        this.setState({
            contest: response.data,
        });
    }

    handleSubmit = async ({ values, actions }) => {
        try {
            const response = await axios.post('/contests/', {
                ...values,
            });
            const { id } = response.data;

            const { tasks } = values;
            for (let i = 0; i < tasks.length; i += 1) {
                const task = tasks[i];
                await axios.post('/contest_task_relationship/', {
                    task: task.id,
                    contest: id,
                    ordering_number: i,
                    cost: task.cost,
                    main_tag: task.main_tag,
                });
            }

            this.setState({
                redirect: `/contests/${id}/`,
            });
        } catch (error) {
            const errorData = error.response.data;
            Object.keys(errorData).forEach((key) => {
                actions.setFieldError(key, errorData[key]);
                actions.setFieldTouched(key, true, false);
            });
            actions.setSubmitting(false);
        }
    };

    render() {
        if (this.state.redirect !== null) {
            return <Redirect to={this.state.redirect} />;
        }

        return (
            <Component
                handleSubmit={this.handleSubmit}
                handleChange={this.handleChange}
                contest={this.state.contest}
            />
        );
    }
}

export default ContestCreateContainer;

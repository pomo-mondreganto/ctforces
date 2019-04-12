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
            old_tasks: [],
        };
    }

    async componentDidMount() {
        const { id } = this.props.match.params;
        const response = await axios.get(`/contests/${id}/full/`);
        const contest = response.data;
        this.setState({
            contest,
            old_relationships: contest.contest_task_relationship_details.map(relationship => ({
                task: relationship.task,
                id: relationship.id,
            })),
        });
    }

    handleSubmit = async ({ values, actions }) => {
        try {
            for (let i = 0; i < this.state.old_relationships.length; i += 1) {
                if (!values.tasks.map(task => task.id).includes(
                    this.state.old_relationships[i].task,
                )) {
                    await axios.delete(`/contest_task_relationship/${this.state.old_relationships[i].id}/`);
                }
            }

            const response = await axios.put(`/contests/${this.state.contest.id}/`, {
                ...values,
                tasks: values.tasks.map(task => ({
                    ...task,
                    main_tag: task.main_tag.id,
                })),
                start_time: values.start_time.toISOString(),
                end_time: values.end_time.toISOString(),
            });
            const { id } = response.data;

            const { tasks } = values;
            for (let i = 0; i < tasks.length; i += 1) {
                const task = tasks[i];
                if (!this.state.old_relationships.map(relationship => relationship.task).includes(
                    task.id,
                )) {
                    await axios.post('/contest_task_relationship/', {
                        task: task.id,
                        contest: id,
                        ordering_number: i,
                        cost: task.cost,
                        main_tag: task.main_tag.id,
                    });
                } else {
                    const relationshipId = this.state.old_relationships.filter(
                        relationship => relationship.task === task.id,
                    )[0];
                    await axios.put(`/contest_task_relationship/${relationshipId}/`, {
                        ordering_number: i,
                        cost: task.cost,
                        main_tag: task.main_tag.id,
                    });
                }
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

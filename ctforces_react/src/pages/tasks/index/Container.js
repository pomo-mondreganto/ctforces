import React from 'react';

import Component from './Component';

import axios from 'axios';

class TaskViewContainer extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            task: null
        };
    }

    async componentDidMount() {
        const { id } = this.props.match.params;
        const response = await axios.get(`/tasks/${id}/`);
        this.setState({
            task: response.data
        });
    }

    render() {
        return <Component task={this.state.task} />;
    }
}

export default TaskViewContainer;

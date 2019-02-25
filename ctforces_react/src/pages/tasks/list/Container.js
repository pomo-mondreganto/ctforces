import React from 'react';


import axios from 'axios';
import Component from './Component';

class TaskListContainer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            tasks: null,
        };
    }

    async componentDidMount() {
        const response = await axios.get('/tasks/');
        const { data } = response;
        this.setState({
            tasks: data.results,
        });
    }

    render() {
        return <Component tasks={this.state.tasks} />;
    }
}

export default TaskListContainer;

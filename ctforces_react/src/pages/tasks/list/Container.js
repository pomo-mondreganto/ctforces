import React from 'react';

import axios from 'axios';
import qs from 'lib/qs';
import Component from './Component';

class TaskListContainer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            tasks: null,
        };
    }

    async componentDidMount() {
        const { page: currentPage = 1 } = qs(this.props.location.search);
        const response = await axios.get(`/tasks/?page=${currentPage}`);
        const { data } = response;
        const { page_size: pageSize, count, results: tasks } = data;
        this.setState({
            count,
            tasks,
            currentPage,
            pageSize,
        });
    }

    render() {
        return <Component
            tasks={this.state.tasks}
            currentPage={this.state.currentPage}
            count={this.state.count}
            pageSize={this.state.pageSize} />;
    }
}

export default TaskListContainer;

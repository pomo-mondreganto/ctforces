import React from 'react';

import axios from 'axios';
import qs from 'lib/qs';
import Component from './Component';

class TaskSolvedContainer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    async componentDidMount() {
        const { id } = this.props.match.params;
        const { page: currentPage = 1 } = qs(this.props.location.search);
        const response = await axios.get(`/tasks/${id}/solved/?page=${currentPage}`);
        const { data } = response;
        const { page_size: pageSize, count, results: users } = data;
        this.setState({
            count,
            users,
            currentPage,
            pageSize,
            id,
        });
    }

    render() {
        return <Component
            taskId={this.state.id}
            users={this.state.users}
            currentPage={this.state.currentPage}
            count={this.state.count}
            pageSize={this.state.pageSize} />;
    }
}

export default TaskSolvedContainer;

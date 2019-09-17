import React from 'react';

import axios from 'axios';
import qs from 'lib/qs';
import Component from './Component';

class ContestTaskSolvedContainer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    async componentDidMount() {
        const { id, task_id: taskId } = this.props.match.params;
        const { page: currentPage = 1 } = qs(this.props.location.search);
        const response = await axios.get(`/contests/${id}/tasks/${taskId}/solved/?page=${currentPage}`);
        const { data } = response;
        const { page_size: pageSize, count, results: users } = data;
        this.setState({
            count,
            users,
            currentPage,
            pageSize,
            id,
            taskId,
        });
    }

    render() {
        return <Component
            taskId={this.state.taskId}
            contestId={this.state.id}
            users={this.state.users}
            currentPage={this.state.currentPage}
            count={this.state.count}
            pageSize={this.state.pageSize} />;
    }
}

export default ContestTaskSolvedContainer;

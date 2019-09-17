import React from 'react';

import axios from 'axios';
import qs from 'lib/qs';
import withAuth from 'wrappers/withAuth';
import Component from './Component';


class UserTasksPage extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            user: null,
        };
    }

    async componentDidMount() {
        const { username } = this.props.match.params;
        const { page: currentPage = 1 } = qs(this.props.location.search);
        const responseTasks = await axios.get(`/users/${username}/tasks/?page=${currentPage}`);
        const { page_size: pageSize, count, results: tasks } = responseTasks.data;
        this.setState({
            pageSize,
            currentPage,
            count,
            tasks,
        });
    }

    render() {
        return (
            <Component
                user={this.state.user}
                auth={this.props.auth}
                username={this.props.match.params.username}
                tasks={this.state.tasks}
                currentPage={this.state.currentPage}
                count={this.state.count}
                pageSize={this.state.pageSize}
            />
        );
    }
}

export default withAuth(UserTasksPage);

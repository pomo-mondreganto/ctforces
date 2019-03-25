import React from 'react';

import axios from 'axios';
import queryString from 'querystring';
import Component from './Component';
import withAuth from '../../../wrappers/withAuth';


class UserTasksPage extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            user: null,
        };
    }

    async componentDidMount() {
        const { username } = this.props.match.params;
        const { page: currentPage = 1 } = queryString.parse(this.props.location.search);
        const responseUser = await axios.get(`/users/${username}/`);
        const responseTasks = await axios.get(`/users/${username}/tasks/?page=${currentPage}`);
        const { page_size: pageSize, count, results: tasks } = responseTasks.data;
        this.setState({
            user: responseUser.data,
            pageSize,
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

import React from 'react';

import axios from 'axios';
import queryString from 'querystring';
import withAuth from 'wrappers/withAuth';
import Component from './Component';


class UserPostsPage extends React.Component {
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
        const responseTasks = await axios.get(`/users/${username}/posts/?page=${currentPage}`);
        const { page_size: pageSize, count, results: posts } = responseTasks.data;
        this.setState({
            user: responseUser.data,
            pageSize,
            currentPage,
            count,
            posts,
        });
    }

    render() {
        return (
            <Component
                user={this.state.user}
                auth={this.props.auth}
                username={this.props.match.params.username}
                posts={this.state.posts}
                currentPage={this.state.currentPage}
                count={this.state.count}
                pageSize={this.state.pageSize}
            />
        );
    }
}

export default withAuth(UserPostsPage);

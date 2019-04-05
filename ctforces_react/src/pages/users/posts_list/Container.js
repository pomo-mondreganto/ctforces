import React from 'react';

import axios from 'axios';
import qs from 'lib/qs';
import withAuth from 'wrappers/withAuth';
import Component from './Component';


class UserPostsPage extends React.Component {
    constructor(props) {
        super(props);

        this.state = {};
    }

    async componentDidMount() {
        const { username } = this.props.match.params;
        const { page: currentPage = 1 } = qs(this.props.location.search);
        const responsePosts = await axios.get(`/users/${username}/posts/?page=${currentPage}`);
        const { page_size: pageSize, count, results: posts } = responsePosts.data;
        this.setState({
            pageSize,
            currentPage,
            count,
            posts,
        });
    }

    render() {
        return (
            <Component
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

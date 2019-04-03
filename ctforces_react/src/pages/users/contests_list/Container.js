import React from 'react';

import axios from 'axios';
import qs from 'lib/qs';
import withAuth from 'wrappers/withAuth';
import Component from './Component';


class UserContestsPage extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            user: null,
        };
    }

    async componentDidMount() {
        const { username } = this.props.match.params;
        const { page: currentPage = 1 } = qs(this.props.location.search);
        const responseContests = await axios.get(`/users/${username}/contests/?page=${currentPage}`);

        const { upcoming, running, finished } = responseContests.data;
        const {
            count,
            page_size: pageSize,
            results: finishedContests,
        } = finished;

        this.setState({
            count,
            currentPage,
            pageSize,
            upcoming,
            running,
            finished: finishedContests,
        });
    }

    render() {
        return (
            <Component
                auth={this.props.auth}
                username={this.props.match.params.username}
                {...this.state}
            />
        );
    }
}

export default withAuth(UserContestsPage);

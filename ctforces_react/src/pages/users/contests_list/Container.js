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

    register = async (id) => {
        try {
            await axios.get(`/contests/${id}/register/`);
            const upcoming = this.state.upcoming.map((obj) => {
                if (obj.id === id) {
                    const ret = obj;
                    ret.is_registered = true;
                    return ret;
                }
                return obj;
            });
            const running = this.state.running.map((obj) => {
                if (obj.id === id) {
                    const ret = obj;
                    ret.is_registered = true;
                    return ret;
                }
                return obj;
            });
            this.setState({
                upcoming,
                running,
            });
        } catch (error) { throw Error('Cant register'); }
    }

    render() {
        return (
            <Component
                {...this.props}
                username={this.props.match.params.username}
                register={this.register}
                {...this.state}
            />
        );
    }
}

export default withAuth(UserContestsPage);

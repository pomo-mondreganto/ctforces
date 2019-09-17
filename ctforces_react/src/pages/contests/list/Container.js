import React from 'react';

import axios from 'axios';
import qs from 'lib/qs';
import withAuth from 'wrappers/withAuth';
import Component from './Component';

class ContestListContainer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            tasks: null,
        };
    }

    async componentDidMount() {
        const { page: currentPage = 1 } = qs(this.props.location.search);
        const response = await axios.get(`/contests/?page=${currentPage}`);
        const { data } = response;
        const { upcoming, running, finished } = data;
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
        return <Component {...this.state} {...this.props} register={this.register} />;
    }
}

export default withAuth(ContestListContainer);

import React from 'react';

import axios from 'axios';
import qs from 'lib/qs';
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

    render() {
        return <Component {...this.state} />;
    }
}

export default ContestListContainer;

import React from 'react';

import axios from 'axios';
import qs from 'lib/qs';
import Component from './Component';

class TopRatingContainer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    async componentDidMount() {
        const { page: currentPage = 1 } = qs(this.props.location.search);
        const response = await axios.get(`/users/rating_top/?page=${currentPage}`);
        const { data } = response;
        const { page_size: pageSize, count, results: users } = data;
        this.setState({
            count,
            users,
            currentPage,
            pageSize,
        });
    }

    render() {
        return <Component
            users={this.state.users}
            currentPage={this.state.currentPage}
            count={this.state.count}
            pageSize={this.state.pageSize} />;
    }
}

export default TopRatingContainer;

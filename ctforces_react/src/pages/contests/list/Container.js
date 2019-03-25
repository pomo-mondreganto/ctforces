import React from 'react';

import axios from 'axios';
import queryString from 'querystring';
import Component from './Component';

class TaskListContainer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            tasks: null,
        };
    }

    async componentDidMount() {
        const { page: currentPage = 1 } = queryString.parse(this.props.location.search);
        const response = await axios.get(`/contests/?page=${currentPage}`);
        const { data } = response;
        const { page_size: pageSize, count, results: contests } = data;
        console.log(contests);
        this.setState({
            count,
            contests,
            currentPage,
            pageSize,
        });
    }

    render() {
        return <Component
            contests={this.state.contests}
            currentPage={this.state.currentPage}
            count={this.state.count}
            pageSize={this.state.pageSize} />;
    }
}

export default TaskListContainer;

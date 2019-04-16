import React from 'react';

import axios from 'axios';
import qs from 'lib/qs';
import Component from './Component';

class ContestViewContainer extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            contest: null,
        };
    }

    async componentDidMount() {
        const { page: currentPage = 1, group_id: groupId } = qs(this.props.location.search);
        const { id } = this.props.match.params;
        const responseContest = await axios.get(`/contests/${id}/`);
        const responseScoreboard = await axios.get(`/contests/${id}/scoreboard/?page=${currentPage}${groupId ? `&group_id=${groupId}` : ''}`);
        const {
            count,
            page_size: pageSize,
        } = responseScoreboard.data.users;
        this.setState({
            contest: responseContest.data,
            scoreboard: responseScoreboard.data.users.results,
            count,
            pageSize,
            currentPage,
        });
    }

    render() {
        return <Component
            {...this.state}
        />;
    }
}

export default ContestViewContainer;

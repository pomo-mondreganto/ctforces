import React from 'react';

import axios from 'axios';
import Component from './Component';


class ContestViewContainer extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            contest: null,
        };
    }

    async componentDidMount() {
        const { id } = this.props.match.params;
        const response = await axios.get(`/contests/${id}/`);
        this.setState({
            contest: response.data,
        });
    }

    render() {
        return <Component contest={this.state.contest} />;
    }
}

export default ContestViewContainer;

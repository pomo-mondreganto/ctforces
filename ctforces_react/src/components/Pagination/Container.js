import React from 'react';
import { withRouter } from 'react-router-dom';
import qs from 'lib/qs';

import Component from './Component';

class PaginationContainer extends React.Component {
    constructor(props) {
        super(props);

        this.state = {};
    }

    recalcState = (props) => {
        if (props.count === undefined) {
            return;
        }

        const pagesCount = Math.max(Math.ceil(props.count / props.pageSize), 1);
        const { currentPage } = props;
        const lastPage = pagesCount;
        const firstPage = 1;
        const left = currentPage > firstPage;
        const right = currentPage < lastPage;
        const pages = [];

        for (let i = Math.max(currentPage - 4, firstPage);
            i <= Math.min(currentPage + 4, lastPage); i += 1) {
            pages.push(i);
        }

        this.setState({
            paginationInfo: {
                currentPage,
                pages,
                left,
                right,
                to: props.to,
            },
        });
    }

    componentDidMount() {
        const params = qs(this.props.location.search);
        if (params.page !== undefined) {
            delete params.page;
        }
        this.setState({
            params,
        });
        this.recalcState(this.props);
    }

    componentDidUpdate(previousProps) {
        if (previousProps !== this.props) {
            this.recalcState(this.props);
        }
    }

    render() {
        if (!this.state.paginationInfo) {
            return null;
        }

        return <Component paginationInfo={this.state.paginationInfo} params={this.state.params} />;
    }
}

export default withRouter(PaginationContainer);

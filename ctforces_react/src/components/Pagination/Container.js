import React from 'react';

import Component from './Component';

class PaginationContainer extends React.Component {
    constructor(props) {
        super(props);

        const pagesCount = Math.ceil(props.count / props.pageSize);
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

        this.state = {
            pages,
            left,
            right,
        };
    }

    render() {
        return <Component paginationInfo={this.state} />;
    }
}

export default PaginationContainer;

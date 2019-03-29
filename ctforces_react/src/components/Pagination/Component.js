import React from 'react';

import { Pagination, PaginationItem, PaginationLink } from 'reactstrap';

import { LinkContainerAuto } from 'lib/LinkContainer';

import 'styles/components/Pagination.scss';

const Component = props => (
    <Pagination className="pagination">
        <PaginationItem disabled={!props.left}>
            <PaginationLink previous />
        </PaginationItem>
        {props.paginationInfo.pages.map((obj, i) => (
            <PaginationItem key={i}>
                <LinkContainerAuto to={`${props.paginationInfo.to}?page=${obj}`}>
                    <PaginationLink>
                        {obj}
                    </PaginationLink>
                </LinkContainerAuto>
            </PaginationItem>
        ))}
        <PaginationItem disabled={!props.right}>
            <PaginationLink next />
        </PaginationItem>
    </Pagination>
);

export default Component;
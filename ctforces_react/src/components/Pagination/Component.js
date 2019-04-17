import React from 'react';

import { Pagination, PaginationItem, PaginationLink } from 'reactstrap';

import queryString from 'query-string';

import { LinkContainerAuto } from 'lib/LinkContainer';

import 'styles/components/Pagination.scss';

const Component = props => (
    <>
        {

            <Pagination className="pagination">
                <PaginationItem disabled={!props.paginationInfo.left}>
                    {props.paginationInfo.left ? (
                        <LinkContainerAuto to={`${props.paginationInfo.to}?page=${
                            parseInt(props.paginationInfo.currentPage, 10) - 1
                        }&${queryString.stringify(props.params)}`}>
                            <PaginationLink previous />
                        </LinkContainerAuto>
                    ) : (
                        <PaginationLink previous />
                    )}

                </PaginationItem>
                {props.paginationInfo.pages.map((obj, i) => (
                    <PaginationItem key={i}>
                        <LinkContainerAuto to={`${props.paginationInfo.to}?page=${obj}&${queryString.stringify(props.params)}`}>
                            <PaginationLink>
                                {obj}
                            </PaginationLink>
                        </LinkContainerAuto>
                    </PaginationItem>
                ))}
                <PaginationItem disabled={!props.paginationInfo.right}>
                    <LinkContainerAuto to={`${props.paginationInfo.to}?page=${
                        parseInt(props.paginationInfo.currentPage, 10) + 1
                    }&${queryString.stringify(props.params)}`}>
                        <PaginationLink next />
                    </LinkContainerAuto>
                </PaginationItem>
            </Pagination>

        }
    </>
);

export default Component;

import React from 'react';

import Layout from 'layouts/sidebar/Container';
import withLayout from 'wrappers/withLayout';

import { Card } from 'reactstrap';
import Pagination from 'components/Pagination/Container';
import { LinkContainerNonActive } from 'lib/LinkContainer';

const Component = props => (
    <Card>
        {props.contests && props.contests.map((obj, i) => (
            <div key={i}>
                <LinkContainerNonActive to={`/contests/${obj.id}/`}>
                    <a>
                        {obj.name}
                    </a>
                </LinkContainerNonActive>
            </div>
        ))}
        {props.contests
            && <Pagination to={'/contests/'}
                currentPage={props.currentPage}
                count={props.count}
                pageSize={props.pageSize} />}
    </Card>
);

export default withLayout(Component, Layout);

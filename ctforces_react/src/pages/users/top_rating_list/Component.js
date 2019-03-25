import React from 'react';

import Layout from 'layouts/sidebar/Container';
import withLayout from 'wrappers/withLayout';

import { Card } from 'reactstrap';
import Pagination from 'components/Pagination/Container';
import { LinkContainerNonActive } from 'lib/LinkContainer';

const Component = props => (
    <Card>
        {props.users && props.users.map((obj, i) => (
            <div key={i}>
                <LinkContainerNonActive to={`/users/${obj.username}/`}>
                    <a>
                        {obj.username}
                    </a>
                </LinkContainerNonActive>
            </div>
        ))}
        {props.users
            && <Pagination to="/users/rating/top/"
                currentPage={props.currentPage}
                count={props.count}
                pageSize={props.pageSize} />}
    </Card>
);

export default withLayout(Component, Layout);

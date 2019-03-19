import React from 'react';

import Layout from 'layouts/sidebar/Container';
import withLayout from 'wrappers/withLayout';

import { Card } from 'reactstrap';
import Pagination from 'components/Pagination/Container';
import { LinkContainerNonActive } from 'lib/LinkContainer';

const Component = props => (
    <Card>
        {props.tasks && props.tasks.map((obj, i) => (
            <LinkContainerNonActive to={`/tasks/${obj.id}/`} key={i}>
                <a>
                    {obj.name}
                </a>
            </LinkContainerNonActive>
        ))}
        {props.tasks
            && <Pagination currentPage={props.currentPage}
                count={props.count}
                pageSize={props.pageSize} />}
    </Card>
);

export default withLayout(Component, Layout);

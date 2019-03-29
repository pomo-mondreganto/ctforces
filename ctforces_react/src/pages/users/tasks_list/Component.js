import React from 'react';

import { LinkContainerNonActive } from 'lib/LinkContainer';
import Pagination from 'components/Pagination/Container';
import {
    Button, CardBody, CardFooter, Row, Table,
} from 'reactstrap';
import withLayout from 'wrappers/withLayout';
import Layout from 'layouts/sidebar/Container';
import CardWithTabsComponent from 'components/CardWithTabs/Container';

import 'styles/pages/users.scss';

const Component = props => (
    <CardWithTabsComponent
        tabs={[
            {
                text: props.username,
                href: `/users/${props.username}`,
            },
            { text: 'Blog', href: `/users/${props.username}/posts/` },
            { text: 'Tasks', href: `/users/${props.username}/tasks/` },
            { text: 'General', href: '/settings/general/' },
            { text: 'Social', href: '/settings/social/' },
        ]}
    >
        <CardBody>
            <Table>
                <thead className="thead-light">
                    <tr>
                        <th className="border-right text-center" style={{ width: '6%' }}>#</th>
                        <th className="border-left border-right text-center" style={{ width: '54%' }}>Name</th>
                        <th className="border-left border-right text-center" style={{ width: '6%' }}>Cost</th>
                        <th className="border-left border-right text-center" style={{ width: '20%' }}>Tags</th>
                        <th style={{ width: '8%' }} className="text-center border-left">Solved</th>
                    </tr>
                </thead>
                <tbody>
                    {props.tasks && props.tasks.map((obj, i) => (
                        <tr key={i}>
                            <td className="border-right text-center align-middle">{i + 1 + props.pageSize * (props.currentPage - 1)}</td>
                            <td className="border-left border-right align-middle">
                                <LinkContainerNonActive to={`/tasks/${obj.id}/`}>
                                    <a>
                                        {obj.name}
                                    </a>
                                </LinkContainerNonActive>
                            </td>
                            <td className="border-left border-right align-middle text-center">
                                {obj.cost}
                            </td>
                            <td className="border-left border-right align-middle">
                                <Row className="justify-content-center">
                                    {obj.task_tags_details.map((tag, j) => (
                                        <Button style={{ marginTop: '2px', marginBottom: '2px' }} className="btn-sm" outline
                                            color="secondary" key={j}>
                                            {tag.name}
                                        </Button>
                                    ))}
                                </Row>
                            </td>
                            <td className="text-center border-left align-middle">
                                <LinkContainerNonActive to={`/tasks/${obj.id}/solved/`}>
                                    <a>
                                        {obj.solved_count}
                                    </a>
                                </LinkContainerNonActive>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </Table>
            <CardFooter>
                {
                    props.tasks
                    && <Pagination to={`/user/${props.username}/tasks/`}
                        currentPage={props.currentPage}
                        count={props.count}
                        pageSize={props.pageSize} />
                }
            </CardFooter>
        </CardBody>
    </CardWithTabsComponent>
);

export default withLayout(Component, Layout);

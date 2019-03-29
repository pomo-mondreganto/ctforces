import React from 'react';

import Layout from 'layouts/sidebar/Container';
import withLayout from 'wrappers/withLayout';

import {
    Button, Card, CardBody, CardFooter, CardTitle, Row, Table,
} from 'reactstrap';
import Pagination from 'components/Pagination/Container';
import { LinkContainerNonActive } from 'lib/LinkContainer';

const Component = props => (
    <Card>
        <CardBody>
            <CardTitle className="mb-4"><p className="h3 text-center">Tasks</p></CardTitle>
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
                                        <Button style={{ marginTop: '2px', marginBottom: '2px' }} className="btn-sm"
                                            outline color="secondary" key={j}>
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
        </CardBody>
        <CardFooter>
            {
                props.tasks
                && <Pagination to={'/tasks/'}
                    currentPage={props.currentPage}
                    count={props.count}
                    pageSize={props.pageSize} />
            }
        </CardFooter>
    </Card >
);

export default withLayout(Component, Layout);

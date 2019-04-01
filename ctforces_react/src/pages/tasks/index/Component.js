import React from 'react';

import {
    Button, Card, CardBody, CardSubtitle, CardTitle,
} from 'reactstrap';
import getRank from 'lib/Ranking';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEdit } from '@fortawesome/free-solid-svg-icons';
import Layout from 'layouts/sidebar/Container';
import withLayout from 'wrappers/withLayout';

import { LinkContainerNonActive } from 'lib/LinkContainer';

const Component = ({ task }) => (
    <Card>
        {task !== null && (
            <CardBody>
                <CardTitle className="th1">
                    {task.name}
                </CardTitle>
                <CardSubtitle className="pt-3">
                    <div>
                        By {' '}
                        <LinkContainerNonActive
                            to={`/users/${task.author_username}/`}>
                            <a className={getRank(task.author_rating)}>
                                {task.author_username}
                            </a>
                        </LinkContainerNonActive>
                        {task.can_edit_task && (
                            <>
                                {' '}
                                <LinkContainerNonActive
                                    to={`/tasks/${task.id}/edit/`}
                                >
                                    <FontAwesomeIcon icon={faEdit} className="c-p" />
                                </LinkContainerNonActive>
                            </>
                        )}
                    </div>
                    <div className="pt-2">
                        Tags:
                        {task.tags_details.map((tag, i) => (
                            <Button key={i} className="btn-sm ml-1 mr-1" outline
                                color="secondary">
                                {tag.name}
                            </Button>
                        ))}
                    </div>
                </CardSubtitle>
                <hr />
                <div className="long-text">
                    {task.description}
                </div>
                <hr />
                <div>
                    Files:
                    {task.files_details.map((obj, i) => (
                        <div key={i}>
                            <a href={obj.file_field}>{obj.name}</a>
                        </div>
                    ))}
                </div>
            </CardBody>
        )}
    </Card>
);

export default withLayout(Component, Layout);

import React from 'react';

import {Button, Card, CardBody, CardSubtitle, CardText, CardTitle,} from 'reactstrap';
import {getRank, getRankColor} from 'lib/Ranking';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faEdit} from '@fortawesome/free-solid-svg-icons';
import Layout from '../../../layouts/sidebar/Container';
import withLayout from '../../../wrappers/withLayout';

import {LinkContainerNonActive} from '../../../lib/LinkContainer';

const Component = ({ task }) => (
    <Card className="p-2">
        {task !== null && (
            <CardBody>
                <CardTitle className="h2">
                    {task.name}
                </CardTitle>
                <CardSubtitle>
                    <p>
                        By <span style={{
                        color: getRankColor(getRank(task.author_rating)),
                    }}>
                            <LinkContainerNonActive
                                to={`/users/${task.author_username}/`}
                            >
                                <span>
                                    {task.author_username}
                                </span>
                            </LinkContainerNonActive>
                        </span> {' '}
                        {task.can_edit_task && (
                            <LinkContainerNonActive
                                to={`/posts/${task.id}/edit/`}
                            >
                                <FontAwesomeIcon icon={faEdit}/>
                            </LinkContainerNonActive>
                        )}</p>
                    Tags:
                    {task.tags_details.map((tag, i) => (
                        <Button key={i} style={{marginTop: '2px', marginBottom: '2px'}} className="btn-sm ml-2" outline
                                color="secondary">
                            {tag.name}
                        </Button>
                    ))}
                </CardSubtitle>
                <div>
                </div>
                <div>
                    Files:
                    {task.files_details.map((obj, i) => (
                        <div key={i}>
                            <a href={obj.file_field}>{obj.name}</a>
                        </div>
                    ))}
                </div>
                <hr />
                <CardText>
                    {task.description}
                </CardText>
            </CardBody>
        )}
    </Card>
);

export default withLayout(Component, Layout);

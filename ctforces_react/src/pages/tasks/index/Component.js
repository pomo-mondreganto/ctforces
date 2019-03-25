import React from 'react';

import { Card } from 'reactstrap';
import Layout from '../../../layouts/sidebar/Container';
import withLayout from '../../../wrappers/withLayout';

import { LinkContainerNonActive } from '../../../lib/LinkContainer';

const Component = ({ task }) => (
    <Card className="p-2">
        {task !== null && (
            <>
                <div className="py-2">
                    <span style={{ fontSize: '2rem' }}>
                        {`${task.name} by ${task.author_username}`}
                    </span>
                </div>
                <div>
                    <span style={{ fontSize: '2rem' }}>
                        {`Cost: ${task.cost}`}
                    </span>
                </div>
                <div>
                    Tags:
                    {task.tags_details.map((obj, i) => <div key={i}>{obj.name}</div>)}
                </div>
                <div>
                    Files:
                    {task.files_details.map((obj, i) => (
                        <div key={i}>
                            <a href={obj.file_field}>{obj.name}</a>
                        </div>
                    ))}
                </div>
                {task.can_edit_task && (
                    <div className="py-2">
                        <LinkContainerNonActive
                            to={`/tasks/${task.id}/edit/`}
                        >
                            <a>Edit task</a>
                        </LinkContainerNonActive>
                    </div>
                )}
                <hr />
                <div className="py-2">
                    <span style={{ fontSize: '2rem' }}>
                        {task.description}
                    </span>
                </div>
            </>
        )}
    </Card>
);

export default withLayout(Component, Layout);

import React from 'react';

import { Card } from 'reactstrap';
import Layout from '../../../layouts/sidebar/Container';
import withLayout from '../../../wrappers/withLayout';

import { LinkContainerNonActive } from '../../../lib/LinkContainer';

const Component = ({ contest }) => (
    <Card className="p-2">
        {contest !== null && (
            <>
                <div className="py-2">
                    <span style={{ fontSize: '2rem' }}>
                        {`${contest.name} by ${contest.author_username}`}
                    </span>
                </div>

                {contest.can_edit_contest && (
                    <div className="py-2">
                        <LinkContainerNonActive
                            to={`/contests/${contest.id}/edit`}
                        >
                            <a>Edit contest</a>
                        </LinkContainerNonActive>
                    </div>
                )}
                <hr />
                <div>
                    Tasks:
                    {contest.contest_task_relationship_details.map(
                        (obj, i) => (
                            <div key={i}>
                                <span>{obj.task_name}</span>
                                <span>{obj.cost}</span>
                                <span>{obj.main_tag_name}</span>
                            </div>
                        ),
                    )}
                </div>
            </>
        )}
    </Card>
);

export default withLayout(Component, Layout);

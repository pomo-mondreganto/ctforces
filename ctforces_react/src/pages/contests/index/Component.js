import React from 'react';

import getRank from 'lib/Ranking';
import convert from 'lib/HumanTime';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEdit } from '@fortawesome/free-solid-svg-icons';
import { LinkContainerNonActive } from 'lib/LinkContainer';
import Layout from 'layouts/sidebar/Container';
import withLayout from 'wrappers/withLayout';
import { Button } from 'reactstrap';

import CardWithTabs from 'components/CardWithTabs/Container';

import 'styles/pages/tasks.scss';

const Component = ({ contest }) => (
    <CardWithTabs
        tabs={[
            { text: 'Tasks', href: `/contests/${contest ? contest.id : ''}/` },
            { text: 'Scoreboard', href: `/contests/${contest ? contest.id : ''}/scoreboard/` },
        ]}
    >
        {contest !== null && (
            <>
                <div className="th1">
                    {contest.name}
                </div>
                <div className="mt-3">
                    By {' '}
                    <LinkContainerNonActive to={`/users/${contest.author_username}/`} >
                        <a className={getRank(contest.author_rating)}>
                            {contest.author_username}
                        </a>
                    </LinkContainerNonActive>
                    , {convert(contest.created_at)}
                    {' '}
                    {contest.can_edit_contest && (
                        <>
                            {' '}
                            <LinkContainerNonActive
                                to={`/contests/${contest.id}/edit/`}
                            >
                                <FontAwesomeIcon icon={faEdit} className="c-p" />
                            </LinkContainerNonActive>
                        </>
                    )}
                </div>
                <div className="tasks-table mt-4">
                    <div className="tasks-table-head">
                        <span className="ta-c">#</span>
                        <span className="ta-l">Name</span>
                        <span className="ta-c">Cost</span>
                        <span className="ta-c">Tags</span>
                        <span className="ta-c">Solved</span>
                    </div>
                    <div className="tasks-table-body">
                        {contest.contest_task_relationship_details.map((obj, i) => (
                            <div key={i} className={`tasks-table-item 
                                                         ${obj.is_solved_by_user ? 'solved' : ''}`}>
                                <span className="ta-c">{i + 1}</span>
                                <span className="ta-l">
                                    <LinkContainerNonActive to={`/contests/${contest.id}/tasks/${i + 1}/`}>
                                        <a>
                                            {obj.task_name}
                                        </a>
                                    </LinkContainerNonActive>
                                </span>
                                <span className="ta-c">
                                    {obj.cost}
                                </span>
                                <span className="ta-c">
                                    <span>
                                        <Button className="btn-sm mr-1 ml-1"
                                            outline color="secondary">
                                            {obj.main_tag_details.name}
                                        </Button>
                                    </span>
                                </span>
                                <span className="ta-c">
                                    <LinkContainerNonActive to={`/contests/${contest.id}/tasks/${i + 1}/solved/`}>
                                        <a>
                                            {obj.solved_count}
                                        </a>
                                    </LinkContainerNonActive>
                                </span>
                            </div>
                        ))}
                    </div>
                </div>
            </>
        )}
    </CardWithTabs>
);

export default withLayout(Component, Layout);

import React from 'react';

import getRank from 'lib/Ranking';
import convert from 'lib/HumanTime';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEdit } from '@fortawesome/free-solid-svg-icons';
import { LinkContainerNonActive } from 'lib/LinkContainer';
import Layout from 'layouts/sidebar/Container';
import withLayout from 'wrappers/withLayout';
import Pagination from 'components/Pagination/Container';

import CardWithTabs from 'components/CardWithTabs/Container';

import 'styles/pages/users.scss';

const Component = ({
    contest, scoreboard, currentPage, count, pageSize,
}) => (
    <CardWithTabs
        tabs={[
            { text: 'Tasks', href: `/contests/${contest ? contest.id : ''}/` },
            { text: 'Scoreboard', href: `/contests/${contest ? contest.id : ''}/scoreboard/` },
        ]}
        pagination={
            <Pagination to={`/contests/${contest ? contest.id : ''}/scoreboard/`}
                currentPage={currentPage}
                count={count}
                pageSize={pageSize} />
        }
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
                    <div className="users-table mt-4">
                        <div className="users-table-head">
                            <span className="ta-c">#</span>
                            <span className="ta-l">Username</span>
                            <span className="ta-c">Points</span>
                        </div>
                        <div className="users-table-body">
                            {scoreboard && scoreboard.map((obj, i) => (
                                <div key={i} className='users-table-item'>
                                    <span className="ta-c">{i + 1}</span>
                                    <span className="ta-l">
                                        <LinkContainerNonActive to={`/users/${obj.username}/`}>
                                            <a className={getRank(obj.rating)}>
                                                {obj.username}
                                            </a>
                                        </LinkContainerNonActive>
                                    </span>
                                    <span className="ta-c">
                                        {obj.cost_sum}
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

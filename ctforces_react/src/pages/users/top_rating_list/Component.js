import React from 'react';

import Layout from 'layouts/sidebar/Container';
import withLayout from 'wrappers/withLayout';

import CardWithTabs from 'components/CardWithTabs/Container';
import Pagination from 'components/Pagination/Container';
import { LinkContainerNonActive } from 'lib/LinkContainer';

import getRank from 'lib/Ranking';

const Component = props => (
    <CardWithTabs
        title="Rating"
        pagination={
            <Pagination to="/users/rating/top/"
                currentPage={props.currentPage}
                count={props.count}
                pageSize={props.pageSize} />
        }
    >
        <div className="tasks-table">
            <div className="users-table-head">
                <span className="ta-c">#</span>
                <span className="ta-l">Username</span>
                <span className="ta-c">Rating</span>
            </div>
            <div className="users-table-body">
                {props.users && props.users.map((obj, i) => (

                    <div key={i} className="users-table-item">
                        <span className="ta-c">{i + 1 + props.pageSize * (props.currentPage - 1)}</span>
                        <span className="ta-l">
                            <LinkContainerNonActive to={`/users/${obj.username}/`}>
                                <a className={getRank(obj.rating)}>
                                    {obj.username}
                                </a>
                            </LinkContainerNonActive>
                        </span>
                        <span className="ta-c">{obj.rating}</span>
                    </div>
                ))}
            </div>
        </div>
    </CardWithTabs>
);

export default withLayout(Component, Layout);

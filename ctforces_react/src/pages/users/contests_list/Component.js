import React from 'react';

import Layout from 'layouts/sidebar/Container';
import withLayout from 'wrappers/withLayout';

import CardWithTabs from 'components/CardWithTabs/Container';
import Pagination from 'components/Pagination/Container';
import { LinkContainerNonActive } from 'lib/LinkContainer';

import UserTopBar from 'snippets_components/UserTopBar';

import 'styles/pages/contests.scss';

const Component = props => (
    <CardWithTabs
        tabs={UserTopBar(props.username)}
        pagination={
            <>
                {
                    props.finished
                    && <Pagination to={`/users/${props.username}/contests/`}
                        currentPage={props.currentPage}
                        count={props.count}
                        pageSize={props.pageSize} />
                }
            </>
        }
    >
        {props.running && (
            <>
                <div className="th3 mb-3">Running</div>
                <div className="contests-table mb-5">
                    <div className="contests-table-head">
                        <span className="ta-c">#</span>
                        <span className="ta-l">Name</span>
                    </div>
                    <div className="contests-table-body">
                        {props.running.map((obj, i) => (
                            <div key={i} className="contests-table-item">
                                <span className="ta-c">{i + 1}</span>
                                <span className="ta-l">
                                    <LinkContainerNonActive to={`/contests/${obj.id}/`}>
                                        <a>
                                            {obj.name}
                                        </a>
                                    </LinkContainerNonActive>
                                </span>
                            </div>
                        ))}
                    </div>
                </div>
            </>
        )}

        {props.upcoming && (
            <>
                <div className="th3 mb-3">Upcoming</div>
                <div className="contests-table mb-5">
                    <div className="contests-table-head">
                        <span className="ta-c">#</span>
                        <span className="ta-l">Name</span>
                    </div>
                    <div className="contests-table-body">
                        {props.upcoming.map((obj, i) => (
                            <div key={i} className="contests-table-item">
                                <span className="ta-c">{i + 1}</span>
                                <span className="ta-l">
                                    <LinkContainerNonActive to={`/contests/${obj.id}/`}>
                                        <a>
                                            {obj.name}
                                        </a>
                                    </LinkContainerNonActive>
                                </span>
                            </div>
                        ))}
                    </div>
                </div>
            </>
        )}

        {props.finished && (
            <>
                <div className="th3 mb-3">Finished</div>
                <div className="contests-table">
                    <div className="contests-table-head">
                        <span className="ta-c">#</span>
                        <span className="ta-l">Name</span>
                    </div>
                    <div className="contests-table-body">
                        {props.finished.map((obj, i) => (
                            <div key={i} className="contests-table-item">
                                <span className="ta-c">{i + 1 + props.pageSize * (props.currentPage - 1)}</span>
                                <span className="ta-l">
                                    <LinkContainerNonActive to={`/contests/${obj.id}/`}>
                                        <a>
                                            {obj.name}
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

import React from 'react';

import { LinkContainerNonActive } from 'lib/LinkContainer';
import Pagination from 'components/Pagination/Container';
import withLayout from 'wrappers/withLayout';
import Layout from 'layouts/sidebar/Container';
import CardWithTabsComponent from 'components/CardWithTabs/Container';
import getRank from 'lib/Ranking';
import convert from 'lib/HumanTime';
import Markdown from 'components/Markdown/Container';

import UserTopBar from 'snippets_components/UserTopBar';

import 'styles/pages/users.scss';
import 'styles/pages/posts.scss';

const Component = props => (
    <CardWithTabsComponent
        tabs={UserTopBar(props.username, props.auth)}

        pagination={
            <Pagination to={`/users/${props.username}/posts/`}
                currentPage={props.currentPage}
                count={props.count}
                pageSize={props.pageSize} />
        }
    >
        <>
            {props.posts && props.posts.map((obj, i) => (
                <div key={i} className={`${i ? 'mt-5' : ''}`}>
                    <div className="th1">
                        <LinkContainerNonActive to={`/posts/${obj.id}/`}>
                            <a>{obj.title}</a>
                        </LinkContainerNonActive>
                    </div>
                    <div className="mt-3">
                        By {' '}
                        <LinkContainerNonActive to={`/users/${obj.author_username}/`} >
                            <a className={getRank(obj.author_rating)}>
                                {obj.author_username}
                            </a>
                        </LinkContainerNonActive>
                        , {convert(obj.created_at)}
                    </div>

                    <hr />
                    <div className="py-2 long-text">
                        <Markdown text={obj.body} />
                    </div>
                </div>
            ))}

        </>
    </CardWithTabsComponent>
);

export default withLayout(Component, Layout);

import React from 'react';

import { LinkContainerNonActive } from 'lib/LinkContainer';

import { serverUrl } from 'config/config';
import CardWithTabs from 'components/CardWithTabs/Container';
import getRank from 'lib/ranking';

import 'styles/components/Sidebar.scss';
import 'styles/pages/users.scss';

const Component = (props) => {
    const { user } = props.auth;
    return (
        <aside id="sidebar">
            {props.auth.requested && props.auth.loggedIn && (
                <CardWithTabs>
                    <div id="sidebar-main" className="th4">{user.username}</div>
                    <hr />
                    <div id="user-info">
                        <div id="sidebar-bullets">
                            <div>
                                Rating: <span className={getRank(user.rating)}>{user.rating}</span>
                            </div>
                            <div className="mb-3">
                                Points: <span className={getRank(user.rating)}>
                                    {user.cost_sum}
                                </span>
                            </div>
                            <ul className="ml-1 pl-3">
                                <li>
                                    <LinkContainerNonActive to={`/users/${user.username}/`}>
                                        <a>
                                            Profile
                                        </a>
                                    </LinkContainerNonActive>
                                </li>
                                {user.has_posts && (
                                    <li>
                                        <LinkContainerNonActive to={`/users/${user.username}/posts/`}>
                                            <a>
                                                Blog
                                            </a>
                                        </LinkContainerNonActive>
                                    </li>
                                )}
                                {user.has_tasks && (
                                    <li>
                                        <LinkContainerNonActive to={`/users/${user.username}/tasks/`}>
                                            <a>
                                                Tasks
                                            </a>
                                        </LinkContainerNonActive>
                                    </li>
                                )}
                                {user.has_contests && (
                                    <li>
                                        <LinkContainerNonActive to={`/users/${user.username}/contests/`}>
                                            <a>
                                                Contests
                                            </a>
                                        </LinkContainerNonActive>
                                    </li>
                                )}
                                <li>
                                    <LinkContainerNonActive to={'/settings/general/'}>
                                        <a>
                                            Settings
                                        </a>
                                    </LinkContainerNonActive>
                                </li>
                            </ul>
                        </div>
                        <div id="sidebar-avatar">
                            <img

                                className="p-3"
                                src={`${serverUrl}${user.avatar_small}`}
                            />
                        </div>
                    </div>
                </CardWithTabs >
            )}
            {props.topUsers && (
                <div className="mt-4">
                    <CardWithTabs>
                        <div className="th3 mb-3 ta-c">Top users</div>
                        <div className="tasks-table">
                            <div className="users-table-head">
                                <span className="ta-c">#</span>
                                <span className="ta-l">Username</span>
                                <span className="ta-c">Rating</span>
                            </div>
                            <div className="users-table-body">
                                {props.topUsers && props.topUsers.map((obj, i) => (

                                    <div key={i} className="users-table-item">
                                        <span className="ta-c">{i + 1}</span>
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
                </div>
            )}
        </aside >
    );
};

export default Component;

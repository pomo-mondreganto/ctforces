import React from 'react';

import { LinkContainerNonActive } from 'lib/LinkContainer';

import { mediaUrl } from 'config/config';
import CardWithTabs from 'components/CardWithTabs/Container';
import getRank from 'lib/Ranking';

import 'styles/components/Sidebar.scss';

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
                                <li>
                                    <LinkContainerNonActive to={`/users/${user.username}/posts/`}>
                                        <a>
                                            Blog
                                        </a>
                                    </LinkContainerNonActive>
                                </li>
                                <li>
                                    <LinkContainerNonActive to={`/users/${user.username}/tasks/`}>
                                        <a>
                                            Tasks
                                        </a>
                                    </LinkContainerNonActive>
                                </li>
                                <li>
                                    <LinkContainerNonActive to={`/users/${user.username}/contests/`}>
                                        <a>
                                            Contests
                                        </a>
                                    </LinkContainerNonActive>
                                </li>
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
                                src={`${mediaUrl}${user.avatar_small}`}
                            />
                        </div>
                    </div>
                </CardWithTabs >
            )
            }
        </aside >
    );
};

export default Component;

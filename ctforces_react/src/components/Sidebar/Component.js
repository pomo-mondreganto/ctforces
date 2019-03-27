import React from 'react';

import {Card, CardHeader} from 'reactstrap';
import {LinkContainerNonActive} from 'lib/LinkContainer';

import {mediaUrl} from '../../../config/config';
import './styles.scss';

const Component = (props) => {
    const { user } = props.auth;
    return (
        <aside id="sidebar">
            {props.auth.requested && props.auth.loggedIn && (
                <Card className="mb-2" id="user-info">
                    <CardHeader id="main">{user.username}</CardHeader>
                    <div id="bullets" className="p-3">
                        <p className="my-0" style={{fontSize: '0.87rem'}}>Rating: <strong>{user.rating}</strong></p>
                        <p style={{fontSize: '0.87rem'}}>Points: <strong>{user.cost_sum}</strong></p>
                        <ul className="ml-1 pl-4" style={{fontSize: '0.9rem'}}>
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
                    <img
                        id="avatar"
                        className="w-100 h-auto p-3"
                        src={`${mediaUrl}${user.avatar_small}`}
                    />
                </Card>
            )}
        </aside>
    );
};

export default Component;

import React from 'react';

import { Card } from 'reactstrap';

import { mediaUrl } from '../../../config/config';
import './styles.scss';

const Component = (props) => {
    const { user } = props.auth;
    return (
        <aside id="sidebar">
            {props.auth.requested && props.auth.loggedIn && (
                <Card className="mb-2" id="user-info">
                    <div id="bullets" className="p-3">
                        <span>{user.username}</span>
                        <p className="my-0">{`Rating: ${user.rating}`}</p>
                        <p>{`Points: ${user.cost_sum}`}</p>
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

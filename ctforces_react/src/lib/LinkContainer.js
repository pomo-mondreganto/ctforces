import React from 'react';

import { LinkContainer } from 'react-router-bootstrap';

const LinkContainerAuto = props => {
    return <LinkContainer exact {...props} />;
};

const LinkContainerNonActive = props => {
    return (
        <LinkContainer
            {...props}
            isActive={() => {
                return false;
            }}
        />
    );
};

export { LinkContainerAuto, LinkContainerNonActive };

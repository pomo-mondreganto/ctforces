import React from 'react';

import { LinkContainer } from 'react-router-bootstrap';

const LinkContainerAuto = props => <LinkContainer exact {...props} />;

const LinkContainerNonActive = props => (
    <LinkContainer
        {...props}
        isActive={() => false}
    />
);

export { LinkContainerAuto, LinkContainerNonActive };

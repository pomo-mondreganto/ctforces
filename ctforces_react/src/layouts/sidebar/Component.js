import React from 'react';

import withLayout from '../../wrappers/withLayout';
import MasterLayout from '../master/Container';

const Component = ({ children }) => {
    return (
        <>
            <main>{children}</main>
            <aside>sidebar</aside>
        </>
    );
};

export default withLayout(Component, MasterLayout);

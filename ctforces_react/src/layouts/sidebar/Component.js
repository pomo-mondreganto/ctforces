import React from 'react';

import withLayout from 'wrappers/withLayout';
import Sidebar from 'components/Sidebar/Container';
import MasterLayout from 'layouts/master/Container';


const Component = ({ children }) => (
    <>
        <main>{children}</main>
        <Sidebar />
    </>
);

export default withLayout(Component, MasterLayout);

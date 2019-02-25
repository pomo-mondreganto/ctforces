import React from 'react';

import withLayout from '../../wrappers/withLayout';
import MasterLayout from '../master/Container';

import Sidebar from '../../components/Sidebar/Container';

const Component = ({ children }) => (
    <>
        <main>{children}</main>
        <Sidebar />
    </>
);

export default withLayout(Component, MasterLayout);

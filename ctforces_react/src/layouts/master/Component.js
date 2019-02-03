import React from 'react';

import MenuComponent from '../../components/Menu/Container';

const Component = ({ children }) => {
    return (
        <>
            <header>
                <MenuComponent />
            </header>
            {children}
        </>
    );
};

export default Component;

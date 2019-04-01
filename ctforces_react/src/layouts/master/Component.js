import React from 'react';

import MenuComponent from 'components/Menu/Container';

const Component = ({ children }) => (
    <>
        <header>
            <MenuComponent />
        </header>
        {children}
        <footer className="ta-c">Powered by <strong>KekusCorporation</strong></footer>
    </>
);

export default Component;

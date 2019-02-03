import React from 'react';

export default (ChildComponent, LayoutComponent) => {
    return props => {
        return (
            <LayoutComponent>
                <ChildComponent {...props} />
            </LayoutComponent>
        );
    };
};

import React from 'react';

const Component = (ChildComponent, LayoutComponent) => function ComponentWithLayout(props) {
    return (
        <LayoutComponent>
            <ChildComponent {...props} />
        </LayoutComponent>);
};

export default Component;

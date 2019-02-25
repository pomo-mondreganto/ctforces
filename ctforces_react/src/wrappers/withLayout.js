import React from 'react';

const Component = (ChildComponent, LayoutComponent) => (props) => {
    const ComponentWithLayout = () => (
        <LayoutComponent>
            <ChildComponent {...props} />
        </LayoutComponent>
    );
    ComponentWithLayout.displayName = 'ComponentWithLayout';
    return ComponentWithLayout;
};

Component.displayName = 'WithLayout';

export default Component;

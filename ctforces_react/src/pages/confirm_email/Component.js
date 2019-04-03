import React from 'react';


import Layout from 'layouts/sidebar/Container';
import withLayout from 'wrappers/withLayout';

import CardWithTabs from 'components/CardWithTabs/Container';

const Component = props => (
    <section>
        <article>
            <CardWithTabs
                title={props.title}
            />
        </article>
    </section>
);

export default withLayout(Component, Layout);

import Link from 'next/link';
import Layout from '../layouts/master.js';
import Router from 'next/router';
import { post, get } from '../lib/api_requests';

const Index = () => (
    <Layout>
        <div />
    </Layout>
);

Index.getInitialProps = async ({ req }) => {
    let a = await post('login', {
        username: 'kek',
        password: 'mem'
    });
    console.log(a);
    return {};
};

export default Index;

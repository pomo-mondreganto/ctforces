import React, { Component } from 'react';
import sidebarLayout from '../../layouts/sidebarLayout';
import withLayout from '../../wrappers/withLayout';
import FormComponent from '../../components/Form';
import { required } from '../../lib/validators';
import { post, get } from '../../lib/api_requests';
import { api_url } from '../../config';
import redirect from '../../lib/redirect';

import { Card } from 'reactstrap';
import SimpleMDEComponent from '../../components/SimpleMDE';

class ViewPost extends Component {
    constructor(props) {
        super(props);
    }

    static async getInitialProps(ctx) {
        let data = await get(`posts/${ctx.query.id}`, {
            ctx: ctx
        });
        data = await data.json();
        return {
            title: data.title,
            body: data.body,
            author_username: data.author_username
        };
    }

    render() {
        return (
            <Card className="p-2">
                <div style={{ fontSize: '2rem' }} className="py-2">
                    {this.props.author_username}
                </div>
                <hr />
                <div style={{ fontSize: '2rem' }} className="py-2">
                    {this.props.title}
                </div>
                <div style={{ fontSize: '2rem' }} className="py-2">
                    {this.props.body}
                </div>
            </Card>
        );
    }
}

export default withLayout(ViewPost, sidebarLayout);

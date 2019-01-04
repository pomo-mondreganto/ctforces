import React, { Component } from 'react';
import sidebarLayout from '../../layouts/sidebarLayout';
import withLayout from '../../wrappers/withLayout';
import FormComponent from '../../components/Form';
import { required } from '../../lib/validators';
import { post, get } from '../../lib/api_requests';
import { api_url } from '../../config';
import redirect from '../../lib/redirect';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChartLine, faMarker } from '@fortawesome/free-solid-svg-icons';
import Link from 'next/link';

import { Card } from 'reactstrap';
import SimpleMDEComponent from '../../components/SimpleMDEInput';

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
            id: data.id,
            title: data.title,
            body: data.body,
            author_username: data.author_username,
            is_published: data.is_published
        };
    }

    render() {
        return (
            <Card className="p-2">
                <div style={{ fontSize: '2rem' }} className="py-2">
                    {this.props.author_username}
                </div>
                {this.props.is_published && (
                    <div className="py-2">
                        <FontAwesomeIcon icon={faMarker} size="lg" />{' '}
                        <Link href={`/post/${this.props.id}/edit`}>
                            <a>Edit post</a>
                        </Link>
                    </div>
                )}
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

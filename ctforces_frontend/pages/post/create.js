import React, { Component } from 'react';
import sidebarLayout from '../../layouts/sidebarLayout';
import withLayout from '../../wrappers/withLayout';
import FormComponent from '../../components/Form';
import { required } from '../../lib/validators';
import { post } from '../../lib/api_requests';
import { api_url } from '../../config';
import redirect from '../../lib/redirect';

import { Card } from 'reactstrap';
import SimpleMDEComponent from '../../components/SimpleMDE';

class CreatePost extends Component {
    constructor(props) {
        super(props);
    }

    onOkSubmit = async ({ title, body }) => {
        let data = await post('posts', {
            data: {
                title: title,
                body: body,
                is_published: false
            }
        });
        if (data.ok) {
            data = await data.json();
            redirect(`post/${data.id}`);
            return { ok: true, errors: {} };
        } else {
            return { ok: false, errors: await data.json() };
        }
    };

    render() {
        return (
            <Card className="p-2">
                <div style={{ fontSize: '2rem' }} className="py-2">
                    Write post
                </div>
                <hr />
                <FormComponent
                    onOkSubmit={this.onOkSubmit}
                    fields={[
                        {
                            name: 'title',
                            type: 'text',
                            placeholder: 'Title',
                            validators: [required]
                        },
                        {
                            source: SimpleMDEComponent,
                            name: 'body',
                            pass_props: {
                                id: 'post_textarea'
                            },
                            validators: [required]
                        }
                    ]}
                />
            </Card>
        );
    }
}

export default withLayout(CreatePost, sidebarLayout);

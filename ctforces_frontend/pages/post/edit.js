import React, {Component} from 'react';
import sidebarLayout from '../../layouts/sidebarLayout';
import withLayout from '../../wrappers/withLayout';
import FormComponent from '../../components/Form';
import {required} from '../../lib/validators';
import {get, post} from '../../lib/api_requests';
import redirect from '../../lib/redirect';

import {Card} from 'reactstrap';
import SimpleMDEComponent from '../../components/SimpleMDEInput';
import CheckBoxComponent from '../../components/CheckBoxInput';

class EditPost extends Component {
    constructor(props) {
        super(props);
    }

    static async getInitialProps(ctx) {
        let data = await get(`posts/${ctx.query.id}`, { ctx: ctx });
        data = await data.json();
        return {
            id: data.id,
            title: data.title,
            body: data.body,
            author_username: data.author_username,
            is_published: data.is_published
        };
    }

    onOkSubmit = async ({ title, body, is_published }) => {
        let data = await post('posts', {
            data: {
                title: title,
                body: body,
                is_published: is_published
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
                    Edit post
                </div>
                <hr />
                <FormComponent
                    onOkSubmit={this.onOkSubmit}
                    fields={[
                        {
                            source: TextInputComponent,
                            initial_value: this.props.title,
                            name: 'title',
                            type: 'text',
                            placeholder: 'Title',
                            validators: [required]
                        },
                        {
                            initial_value: this.props.body,
                            source: SimpleMDEComponent,
                            name: 'body',
                            pass_props: { id: 'post_textarea' },
                            validators: [required]
                        },
                        {
                            initial_value: this.props.is_published,
                            source: CheckBoxComponent,
                            name: 'is_published',
                            pass_props: {
                                label: 'publish'
                            }
                        }
                    ]}
                />
            </Card>
        );
    }
}

export default withLayout(EditPost, sidebarLayout);

import React, {Component} from 'react';
import sidebarLayout from '../../layouts/sidebarLayout';
import withLayout from '../../wrappers/withLayout';
import FormComponent from '../../components/Form';
import {required} from '../../lib/validators';
import {post} from '../../lib/api_requests';
import redirect from '../../lib/redirect';

import {Card} from 'reactstrap';
import SimpleMDEComponent from '../../components/SimpleMDEInput';
import CheckBoxComponent from '../../components/CheckBoxInput';
import TextInputComponent from '../../components/TextInput';

class CreatePost extends Component {
    constructor(props) {
        super(props);
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
                    Write post
                </div>
                <hr />
                <FormComponent
                    onOkSubmit={this.onOkSubmit}
                    fields={[
                        {
                            source: TextInputComponent,
                            name: 'title',
                            type: 'text',
                            placeholder: 'Title',
                            validators: [required]
                        },
                        {
                            source: SimpleMDEComponent,
                            name: 'body',
                            pass_props: { id: 'post_textarea' },
                            validators: [required]
                        },
                        {
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

export default withLayout(CreatePost, sidebarLayout);

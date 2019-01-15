import React, { Component } from 'react';
import sidebarLayout from '../../layouts/sidebarLayout';
import withLayout from '../../wrappers/withLayout';
import FormComponent from '../../components/Form';
import { required } from '../../lib/validators';
import { post } from '../../lib/api_requests';
import redirect from '../../lib/redirect';

import { Card } from 'reactstrap';
import SimpleMDEComponent from '../../components/SimpleMDEInput';
import CheckBoxComponent from '../../components/CheckBoxInput';
import TextInputComponent from '../../components/TextInput';
import FileUploaderComponent from '../../components/FileUploaderInput';
import FileListComponent from '../../components/FileList';
import TagsComponent from '../../components/TagsInput';

class CreatePost extends Component {
    constructor(props) {
        super(props);
    }

    onOkSubmit = async ({
        name,
        cost,
        flag,
        description,
        is_published,
        files,
        tags
    }) => {
        let data = await post('tasks', {
            data: {
                name: name,
                cost: cost,
                flag: flag,
                description: description,
                is_published: is_published,
                files: files,
                tags: tags
            }
        });
        if (data.ok) {
            data = await data.json();
            redirect(`task/${data.id}`);
            return { ok: true, errors: {} };
        } else {
            return { ok: false, errors: await data.json() };
        }
    };

    render() {
        return (
            <Card className="p-2">
                <div style={{ fontSize: '2rem' }} className="py-2">
                    Create task
                </div>
                <hr />
                <FormComponent
                    onOkSubmit={this.onOkSubmit}
                    fields={[
                        {
                            source: TextInputComponent,
                            name: 'name',
                            type: 'text',
                            placeholder: 'Name',
                            validators: [required]
                        },
                        {
                            source: TagsComponent,
                            name: 'tags'
                        },
                        {
                            source: TextInputComponent,
                            name: 'cost',
                            type: 'text',
                            placeholder: 'Cost',
                            validators: [required]
                        },
                        {
                            source: TextInputComponent,
                            name: 'flag',
                            type: 'text',
                            placeholder: 'Flag',
                            validators: [required]
                        },
                        {
                            source: SimpleMDEComponent,
                            name: 'description',
                            pass_props: { id: 'task_textarea' },
                            validators: [required]
                        },
                        {
                            source: CheckBoxComponent,
                            name: 'is_published',
                            pass_props: { label: 'is_published' }
                        },
                        {
                            source: FileUploaderComponent,
                            name: 'files',
                            pass_props: {
                                upload_url: 'task_files',
                                file_upload_name: 'file_field',
                                extract_field: 'id',
                                multiple: true
                            }
                        },
                        {
                            source: FileListComponent,
                            pass_props: {
                                ref_name: 'files'
                            }
                        }
                    ]}
                />
            </Card>
        );
    }
}

export default withLayout(CreatePost, sidebarLayout);

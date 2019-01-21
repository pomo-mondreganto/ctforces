import React, { Component } from 'react';
import sidebarLayout from '../../layouts/sidebarLayout';
import withLayout from '../../wrappers/withLayout';
import FormComponent from '../../components/Form';
import { required } from '../../lib/validators';
import { post, get } from '../../lib/api_requests';
import redirect from '../../lib/redirect';

import { Card } from 'reactstrap';
import SimpleMDEComponent from '../../components/SimpleMDEInput';
import CheckBoxComponent from '../../components/CheckBoxInput';
import TextInputComponent from '../../components/TextInput';
import FileUploaderComponent from '../../components/FileUploaderInput';
import FileListComponent from '../../components/FileList';
import TagsComponent from '../../components/TagsInput';

class CreateTask extends Component {
    constructor(props) {
        super(props);
    }

    static async getInitialProps(ctx) {
        let data = await get(`tasks/${ctx.query.id}/full`, {
            ctx: ctx
        });
        data = await data.json();
        console.log(data);
        return {
            id: data.id,
            title: data.name,
            body: data.description,
            author_username: data.author_username,
            can_edit_task: data.can_edit_task,
            is_solved_by_user: data.is_solved_by_user,
            files: data.files_details,
            cost: data.cost,
            flag: data.flag,
            tags: data.task_tags_details
        };
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
                            validators: [required],
                            initial_value: this.props.title
                        },
                        {
                            source: TagsComponent,
                            name: 'tags',
                            initial_value: this.props.tags
                        },
                        {
                            source: TextInputComponent,
                            name: 'cost',
                            type: 'text',
                            placeholder: 'Cost',
                            validators: [required],
                            initial_value: this.props.cost
                        },
                        {
                            source: TextInputComponent,
                            name: 'flag',
                            type: 'text',
                            placeholder: 'Flag',
                            validators: [required],
                            initial_value: this.props.flag
                        },
                        {
                            source: SimpleMDEComponent,
                            name: 'description',
                            pass_props: { id: 'task_textarea' },
                            validators: [required],
                            initial_value: this.props.body
                        },
                        {
                            source: CheckBoxComponent,
                            name: 'is_published',
                            pass_props: { label: 'is_published' },
                            initial_value: this.props.is_published
                        },
                        {
                            source: FileUploaderComponent,
                            name: 'files',
                            pass_props: {
                                upload_url: 'task_files',
                                file_upload_name: 'file_field',
                                extract_field: 'id',
                                multiple: true
                            },
                            initial_value: this.props.files
                        },
                        {
                            source: FileListComponent,
                            pass_props: { ref_name: 'files' }
                        }
                    ]}
                />
            </Card>
        );
    }
}

export default withLayout(CreateTask, sidebarLayout);

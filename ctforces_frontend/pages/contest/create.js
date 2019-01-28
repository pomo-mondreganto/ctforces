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
import TaskListComponent from '../../components/TaskListInput';
import CalendarComponent from '../../components/CalendarInput';

class CreateContest extends Component {
    constructor(props) {
        super(props);
    }

    onOkSubmit = async ({
        name,
        description,
        contest_files,
        is_published,
        is_rated,
        start_time,
        end_time
    }) => {
        let data = await post('contests', {
            data: {
                name: name,
                description: description,
                is_published: is_published,
                is_rated: is_rated,
                start_time: start_time,
                end_time: end_time
            }
        });
        if (data.ok) {
            data = await data.json();
            let contest_id = data.id;
            for (let i = 0; i < contest_files.length; ++i) {
                post('contest_task_relationship', {
                    data: {
                        task: contest_files[i].id,
                        contest: contest_id,
                        ordering_number: i,
                        cost: contest_files[i].cost,
                        main_tag: contest_files[i].main_tag
                    }
                });
            }
            redirect(`contest/${data.id}`);
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
                            source: SimpleMDEComponent,
                            name: 'description',
                            pass_props: { id: 'contest_textarea' },
                            validators: [required]
                        },
                        {
                            source: TaskListComponent,
                            name: 'contest_files'
                        },
                        {
                            source: CheckBoxComponent,
                            name: 'is_published',
                            pass_props: {
                                label: 'Published'
                            }
                        },
                        {
                            source: CheckBoxComponent,
                            name: 'is_rated',
                            pass_props: {
                                label: 'Rated'
                            }
                        },
                        {
                            source: CalendarComponent,
                            name: 'start_time'
                        },
                        {
                            source: CalendarComponent,
                            name: 'end_time'
                        }
                    ]}
                />
            </Card>
        );
    }
}

export default withLayout(CreateContest, sidebarLayout);

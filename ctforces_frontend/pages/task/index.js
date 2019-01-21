import React, { Component } from 'react';
import sidebarLayout from '../../layouts/sidebarLayout';
import withLayout from '../../wrappers/withLayout';
import FormComponent from '../../components/Form';
import { required } from '../../lib/validators';
import { get, post } from '../../lib/api_requests';
import redirect from '../../lib/redirect';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChartLine, faMarker } from '@fortawesome/free-solid-svg-icons';
import { Link } from '../../server/routes';
import MarkdownRender from '../../components/MarkdownRender';

import { Card } from 'reactstrap';
import SimpleMDEComponent from '../../components/SimpleMDEInput';
import CheckBoxComponent from '../../components/CheckBoxInput';
import TextInputComponent from '../../components/TextInput';
import FileUploaderComponent from '../../components/FileUploaderInput';
import FileListComponent from '../../components/FileList';
import TagsComponent from '../../components/TagsInput';

class ViewPost extends Component {
    constructor(props) {
        super(props);

        this.state = {
            is_solved: props.is_solved_by_user
        };
    }

    static async getInitialProps(ctx) {
        let data = await get(`tasks/${ctx.query.id}`, {
            ctx: ctx
        });
        data = await data.json();
        return {
            id: data.id,
            title: data.name,
            body: data.description,
            author_username: data.author_username,
            can_edit_task: data.can_edit_task,
            is_solved_by_user: data.is_solved_by_user,
            files: data.files_details
        };
    }

    onOkSubmit = async ({ flag }) => {
        let data = await post(`tasks/${this.props.id}/submit`, {
            data: {
                flag: flag
            }
        });
        if (data.ok) {
            data = await data.json();
            this.setState({ is_solved: true });
            return { ok: true, errors: {} };
        } else {
            return { ok: false, errors: await data.json() };
        }
    };

    render() {
        return (
            <Card className="p-2">
                <div style={{ fontSize: '2rem' }} className="py-2">
                    {this.props.title + ' by ' + this.props.author_username}
                </div>
                {this.props.can_edit_task && (
                    <div className="py-2">
                        <FontAwesomeIcon icon={faMarker} size="lg" />{' '}
                        <Link route={`/task/${this.props.id}/edit`}>
                            <a>Edit task</a>
                        </Link>
                    </div>
                )}
                <hr />
                <MarkdownRender source={this.props.body} />
                {this.props.files &&
                    this.props.files.map((obj, i) => {
                        return (
                            <a href={obj.file_field} key={i}>
                                {obj.name}
                            </a>
                        );
                    })}
                {this.state.is_solved ? 'Solved' : 'Not solved'}
                <FormComponent
                    onOkSubmit={this.onOkSubmit}
                    fields={[
                        {
                            source: TextInputComponent,
                            name: 'flag',
                            type: 'text',
                            placeholder: 'flag',
                            validators: [required]
                        }
                    ]}
                />
            </Card>
        );
    }
}

export default withLayout(ViewPost, sidebarLayout);

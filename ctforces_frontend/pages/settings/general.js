import React, {Component} from 'react';
import sidebarLayout from '../../layouts/sidebarLayout';
import withLayout from '../../wrappers/withLayout';
import CardWithTabsComponent from '../../components/CardWithTabs';
import FormComponent from '../../components/Form';
import withAuth from '../../wrappers/withAuth';
import redirect from '../../lib/redirect';
import FileUploaderComponent from '../../components/FileUploaderInput';

class SettingsSocial extends Component {
    constructor(props) {
        super(props);
    }

    onOkSubmit = () => {
        redirect(`user/${this.props.auth.user.username}`);
        return {ok: true, errors: {}};
    };

    render() {
        return (
            <div>
                <CardWithTabsComponent
                    tabs={[
                        {
                            text: this.props.auth.user.username,
                            href: `/user/${this.props.auth.user.username}`
                        },
                        {text: 'Blog', href: '#'},
                        {text: 'Tasks', href: '#'},
                        {text: 'General', href: '/settings/general'},
                        {text: 'Social', href: '/settings/social'}
                    ]}
                >
                    <FormComponent
                        onOkSubmit={this.onOkSubmit}
                        fields={[
                            {
                                source: FileUploaderComponent,
                                pass_props: {
                                    upload_url: 'avatar_upload',
                                    file_upload_name: 'avatar',
                                    field: 'avatar'
                                },
                                name: 'avatar'
                            }
                        ]}
                    />
                </CardWithTabsComponent>
            </div>
        );
    }
}

export default withAuth(withLayout(SettingsSocial, sidebarLayout));

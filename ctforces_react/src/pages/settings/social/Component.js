import React from 'react';

import { Formik, Form, Field } from 'formik';
import {
    CardBody, CardHeader, Button,
} from 'reactstrap';
import TextInput from 'components/Form/TextInput/Container';
import CheckboxInput from 'components/Form/CheckboxInput/Container';
import DetailError from 'components/Form/DetailError/Container';
import Layout from 'layouts/sidebar/Container';
import withLayout from 'wrappers/withLayout';

import CardWithTabsComponent from 'components/CardWithTabs/Container';

const Component = (props) => {
    const {
        personal_info: personalInfo = {
            first_name: '',
            last_name: '',
        },
        hide_personal_info: hidePersonalInfo = false,
    } = props.auth.user;

    return (
        <section>
            <article>
                <CardWithTabsComponent
                    tabs={[
                        {
                            text: props.auth.user.username,
                            href: `/users/${props.auth.user.username}/`,
                        },
                        { text: 'Blog', href: `/users/${props.auth.user.username}/posts/` },
                        { text: 'Tasks', href: `/users/${props.auth.user.username}/tasks/` },
                        { text: 'General', href: '/settings/general/' },
                        { text: 'Social', href: '/settings/social/' },
                    ]}
                >
                    <CardHeader className="text-center">Social Settings</CardHeader>
                    <CardBody>
                        <Formik
                            initialValues={{
                                first_name: personalInfo.first_name,
                                last_name: personalInfo.last_name,
                                hide_personal_info: hidePersonalInfo,
                            }}
                            enableReinitialize
                            onSubmit={(values, actions) => {
                                props.handleSubmit({ values, actions });
                            }}
                        >
                            {({ isSubmitting }) => (
                                <Form>
                                    <Field
                                        type="text"
                                        name="first_name"
                                        placeholder="First name"
                                        component={TextInput}
                                    />
                                    <Field
                                        type="text"
                                        name="last_name"
                                        placeholder="Last name"
                                        component={TextInput}
                                    />
                                    <Field
                                        name="hide_personal_info"
                                        label="Hide personal info"
                                        component={CheckboxInput}
                                    />
                                    <Field component={DetailError} />
                                    <Button
                                        type="submit"
                                        color="primary"
                                        className="btn-block"
                                        disabled={isSubmitting}
                                    >
                                        Update
                                    </Button>
                                </Form>
                            )}
                        </Formik>
                    </CardBody>
                </CardWithTabsComponent>
            </article>
        </section>);
};

export default withLayout(Component, Layout);

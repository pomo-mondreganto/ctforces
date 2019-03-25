import React from 'react';

import { Formik, Form, Field } from 'formik';
import {
    CardBody, CardHeader, Button,
} from 'reactstrap';
import TextInput from 'components/Form/TextInput/Container';
import FilesInput from 'components/Form/FilesInput/Container';
import DetailError from 'components/Form/DetailError/Container';
import Layout from 'layouts/sidebar/Container';
import withLayout from 'wrappers/withLayout';

import CardWithTabsComponent from 'components/CardWithTabs/Container';

const Component = props => (
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
                <CardHeader className="text-center">General Settings</CardHeader>
                <CardBody>
                    <Formik
                        initialValues={{
                            old_password: '',
                            password: '',
                        }}

                        onSubmit={(values, actions) => {
                            props.handleSubmit({ values, actions });
                        }}
                    >
                        {({ isSubmitting }) => (
                            <Form>
                                <Field
                                    type="password"
                                    name="old_password"
                                    placeholder="Old password"
                                    component={TextInput}
                                />
                                <Field
                                    type="password"
                                    name="password"
                                    placeholder="New password"
                                    component={TextInput}
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

                    <hr />

                    <Formik
                        initialValues={{
                            avatar: [],
                        }}

                        onSubmit={(values, actions) => {
                            props.handleSubmitAvatar({ values, actions });
                        }}
                    >
                        {({ isSubmitting }) => (
                            <Form>
                                <Field name="avatar" component={FilesInput} />
                                <Field component={DetailError} />
                                <Button
                                    type="submit"
                                    color="primary"
                                    className="btn-block"
                                    disabled={isSubmitting}
                                >
                                    Upload avatar
                                </Button>
                            </Form>
                        )}
                    </Formik>
                </CardBody>
            </CardWithTabsComponent>
        </article>
    </section>);

export default withLayout(Component, Layout);

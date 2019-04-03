import React from 'react';

import { Formik, Form, Field } from 'formik';
import {
    Button,
} from 'reactstrap';
import TextInput from 'components/Form/TextInput/Container';
import CheckboxInput from 'components/Form/CheckboxInput/Container';
import DetailError from 'components/Form/DetailError/Container';
import Layout from 'layouts/sidebar/Container';
import withLayout from 'wrappers/withLayout';

import UserTopBar from 'snippets_components/UserTopBar';

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
                    tabs={UserTopBar(props.auth.user.username)}
                >
                    <Formik
                        initialValues={{
                            personal_info: personalInfo,
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
                                    name="personal_info.first_name"
                                    placeholder="First name"
                                    component={TextInput}
                                />
                                <Field
                                    type="text"
                                    name="personal_info.last_name"
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
                </CardWithTabsComponent>
            </article>
        </section>);
};

export default withLayout(Component, Layout);

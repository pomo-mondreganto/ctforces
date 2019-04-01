import React from 'react';

import { Button } from 'reactstrap';
import { Formik, Form, Field } from 'formik';
import Layout from 'layouts/sidebar/Container';
import withLayout from 'wrappers/withLayout';
import TextInput from 'components/Form/TextInput/Container';
import CheckboxInput from 'components/Form/CheckboxInput/Container';
import SimpleMDEInput from 'components/Form/SimpleMDEInput/Container';
import DetailError from 'components/Form/DetailError/Container';

import CardWithTabs from 'components/CardWithTabs/Container';

const Component = props => (
    <CardWithTabs
        title="Write post"
    >
        <hr />
        <Formik
            initialValues={{
                title: '',
                body: '',
                is_published: false,
            }}
            onSubmit={(values, actions) => {
                props.handleSubmit({ values, actions });
            }}
        >
            {({ isSubmitting }) => (
                <Form>
                    <Field
                        type="text"
                        name="title"
                        placeholder="Title"
                        component={TextInput}
                    />
                    <Field name="body" component={SimpleMDEInput} />
                    <Field
                        name="is_published"
                        label="publish"
                        component={CheckboxInput}
                    />
                    <Field component={DetailError} />
                    <Button
                        type="submit"
                        color="primary"
                        className="btn-block"
                        disabled={isSubmitting}
                    >
                        Post
                    </Button>
                </Form>
            )}
        </Formik>
    </CardWithTabs>
);

export default withLayout(Component, Layout);

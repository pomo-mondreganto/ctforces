import React from 'react';

import { Card, Button } from 'reactstrap';
import Layout from '../../../layouts/sidebar/Container';
import withLayout from '../../../wrappers/withLayout';
import { Formik, Form, Field } from 'formik';
import TextInput from '../../../components/Form/TextInput/Container';
import CheckboxInput from '../../../components/Form/CheckboxInput/Container';
import SimpleMDEInput from '../../../components/Form/SimpleMDEInput/Container';
import DetailError from '../../../components/Form/DetailError/Container';

const Component = props => {
    return (
        <Card className="p-2">
            <div style={{ fontSize: '2rem' }} className="py-2">
                Write post
            </div>
            <hr />
            <Formik
                initialValues={{
                    title: '',
                    body: '',
                    is_published: false
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
                            type="checkbox"
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
        </Card>
    );
};

export default withLayout(Component, Layout);

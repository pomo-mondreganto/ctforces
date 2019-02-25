import React from 'react';

import { Card, Button } from 'reactstrap';
import {
    Formik, Form, Field, FieldArray,
} from 'formik';
import moment from 'moment';
import Layout from '../../../layouts/sidebar/Container';
import withLayout from '../../../wrappers/withLayout';
import TextInput from '../../../components/Form/TextInput/Container';
import CheckboxInput from '../../../components/Form/CheckboxInput/Container';
import DetailError from '../../../components/Form/DetailError/Container';
import CalendarInput from '../../../components/Form/CalendarInput/Container';
import TaskPreviewInput from '../components/TaskPreview/Container';

const Component = (props) => {
    const {
        name = '',
        description = '',
        is_published: isPublished = false,
        is_registration_open: isRegistrationOpen = false,
        is_rated: isRated = false,
        is_running: isRunning = false,
        publish_tasks_after_finished: publishTasksAfterFinished = false,
        is_finished: isFinished = false,
        start_time: startTime = moment().toISOString(),
        end_time: endTime = moment().toISOString(),
    } = { ...props.contest };

    const tasks = [{
        id: '', name: '', cost: '', main_tag: '',
    }];

    return (
        <Card className="p-2">
            <div style={{ fontSize: '2rem' }} className="py-2">
                Edit contest
            </div>
            <hr />
            <Formik
                enableReinitialize
                initialValues={{
                    name,
                    description,
                    tasks,
                    is_published: isPublished,
                    is_registration_open: isRegistrationOpen,
                    is_rated: isRated,
                    is_running: isRunning,
                    publish_tasks_after_finished: publishTasksAfterFinished,
                    is_finished: isFinished,
                    start_time: startTime,
                    end_time: endTime,
                }}
                onSubmit={(values, actions) => {
                    props.handleSubmit({ values, actions });
                }}
            >
                {({ isSubmitting, values }) => (
                    <Form>
                        <Field
                            type="text"
                            name="name"
                            placeholder="Name"
                            component={TextInput}
                        />

                        <Field
                            type="text"
                            name="description"
                            placeholder="Description"
                            component={TextInput}
                        />

                        <FieldArray
                            name="tasks"
                            render={arrayHelpers => (
                                <>
                                    {values.tasks.map((obj, i) => (
                                        <div key={i}>
                                            <Field
                                                name={`tasks.${i}`}
                                                component={TaskPreviewInput}
                                            />

                                            <button
                                                type="button"
                                                onClick={() => arrayHelpers.remove(i)
                                                }
                                            >
                                                remove
                                            </button>
                                        </div>
                                    ))}
                                    <button
                                        type="button"
                                        onClick={() => arrayHelpers.push({
                                            id: '',
                                            name: '',
                                        })
                                        }
                                    >
                                        add task
                                    </button>
                                </>
                            )}
                        />

                        <Field
                            type="checkbox"
                            name="is_published"
                            label="Published"
                            component={CheckboxInput}
                        />

                        <Field
                            type="checkbox"
                            name="is_registration_open"
                            label="Registration is opened"
                            component={CheckboxInput}
                        />

                        <Field
                            type="checkbox"
                            name="is_rated"
                            label="Rated"
                            component={CheckboxInput}
                        />

                        <Field
                            type="checkbox"
                            name="is_running"
                            label="Running"
                            component={CheckboxInput}
                        />

                        <Field
                            type="checkbox"
                            name="publish_tasks_after_finished"
                            label="Publish tasks after contest is finished"
                            component={CheckboxInput}
                        />

                        <Field
                            type="checkbox"
                            name="is_finished"
                            label="Finished"
                            component={CheckboxInput}
                        />

                        <label>Start time</label>
                        <Field name="start_time" component={CalendarInput} />

                        <label>End time</label>
                        <Field name="end_time" component={CalendarInput} />

                        <Field component={DetailError} />
                        <Button
                            type="submit"
                            color="primary"
                            className="btn-block"
                            disabled={isSubmitting}
                        >
                            Edit
                        </Button>
                    </Form>
                )}
            </Formik>
        </Card>
    );
};

export default withLayout(Component, Layout);

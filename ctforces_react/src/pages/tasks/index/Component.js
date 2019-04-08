import React from 'react';

import {
    Button,
} from 'reactstrap';
import { mediaUrl } from 'config/config';
import { Formik, Form, Field } from 'formik';
import getRank from 'lib/Ranking';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEdit } from '@fortawesome/free-solid-svg-icons';
import Layout from 'layouts/sidebar/Container';
import withLayout from 'wrappers/withLayout';
import TextInput from 'components/Form/TextInput/Container';
import DetailError from 'components/Form/DetailError/Container';
import CardWithTabs from 'components/CardWithTabs/Container';

import Markdown from 'components/Markdown/Container';

import { LinkContainerNonActive } from 'lib/LinkContainer';

import 'styles/pages/tasks.scss';

const Component = ({ task, handleSubmit }) => (
    <CardWithTabs>
        {task !== null && (
            <>
                <div className="th1">
                    {task.name}
                </div>
                <div className="mt-3">
                    By {' '}
                    <LinkContainerNonActive
                        to={`/users/${task.author_username}/`}>
                        <a className={getRank(task.author_rating)}>
                            {task.author_username}
                        </a>
                    </LinkContainerNonActive>
                    {task.can_edit_task && (
                        <>
                            {' '}
                            <LinkContainerNonActive
                                to={`/tasks/${task.id}/edit/`}
                            >
                                <FontAwesomeIcon icon={faEdit} className="c-p" />
                            </LinkContainerNonActive>
                        </>
                    )}
                </div>
                <div className="pt-2">
                    Tags:
                    {task.tags_details.map((tag, i) => (
                        <Button key={i} className="btn-sm ml-1 mr-1" outline
                            color="secondary">
                            {tag.name}
                        </Button>
                    ))}
                </div>
                <hr />
                <div className="long-text">
                    <Markdown text={task.description} />
                </div>
                <hr />
                {task.files && task.files.length > 0 && (
                    <>
                        <div>
                            Files:
                            {task.files_details.map((obj, i) => (
                                <div key={i}>
                                    <a href={`${mediaUrl}${obj.file_field}`}>{obj.name}</a>
                                </div>
                            ))}
                        </div>
                        <hr />
                    </>
                )}
                <Formik
                    initialValues={{
                        flag: '',
                    }}
                    onSubmit={(values, actions) => {
                        handleSubmit({ values, actions });
                    }}
                >
                    {({ isSubmitting }) => (
                        <Form>
                            <Field
                                type="text"
                                name="flag"
                                placeholder="flag{ucucuga}"
                                className={task.is_solved_by_user ? 'solved' : ''}
                                component={TextInput}
                            />
                            <Field component={DetailError} />
                            <Button
                                type="submit"
                                color="primary"
                                className="btn-block"
                                disabled={isSubmitting}
                            >
                                Submit
                            </Button>
                        </Form>
                    )}
                </Formik>
            </>
        )}
    </CardWithTabs >
);

export default withLayout(Component, Layout);

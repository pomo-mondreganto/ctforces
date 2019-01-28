import Layout from '../layouts/master.js';
import React, { Component } from 'react';
import { register } from '../lib/auth_service';
import { Link } from '../server/routes';
import { GlobalCtx } from '../wrappers/withGlobal';
import { equalTo, required } from '../lib/validators';
import withLayout from '../wrappers/withLayout';
import FormComponent from '../components/Form';
import redirect from '../lib/redirect';

import {
    Card,
    CardBody,
    CardHeader,
    CardLink,
    Col,
    Container,
    Row
} from 'reactstrap';
import TextInputComponent from '../components/TextInput';

class Register extends Component {
    constructor(props) {
        super(props);
    }

    onOkSubmit = async ({ username, email, password }) => {
        let data = await register(username, email, password);
        if (data.ok) {
            redirect('login');
            return { ok: true, errors: {} };
        } else {
            return { ok: false, errors: await data.json() };
        }
    };

    render() {
        return (
            <Row className="justify-content-center">
                <Col className="col-xl-6 col-lg-6 col-md-8 col-sm-10 col-10 my-4">
                    <Card>
                        <CardHeader className="text-center">Sign up</CardHeader>
                        <CardBody>
                            <FormComponent
                                onOkSubmit={this.onOkSubmit}
                                fields={[
                                    {
                                        source: TextInputComponent,
                                        name: 'username',
                                        type: 'text',
                                        placeholder: 'username',
                                        validators: [required]
                                    },
                                    {
                                        source: TextInputComponent,
                                        name: 'email',
                                        type: 'text',
                                        placeholder: 'email',
                                        validators: [required]
                                    },
                                    {
                                        source: TextInputComponent,
                                        name: 'password',
                                        type: 'password',
                                        placeholder: 'password',
                                        validators: [required]
                                    },
                                    {
                                        source: TextInputComponent,
                                        name: 'password2',
                                        type: 'password',
                                        placeholder: 'repeat password',
                                        validators: [
                                            required,
                                            equalTo('password')
                                        ]
                                    }
                                ]}
                            />
                            <hr className="my-3" />
                            <Container>
                                <Row>
                                    <Col className="text-left">
                                        <Link
                                            route="/restore_password"
                                            passHref
                                        >
                                            <CardLink>Forgot password</CardLink>
                                        </Link>
                                    </Col>
                                    <Col className="text-right">
                                        <Link route="/login" passHref>
                                            <CardLink>Login</CardLink>
                                        </Link>
                                    </Col>
                                </Row>
                            </Container>
                        </CardBody>
                    </Card>
                </Col>
            </Row>
        );
    }
}

export default withLayout(Register, Layout);

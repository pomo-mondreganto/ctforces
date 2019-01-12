import Layout from '../layouts/master.js';
import React, { Component } from 'react';
import { getUser, login } from '../lib/auth_service';
import Link from 'next/link';
import { GlobalCtx } from '../wrappers/withGlobal';
import { required } from '../lib/validators';
import withLayout from '../wrappers/withLayout';
import FormComponent from '../components/Form';
import TextInputComponent from '../components/TextInput';
import redirect from '../lib/redirect';
import { withRouter } from 'next/router';

import {
    Card,
    CardBody,
    CardHeader,
    CardLink,
    Col,
    Container,
    Row
} from 'reactstrap';

class Login extends Component {
    static contextType = GlobalCtx;

    constructor(props) {
        super(props);
    }

    onOkSubmit = async ({ username, password }) => {
        let data = await login(username, password);
        if (data.ok) {
            this.context.updateAuth(await getUser());
            const { router } = this.props;
            const { query } = router;
            const next = query.next || '/';
            redirect(next);
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
                        <CardHeader className="text-center">Sign in</CardHeader>
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
                                        name: 'password',
                                        type: 'password',
                                        placeholder: 'password',
                                        validators: [required]
                                    }
                                ]}
                            />
                            <hr className="my-3" />
                            <Container>
                                <Row>
                                    <Col className="text-left">
                                        <Link href="/restore_password" passHref>
                                            <CardLink>Forgot password</CardLink>
                                        </Link>
                                    </Col>
                                    <Col className="text-right">
                                        <Link href="/register" passHref>
                                            <CardLink>Register</CardLink>
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

export default withRouter(withLayout(Login, Layout));

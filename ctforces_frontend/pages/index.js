import sidebarLayout from '../layouts/sidebarLayout';
import React, { Component } from 'react';
import withLayout from '../wrappers/withLayout';
import Link from 'next/link';
import { Col, Container, Row } from 'reactstrap';

class Post extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <Row className="border rounded">
                <Col className="m-3">
                    <p className="h2">
                        <Link href={`/post/${this.props.data.id}`}>
                            <a>{this.props.data.title}</a>
                        </Link>
                    </p>
                    <p className="lead">
                        By{' '}
                        <Link href={`/user/${this.props.data.author}`}>
                            <a>{this.props.data.author},</a>
                        </Link>{' '}
                        {this.props.data.created_at}
                    </p>
                    <hr />
                    <p>{this.props.data.body}</p>
                </Col>
            </Row>
        );
    }
}

class Index extends Component {
    state = {
        posts: [
            {
                id: 1,
                title: 'Test post',
                body: 'This is test post body',
                author: 'pomo',
                created_at: '18/12/2018 Thu 13:43'
            }
        ]
    };

    constructor(props) {
        super(props);
        // this.setState({
        //     posts:
        // });
    }

    render() {
        return <div />;
    }
}

export default withLayout(Index, sidebarLayout, {
    guarded: false
});

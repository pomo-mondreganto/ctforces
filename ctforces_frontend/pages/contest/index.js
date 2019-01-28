import React, { Component } from 'react';
import sidebarLayout from '../../layouts/sidebarLayout';
import withLayout from '../../wrappers/withLayout';
import FormComponent from '../../components/Form';
import { required } from '../../lib/validators';
import { post, get } from '../../lib/api_requests';
import { api_url } from '../../config';
import redirect from '../../lib/redirect';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChartLine, faMarker } from '@fortawesome/free-solid-svg-icons';
import { Link } from '../../server/routes';
import TextInputComponent from '../../components/TextInput';

import { Card } from 'reactstrap';
import SimpleMDEComponent from '../../components/SimpleMDEInput';

class ViewContest extends Component {
    constructor(props) {
        super(props);
    }

    static async getInitialProps(ctx) {
        let data = await get(`contests/${ctx.query.id}`, {
            ctx: ctx
        });
        data = await data.json();
        return {
            id: data.id,
            title: data.name,
            author_username: data.author_username,
            tasks: data.contest_task_relationship_details
        };
    }

    render() {
        return (
            <Card className="p-2">
                <div style={{ fontSize: '2rem' }} className="py-2">
                    {this.props.title + ' by ' + this.props.author_username}
                </div>
                <hr />
                {this.props.tasks.map((obj, i) => {
                    return (
                        <Link route={`/task/${obj.id}`} key={i} passHref>
                            <a>{obj.task_name}</a>
                        </Link>
                    );
                })}
            </Card>
        );
    }
}

export default withLayout(ViewContest, sidebarLayout);

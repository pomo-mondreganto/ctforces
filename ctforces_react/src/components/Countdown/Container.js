import React from 'react';

import moment from 'moment';
import FormatDiffTime from 'lib/FormatDiffTime';
import Component from './Component';


class Countdown extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            goal: props.goal,
            interval: null,
        };
    }

    componentDidMount() {
        const interval = setInterval(() => {
            const remainingTime = moment(this.state.goal) - moment();
            if (remainingTime <= 0) {
                this.stop();
            }

            this.setState({
                str: FormatDiffTime(remainingTime),
                interval,
            });
        }, 1000);
    }

    componentWillMount() {
        this.stop();
    }

    stop = () => {
        if (this.state.interval !== null) {
            clearInterval(this.state.inverval);
            this.setState({
                interval: null,
            });
        }
    }

    render = () => <Component str={this.state.str} />;
}

export default Countdown;

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
                this.setState({
                    str: '00:00:00',
                });
                this.stop();
            } else {
                this.setState({
                    str: FormatDiffTime(remainingTime),
                });
            }
        }, 1000);

        this.setState({ interval });
    }

    componentWillUnmount() {
        this.stop();
    }

    stop = () => {
        if (this.state.interval !== null) {
            clearInterval(this.state.interval);
            this.setState({
                interval: null,
                str: '00:00:00',
            });
        }
    }

    render = () => <Component str={this.state.str} />;
}

export default Countdown;

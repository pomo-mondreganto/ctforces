import React, { Component } from 'react';

import Calendar from 'react-calendar';

class CalendarComponent extends Component {
    constructor(props) {
        super(props);
        this.state = {
            date: new Date()
        };
    }

    onChange = date => {
        this.setState({ date: date });
        this.props.handleChange({
            target: {
                name: this.props.name,
                value: date.toISOString()
            }
        });
    };

    render() {
        return (
            <div>
                <Calendar onChange={this.onChange} value={this.state.date} />
            </div>
        );
    }
}

export default CalendarComponent;

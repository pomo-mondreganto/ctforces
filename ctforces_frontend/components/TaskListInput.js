import React, { Component } from 'react';

import { Input, Label } from 'reactstrap';
import { get } from '../lib/api_requests';

class TaskListComponent extends Component {
    constructor(props) {
        super(props);
        this.state = {
            tasks: [],
            last_task: {
                id: '',
                name: '',
                cost: '',
                main_tag: ''
            }
        };
    }

    handleChange = task_id => {
        let tasks = this.state.tasks;
        tasks.push(this.state.last_task);
        this.setState({
            tasks: tasks,
            last_task: {
                id: '',
                name: '',
                cost: '',
                main_tag: ''
            }
        });
        this.props.handleChange({
            target: {
                name: this.props.name,
                value: tasks
            }
        });
    };

    handleRemove = task_key => {
        let tasks = this.state.tasks;
        tasks.splice(task_key, 1);
        this.setState({ tasks: tasks });
        this.props.handleChange({
            target: {
                name: this.props.name,
                value: tasks
            }
        });
    };

    handleIdInput = async event => {
        let task_id = event.target.value;
        let last_task = this.state.last_task;
        last_task.id = task_id;
        let task = await get(`tasks/${task_id}`);
        if (task.ok) {
            task = await task.json();
            last_task.name = task.name;
            last_task.cost = task.cost;
            last_task.tag = 'kek';
        } else {
            last_task.name = '';
            last_task.cost = '';
            last_task.main_tag = '';
        }
        this.setState({ last_task: last_task });
    };

    render() {
        return (
            <div>
                {this.state.tasks.map((obj, i) => {
                    return (
                        <div key={i}>
                            <span>{obj.id}</span>
                            <span>{obj.name}</span>
                            <span>{obj.cost}</span>
                            <button
                                onClick={() => {
                                    this.handleRemove(i);
                                }}
                                type="button"
                            >
                                remove
                            </button>
                        </div>
                    );
                })}
                <div>
                    <Input
                        onChange={this.handleIdInput}
                        value={this.state.last_task.id}
                    />
                    <span>{this.state.last_task.name}</span>
                    <span>{this.state.last_task.cost}</span>
                    <button onClick={this.handleChange} type="button">
                        add
                    </button>
                </div>
            </div>
        );
    }
}

export default TaskListComponent;

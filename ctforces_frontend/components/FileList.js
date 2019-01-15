import React, { Component } from 'react';

import { Progress } from 'reactstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTimes } from '@fortawesome/free-solid-svg-icons';

export default class FileListComponent extends Component {
    constructor(props) {
        super(props);
    }

    handleRemove = (index, props) => {
        let files = props.getStorage(`${props.ref_name}-list`);
        files.splice(index, 1);
        props.putStorage(`${props.ref_name}-list`, files);
    };

    render() {
        let files = this.props.getStorage(`${this.props.ref_name}-list`);
        return (
            <div>
                {files &&
                    files.map((obj, i) => {
                        let progress = this.props.getStorage(
                            `${this.props.ref_name}-${i}-progress`
                        );
                        return (
                            <div key={i}>
                                <div className="py-2">
                                    <FontAwesomeIcon
                                        icon={faTimes}
                                        size="lg"
                                        onClick={() =>
                                            this.handleRemove(i, this.props)
                                        }
                                    />{' '}
                                    {obj.name}
                                </div>
                                {progress && (
                                    <Progress value={progress * 100} />
                                )}
                            </div>
                        );
                    })}
            </div>
        );
    }
}

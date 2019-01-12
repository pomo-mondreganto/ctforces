import React, { Component } from 'react';

import { Progress } from 'reactstrap';

export default class FileListComponent extends Component {
    constructor(props) {
        super(props);
    }

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
                                <div>{obj.name}</div>
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

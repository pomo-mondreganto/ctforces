import React, { Component } from 'react';
import { post } from '../lib/api_requests';

import { Input, Button } from 'reactstrap';

class FileUploaderComponent extends Component {
    constructor(props) {
        super(props);
        this.state = {
            selectedFile: null,
            loaded: 0
        };
    }

    handleSelectedFile = event => {
        this.setState({
            selectedFile: event.target.files[0],
            loaded: 0
        });
    };

    handleUpload = async () => {
        let data = new FormData();
        data.append(
            'avatar',
            this.state.selectedFile,
            this.state.selectedFile.name
        );
        let result = await post('avatar_upload', {
            data: data,
            content_type: 'multipart/form-data'
        });
        result = await result.json();
    };

    render() {
        return (
            <div>
                <Input
                    type="file"
                    name="avatar"
                    onChange={this.handleSelectedFile}
                />
                <Button onClick={this.handleUpload}>Upload</Button>
                <div> {Math.round(this.state.loaded, 2)} %</div>
            </div>
        );
    }
}

export default FileUploaderComponent;

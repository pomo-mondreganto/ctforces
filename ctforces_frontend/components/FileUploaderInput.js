import React, {Component} from 'react';
import {api_url} from '../config';
import getCookie from '../lib/get_cookie';

import {Button, CustomInput} from 'reactstrap';

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
        let xhr = new XMLHttpRequest();

        xhr.withCredentials = true;

        xhr.upload.onprogress = event => {
            console.log(event.loaded + ' ' + event.total);
        };

        xhr.onload = xhr.onerror = function () {
            console.log(this);
            if (this.status === 200) {
                console.log('success');
            } else {
                console.log('error ' + this.status);
            }
        };

        xhr.open('POST', `${api_url}/avatar_upload/`);
        xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        xhr.setRequestHeader('Accept', 'application/json');
        xhr.send(data);
    };

    render() {
        return (
            <div>
                <CustomInput
                    type="file"
                    name="avatar"
                    id="avatar-input"
                    onChange={this.handleSelectedFile}
                />
                <Button onClick={this.handleUpload}>Upload</Button>
                <div> {Math.round(this.state.loaded, 2)} %</div>
            </div>
        );
    }
}

export default FileUploaderComponent;

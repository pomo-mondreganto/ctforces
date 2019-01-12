import React, { Component } from 'react';
import { api_url } from '../config';
import getCookie from '../lib/get_cookie';

import { Button, CustomInput } from 'reactstrap';
import { resolve } from 'url';
import { rejects } from 'assert';

class FileUploaderComponent extends Component {
    constructor(props) {
        super(props);
    }

    handleSelectedFiles = event => {
        let files = event.target.files;
        let selectedFiles = this.props.getStorage(
            `${this.props.file_upload_name}-list`
        );
        if (selectedFiles === undefined) {
            selectedFiles = [];
        }
        for (let i = 0; i < files.length; ++i) {
            selectedFiles.push(files[i]);
        }
        this.props.putStorage(
            `${this.props.file_upload_name}-list`,
            selectedFiles
        );
    };

    uploadFile = (
        i,
        data,
        file_upload_name,
        file_name,
        upload_url,
        putStorage
    ) => {
        return new Promise(function(resolve, reject) {
            let xhr = new XMLHttpRequest();

            xhr.withCredentials = true;
            xhr.responseType = 'json';

            xhr.upload.onprogress = event => {
                putStorage(
                    `${file_upload_name}-${i}-progress`,
                    event.loaded / event.total
                );
            };

            xhr.onload = xhr.onerror = function() {
                putStorage(`${file_upload_name}-${i}-progress`, undefined);
                if (this.status === 200) {
                    resolve(this.response);
                } else {
                    reject(this.status);
                }
            };

            xhr.open('POST', `${api_url}/${upload_url}/`);
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
            xhr.setRequestHeader('Accept', 'application/json');
            xhr.send(data);
        });
    };

    beforeSubmit = async () => {
        let uploaded_files = [];
        let extract_field = this.props.field;
        let promises = [];
        let files = this.props.getStorage(
            `${this.props.file_upload_name}-list`
        );

        for (let i = 0; i < files.length; ++i) {
            let file = files[i];
            let data = new FormData();
            data.append(this.props.file_upload_name, file, file.name);
            promises.push(
                this.uploadFile(
                    i,
                    data,
                    this.props.file_upload_name,
                    file.name,
                    this.props.upload_url,
                    this.props.putStorage
                )
            );
        }

        let data = await Promise.all(promises);

        if (this.props.multiple) {
            this.props.handleChange({
                target: {
                    name: this.props.name,
                    value: uploaded_files
                }
            });
        } else {
            this.props.handleChange({
                target: {
                    name: this.props.name,
                    value: uploaded_files[0]
                }
            });
        }
    };

    render() {
        return (
            <div>
                <CustomInput
                    type="file"
                    name="avatar"
                    id="avatar-input"
                    onChange={this.handleSelectedFiles}
                    multiple={this.props.multiple}
                />
            </div>
        );
    }
}

export default FileUploaderComponent;

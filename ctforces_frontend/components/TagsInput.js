import React, { Component } from 'react';

import { Input, Label } from 'reactstrap';

import { get, post } from '../lib/api_requests';

import { WithContext as ReactTags } from 'react-tag-input';
import '../styles/tags_style.css';

class TagsComponent extends Component {
    constructor(props) {
        super(props);
        let initial_value = [];
        let external_value = [];
        if (this.props.initial_value !== undefined) {
            for (let tag in this.props.initial_value) {
                initial_value.push({ id: tag.name, text: tag.name });
                external_value.push(tag.id);
            }
        }
        this.state = {
            value: initial_value,
            external_value: external_value,
            suggestions: []
        };
        this.props.handleChange({
            target: {
                name: this.props.name,
                value: initial_value
            }
        });
    }

    handleDelete = i => {
        let tags = this.state.value;
        tags.splice(i, 1);
        this.setState({ value: tags });

        tags = this.state.external_value;
        tags.splice(i, 1);
        this.setState({ external_value: tags });
        this.props.handleChange({
            target: {
                name: this.props.name,
                value: tags
            }
        });
    };

    handleAddition = async tag => {
        let tags = await get('task_tags/search', {
            data: {
                name: tag.text
            }
        });
        tags = await tags.json();
        let tag_id;
        if (tags.length == 0 || tags[0].name !== tag.text) {
            tag_id = await post('task_tags', {
                data: {
                    name: tag.text
                }
            });
            tag_id = await tag_id.json();
            tag_id = tag_id.id;
        }

        tags = this.state.value;
        tags.push(tag);
        this.setState({ value: tags });

        tags = this.state.external_value;
        tags.push(tag_id);
        this.setState({ external_value: tags });
        this.props.handleChange({
            target: {
                name: this.props.name,
                value: tags
            }
        });
    };

    handleInputChange = async tag => {
        let tags = await get('task_tags/search', {
            data: {
                name: tag
            }
        });
        tags = await tags.json();
        let suggestions = [];
        for (let i = 0; i < tags.length; ++i) {
            let tag = tags[i];
            suggestions.push({ id: tag.name, text: tag.name });
        }
        this.setState({ suggestions: suggestions });
    };

    render() {
        return (
            <React.Fragment>
                <ReactTags
                    tags={this.state.value}
                    handleDelete={this.handleDelete}
                    handleAddition={this.handleAddition}
                    handleInputChange={this.handleInputChange}
                    suggestions={this.state.suggestions}
                />
            </React.Fragment>
        );
    }
}

export default TagsComponent;

import React, { Component } from 'react';

import { Input, Label } from 'reactstrap';

import { get, post } from '../lib/api_requests';

import { WithContext as ReactTags } from 'react-tag-input';

class TagsComponent extends Component {
    constructor(props) {
        super(props);
        let initial_value = [];
        this.state = { value: [], suggestions: [] };
    }

    async componentDidMount() {
        if (this.props.initial_value !== undefined) {
            for (let i = 0; i < this.props.initial_value.length; ++i) {
                let tag = this.props.initial_value[i];
                tag = { id: tag.name, text: tag.name };
                await this.handleAddition(tag);
            }
        }
    }

    getTagId = async tag => {
        let tags = await get('task_tags/search', {
            data: {
                name: tag
            }
        });
        tags = await tags.json();
        let tag_id;
        if (tags.length == 0 || tags[0].name !== tag) {
            tag_id = await post('task_tags', {
                data: {
                    name: tag
                }
            });
            tag_id = await tag_id.json();
            tag_id = tag_id.id;
        } else {
            tag_id = tags[0].id;
        }
        return tag_id;
    };

    handleDelete = async i => {
        let tags = this.state.value;
        tags.splice(i, 1);
        this.setState({ value: tags });

        this.props.handleChange({
            target: {
                name: this.props.name,
                value: await tags.map(async (obj, i) => {
                    return await this.getTagId(obj.text);
                })
            }
        });
    };

    handleAddition = async tag => {
        let tags = this.state.value;
        tags.push(tag);
        this.setState({ value: tags });

        this.props.handleChange({
            target: {
                name: this.props.name,
                value: await Promise.all(
                    tags.map(async (obj, i) => {
                        return await this.getTagId(obj.text);
                    })
                )
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

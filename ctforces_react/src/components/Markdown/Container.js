import React from 'react';

import Component from './Component';

class MarkdownContainer extends React.Component {
    render = () => <Component text={this.props.text} />
}

export default MarkdownContainer;

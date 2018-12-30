import React, { Component } from 'react';
import { CSSTransition } from 'react-transition-group';
import { smallWidth } from '../config';
import { GlobalCtx } from '../wrappers/withGlobal';

class SidebarComponent extends Component {
    static contextType = GlobalCtx;

    constructor(props) {
        super(props);
    }

    handleWindowSizeChange = () => {
        this.context.updateSidebars({
            rightSidebar: window.innerWidth > smallWidth
        });
    };

    componentDidMount() {
        if (!this.context.sidebars.rightSidebar) {
            this.handleWindowSizeChange();
        }
        window.addEventListener('resize', this.handleWindowSizeChange);
    }

    componentWillUnmount() {
        window.removeEventListener('resize', this.handleWindowSizeChange);
    }

    render() {
        return (
            <CSSTransition
                in={this.context.sidebars.rightSidebar}
                timeout={300}
                classNames="sidebar-right"
                unmountOnExit
            >
                <nav className="sidebar-right">
                    kek
                    <style jsx>{`
                        .sidebar-right {
                            float: right;
                            min-width: 100%;
                            background-color: blue;
                            margin-right: 0;
                        }
                        .sidebar-right-exit {
                            margin-right: 0;
                        }
                        .sidebar-right-exit-active {
                            margin-right: -150%;
                            transition: all 0.3s linear;
                        }
                        .sidebar-right-enter {
                            margin-right: -150%;
                        }
                        .sidebar-right-enter-active {
                            margin-right: 0;
                            transition: all 0.3s linear;
                        }
                    `}</style>
                </nav>
            </CSSTransition>
        );
    }
}

export default SidebarComponent;

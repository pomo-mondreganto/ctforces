import React from 'react';

import CardWithTabs from 'components/CardWithTabs/Container';
import Pagination from 'components/Pagination/Container';
import { LinkContainerNonActive } from 'lib/LinkContainer';
import Countdown from 'components/Countdown/Container';

import ReactTooltip from 'react-tooltip';
import Popup from 'reactjs-popup';

import 'styles/pages/contests.scss';

const Component = props => (
    <CardWithTabs
        title={props.title}
        tabs={props.tabs}
        pagination={
            <Pagination to={props.paginationUrl}
                currentPage={props.currentPage}
                count={props.count}
                pageSize={props.pageSize} />
        }
    >
        {props.running && props.running.length > 0 && (
            <>
                <div className="th3 mb-3">Running</div>
                <div className="contests-table mb-5">
                    <div className="contests-table-head-running">
                        <span className="ta-c">#</span>
                        <span className="ta-l">Name</span>
                        <span className="ta-c">Ends in</span>
                        <span></span>
                    </div>
                    <div className="contests-table-body">
                        {props.running.map((obj, i) => (
                            <div key={i} className="contests-table-item-running">
                                <span className="ta-c">{i + 1}</span>
                                <span className="ta-l">
                                    <span>
                                        {obj.name}
                                        {obj.is_rated && (
                                            <>
                                                <ReactTooltip place="right" id="rated">
                                                    <span>This contest is rated</span>
                                                </ReactTooltip>
                                                <span className="is-rated" data-tip data-for="rated">
                                                    {' R'}
                                                </span>
                                            </>
                                        )}
                                    </span>
                                </span>
                                <span className="ta-c">
                                    <Countdown
                                        goal={obj.end_time}
                                    />
                                </span>
                                <span className="ta-c">
                                    {(obj.is_registered || !obj.is_registration_open) && (
                                        <LinkContainerNonActive to={`/contests/${obj.id}/`}>
                                            <a>
                                                Open
                                            </a>
                                        </LinkContainerNonActive>
                                    )}
                                    {!obj.is_registered && obj.is_registration_open && (
                                        <>

                                            <Popup
                                                trigger={
                                                    <span className="contest-register">
                                                        Register
                                                    </span>
                                                }
                                                modal
                                                closeOnDocumentClick
                                            >
                                                <div className="mb-3">Are you sure you want to register for this contest?</div>
                                                <span className="contest-register"
                                                    onClick={() => props.register(obj.id)}>
                                                    Yes, Sure!
                                                </span>
                                            </Popup>
                                            <LinkContainerNonActive to={`/contests/${obj.id}/`}>
                                                <a>
                                                    Open
                                                </a>
                                            </LinkContainerNonActive>
                                        </>
                                    )}
                                </span>
                            </div>
                        ))}
                    </div>
                </div>
            </>
        )}

        {props.upcoming && props.upcoming.length > 0 && (
            <>
                <div className="th3 mb-3">Upcoming</div>
                <div className="contests-table mb-5">
                    <div className="contests-table-head-upcoming">
                        <span className="ta-c">#</span>
                        <span className="ta-l">Name</span>
                        <span className="ta-c">Starts in</span>
                        <span></span>
                    </div>
                    <div className="contests-table-body">
                        {props.upcoming.map((obj, i) => (
                            <div key={i} className="contests-table-item-upcoming">
                                <span className="ta-c">{i + 1}</span>
                                <span className="ta-l">
                                    <span>
                                        {obj.name}
                                        {obj.is_rated && (
                                            <>
                                                <ReactTooltip place="right" id="rated">
                                                    <span>This contest is rated</span>
                                                </ReactTooltip>
                                                <span className="is-rated" data-tip data-for="rated">
                                                    {' R'}
                                                </span>
                                            </>
                                        )}
                                    </span>
                                </span>
                                <span className="ta-c">
                                    <Countdown
                                        goal={obj.start_time}
                                    />
                                </span>
                                <span className="ta-c">
                                    {obj.is_registration_open ? (
                                        <>
                                            {!obj.is_registered && (
                                                <span className="contest-register"
                                                    onClick={() => props.register(obj.id)}>
                                                    Register
                                                </span>
                                            )}
                                            {obj.is_registered && (
                                                <span className="contest-registered">
                                                    Registered
                                                </span>
                                            )}
                                        </>
                                    ) : 'Closed'}
                                </span>
                            </div>
                        ))}
                    </div>
                </div>
            </>
        )}

        {props.finished && props.finished.length > 0 && (
            <>
                <div className="th3 mb-3">Finished</div>
                <div className="contests-table">
                    <div className="contests-table-head-finished">
                        <span className="ta-c">#</span>
                        <span className="ta-l">Name</span>
                        <span></span>
                    </div>
                    <div className="contests-table-body">
                        {props.finished.map((obj, i) => (
                            <div key={i} className="contests-table-item-finished">
                                <span className="ta-c">{i + 1 + props.pageSize * (props.currentPage - 1)}</span>
                                <span className="ta-l">
                                    <span>
                                        {obj.name}
                                        {obj.is_rated && (
                                            <>
                                                <ReactTooltip place="right" id="rated">
                                                    <span>This contest is rated</span>
                                                </ReactTooltip>
                                                <span className="is-rated" data-tip data-for="rated">
                                                    {' R'}
                                                </span>
                                            </>
                                        )}
                                    </span>
                                </span>
                                <span className="ta-c">
                                    <LinkContainerNonActive to={`/contests/${obj.id}/`}>
                                        <a>
                                            Open
                                        </a>
                                    </LinkContainerNonActive>
                                </span>
                            </div>
                        ))}
                    </div>
                </div>
            </>
        )}
    </CardWithTabs>
);

export default Component;

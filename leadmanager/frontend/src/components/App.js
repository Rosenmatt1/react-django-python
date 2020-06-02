import React, { Component, Fragment } from 'react';
import ReactDOM from 'react-dom';

import Header from './layout/Header';
import Dashboard from './leads/Dashboard';
import Chuck from './leads/Chuck';

class App extends Component {
    render() {
        return (
            <Fragment>
                <Header />
                <div className="container">
                    <Dashboard />
                </div>
                <Chuck />
            </Fragment>
        )
    }
}

ReactDOM.render(<App />, document.getElementById('app'));
import React, { Component, Fragment } from 'react';
import ReactDOM from 'react-dom';

// import Header from './layout/Header';
// import Dashboard from './leads/Dashboard';
import Chuck from './leads/Chuck';

class App extends Component {
    render() {
        return (
            <Fragment>
                <Chuck />
            </Fragment>
        )
    }
}

ReactDOM.render(<App />, document.getElementById('app'));
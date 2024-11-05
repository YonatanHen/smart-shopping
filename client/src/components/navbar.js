import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

function Navbar() {
    return (
        <nav className="navbar navbar-expand-lg navbar-light bg-light" style={{paddingLeft: "1%", paddingRight: "1%"}}>
            <a className="navbar-brand" href="#">Smart Shopping</a>
            <div className="collapse navbar-collapse" id="navbarNav">
                <ul className="navbar-nav ms-auto">
                    <li className="nav-item">
                        <a className="nav-link" href="/">Your Purchases</a>
                    </li>
                    <li className="nav-item">
                        <a className="nav-link" href="/create-list">Create Shopping List</a>
                    </li>
                </ul>
            </div>
        </nav>
    );
}

export default Navbar;

import React, { Component } from 'react';
import BtnPrimary from './ButtonPrimary';

class Navbar extends Component {
    state = {  } 
    render() { 
        return (
            // <header id="header" class="navbar navbar-expand-lg navbar-end navbar-absolute-top navbar-dark" >
            <nav className="navbar navbar-expand-lg navbar-end navbar-absolute-top navbar-dark">
                <a className="navbar-brand" href="public/logo-white.svg" aria-label="Space">
                    <img className="navbar-brand-logo" src="./public/assets/img8.jpg" alt="Logo" />
                </a>

                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-default">
                    <i className="bi-list"></i>
                    </span>
                    <span className="navbar-toggler-toggled">
                    <i className="bi-x"></i>
                    </span>
                </button>

                <div className="collapse navbar-collapse" id="navbarNavDropdown">
                    <div className="navbar-absolute-top-scroller">
                        <ul className="navbar-nav">
                            <li className="nav-item">
                                Home
                            </li>
                            <li className="nav-item">
                                Pricing
                            </li>
                            <li className="nav-item">
                                About us
                            </li>
                            <li className="nav-divider"></li>
                            <li className="nav-item">
                                Login
                            </li>
                            <li className="nav-item">
                                <BtnPrimary />
                            </li>
                        </ul>   
                    </div>
                </div>
            </nav>
        );
    }
}
 
export default Navbar;


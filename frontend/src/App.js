import Navbar from './components/Navbar'
import './App.css';
import './theme.css';
import React, { Component } from 'react'

class App extends Component {
  state = {} 
  render () {
    return (
      <React.Fragment>
        <Navbar />
      </React.Fragment>
    );
  }
}

export default App;

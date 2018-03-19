import 'materialize-css/dist/css/materialize.min.css';
import 'materialize-css/dist/js/materialize.min.js';
import React, { Component } from 'react';
import logo from '../logo.svg';
import './App.css';
import NewsPanel from '../NewsPanel/NewsPanel';
import NewsCard from '../NewsCard/NewsCard';

class App extends Component {
  render() {
    return (
      <div>
        <img className='logo' src={logo} alt='logo'/>
        <div className='container'>
          <NewsPanel />
          <NewsCard />
        </div>
      </div>

    );
  }  
}

export default App;

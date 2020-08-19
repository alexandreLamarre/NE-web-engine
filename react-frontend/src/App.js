import React from 'react';
import logo from './logo.svg';
import './App.css';
import CLI from "./CLI"

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Non-Euclidean Computational Engine
        </p>
        <CLI />
        <a
          className="App-link"
          href="https://github.com/alexandreLamarre/Non-Euclidean-Computational-Engine-Python-source-code-#Quick-guide"
          target="_blank"
          rel="noopener noreferrer"
        >
          Documentation
        </a>
      </header>
    </div>
  );
}

export default App;

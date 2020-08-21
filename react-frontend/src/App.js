import React from 'react';
import logo from './logo.svg';
import './App.css';
import Latex from "./Latex"
import CLI from "./CLI"

function App() {
  return (
    <div className="App">
      <header className="App-header">


        <CLI />
        <a
          className="App-link"
          href="https://github.com/alexandreLamarre/Non-Euclidean-Computational-Engine-Python-source-code-#Quick-guide"
          target="_blank"
          rel="noopener noreferrer"
        >
          Documentation
        </a>

        <ul  id = "ul-info"></ul>

      </header>

    </div>
  );
}

export default App;

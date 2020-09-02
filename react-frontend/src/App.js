import React from 'react';
import {Tab,Tabs,TabList,TabPanel} from 'react-tabs';
import './Tab.css';
import './App.css';
import CLI from "./CLI"
import MatrixCLI from "./MatrixCLI"

function App() {
  return (
    <div className="App">
      <header className="App-header">

      <Tabs defaultIndex={0} onSelect={index => console.log(index)}>
        <TabList>
          <Tab> Functions </Tab>
          <Tab> Matrices</Tab>
          <Tab> Algorithms</Tab>
          <Tab> Log in </Tab>
        </TabList>
        <TabPanel>
          <CLI />
          <ul  id = "ul-info"></ul>
        </TabPanel>
        <TabPanel>
        Matrices
        <MatrixCLI/> 
        </TabPanel>
        <TabPanel> Algorithms </TabPanel>
        <TabPanel> Log in </TabPanel>
      </Tabs>
      </header>

    </div>
  );
}

export default App;

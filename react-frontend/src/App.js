import React from 'react';
import {Tab,Tabs,TabList,TabPanel} from 'react-tabs';
import './Tab.css';
import logo from './logo.svg';
import './App.css';
import Latex from "./Latex"
import CLI from "./CLI"

function App() {
  return (
    <div className="App">
      <header className="App-header">

      <Tabs defaultIndex={0} onSelect={index => console.log(index)}>
        <TabList>
          <Tab> Functions </Tab>
          <Tab> Matrices</Tab>
          <Tab> Groups</Tab>
          <Tab> Dynamical Systems</Tab>
          <Tab> Algorithms</Tab>
          <Tab> Log in </Tab>
        </TabList>
        <TabPanel>
          <CLI />
          <ul  id = "ul-info"></ul>
        </TabPanel>
        <TabPanel> Matrices </TabPanel>
        <TabPanel> Groups</TabPanel>
        <TabPanel> Dynamical systems </TabPanel>
        <TabPanel> Algorithms </TabPanel>
        <TabPanel> Log in </TabPanel>
      </Tabs>
      </header>

    </div>
  );
}

export default App;

import React from 'react';
import {Tab,Tabs,TabList,TabPanel} from 'react-tabs';
import './Tab.css';
import './App.css';
import CLI from "./CLI"
import MatrixCLI from "./MatrixCLI"
import MarkovGraph from "./MarkovGraph"
import SearchVisualizer from "./Algorithms/SearchVisualizer"
import SortVisualizer from "./Algorithms/SortVisualizer"
import AlgoVisualizer from "./Algorithms/algoVisualizer"

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
        <TabPanel>
          <AlgoVisualizer/>
        </TabPanel>
        <TabPanel>
        Log in
        <MarkovGraph/>
         </TabPanel>
      </Tabs>
      </header>

    </div>
  );
}

export default App;

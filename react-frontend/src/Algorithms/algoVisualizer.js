import {Tab,Tabs,TabList,TabPanel} from 'react-tabs';

import React from "react";
import "./algoVisualizer.css";
import SearchVisualizer from "./SearchVisualizer";
import SortVisualizer from "./SortVisualizer";
import NetworkVisualizer from "./Network";

class AlgoVisualizer extends React.Component{
  constructor(props){
    super(props);
    this.state = {

    };
  }

  render(){

    return <div className = "vertical tabs" defaultIndex={0}>
        <Tabs>
          <TabList>
            <Tab> Search </Tab>
            <Tab> Sort </Tab>
            <Tab> Networks </Tab>
            <Tab> Travelling Salesman</Tab>
          </TabList>
          <TabPanel>
            <SearchVisualizer/>
          </TabPanel>
          <TabPanel>
            <SortVisualizer/>
          </TabPanel>
          <TabPanel>
            <NetworkVisualizer/>
          </TabPanel>
          <TabPanel>
            Nothing here atm!
          </TabPanel>
      </Tabs>
          </div>
  }
}

export default AlgoVisualizer;

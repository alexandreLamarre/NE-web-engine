import React from "react";

import "./Node.css";

class Node extends React.Component{
  constructor(props){
    super(props);
    this.state = {};
  }

  render(){
    const{
      col,GoalNode,StartNode,WallNode,onMouseDown,onMouseEnter,
      onMouseUp,row,} = this.props;

    const extraClassName = GoalNode ? 'node-goal': StartNode ? 'node-start' : WallNode ? 'node-wall' : 'node';
    return <div id = {'node-${row}-${col}'}
    className={`node ${extraClassName}`}
    onMouseDown={() => onMouseDown(row,col)}
    onMouseEnter={()=> onMouseEnter(row,col)}
    onMouseUp={() => onMouseUp()}>
    </div>;
  }
}

export default Node;

import React from "react";
import Node from "./Node"
import "./SearchVisualizer.css";

const START_NODE_ROW = 5;
const START_NODE_COL = 5;
const FINISH_NODE_ROW = 5;
const FINISH_NODE_COL = 10;



class SearchVisualizer extends React.Component{
  constructor(props){
    super(props);
    this.state = {
      grid: [],
      mousePressed: false,
      startNodePos: [5,5],
      goalNodePos: [5,20],
      startNodeDragging: false,
      goalNodeDragging: false
    };
  }

  componentDidMount(){
    const startNodePos = this.state.startNodePos;
    const endNodePos = this.state.goalNodePos;
    const grid = getInitialGrid(startNodePos, endNodePos);
    this.setState({grid: grid});
  }

  handleMouseDown(row,col){
    if(row === this.state.startNodePos[0] && col === this.state.startNodePos[1]){
      this.setState({startNodeDragging: true, mousePressed: true});
      console.log("startnode selected")
    }
    else if(row === this.state.goalNodePos[0] && col === this.state.goalNodePos[1]){
      this.setState({goalNodeDragging: true, mousePressed: true});
      console.log("goalnode selected");
    }
    else{
      const newGrid = getNewGridWithWallToggled(this.state.grid, row, col);
      this.setState({grid: newGrid, mousePressed: true});
      console.log("regular node selected")
    }
  }

  handleMouseEnter(row,col){
    if(!this.state.mousePressed) return;
    if(this.state.startNodeDragging){
      const startNodePos = this.state.startNodePos;
      const newGrid = getNewGridStartNode(this.state.grid, startNodePos[0],startNodePos[1],
                        row,col);
      this.setState({startNodePos: [row,col], grid: newGrid});
      // console.log("moving start to")
      // console.log(row,col)
    }
    else if(this.state.goalNodeDragging){
      const goalNodePos = this.state.goalNodePos;
      const newGrid = getNewGridEndNode(this.state.grid, this.state.goalNodePos[0],this.state.goalNodePos[1],
                        row,col);
      this.setState({goalNodePos: [row,col], grid: newGrid});
      // console.log("moving goal to");
      // console.log(row,col);
    }
    else{
      const newGrid = getNewGridWithWallToggled(this.state.grid,row,col);
      // console.log("drawing wall to");
      // console.log(row,col);
      this.setState({grid: newGrid});
    }
  }

  handleMouseUp(){
    this.setState({mousePressed: false,
      startNodeDragging: false,
      goalNodeDragging:false
    });
    console.log("Mouse Released")
  }



  render(){
    const {grid, mousePressed} = this.state;

    return(
      <>

        <button>
          Run Search
        </button>
        <div className="grid">
          {grid.map((row,rowIdx) => {
            return (
              <div key={rowIdx}>
                {row.map((node,nodeIdx)=>{
                  const {row,col,GoalNode,StartNode,WallNode} = node;
                  return(
                    <Node
                      key = {nodeIdx}
                      col = {col}
                      row = {row}
                      GoalNode = {GoalNode}
                      StartNode = {StartNode}
                      WallNode = {WallNode}
                      mousePressed = {mousePressed}
                      onMouseDown={(row,col) => this.handleMouseDown(row,col)}
                      onMouseEnter={(row,col) => this.handleMouseEnter(row,col)}
                      onMouseUp={() => this.handleMouseUp()}>
                    </Node>
                    );
                })}
              </div>
            )
          }
          )}
        </div>
      </>
    )
  }
}

const getInitialGrid = (startNodePos,endNodePos) => {
  const grid = [];
  for(let row = 0; row< 10; row ++){
    const currentRow = [];
    for(let col = 0; col < 25; col ++){
      currentRow.push(createNode(col,row, startNodePos,endNodePos));
    }
    grid.push(currentRow);
  }
  return grid;
};

const createNode = (col,row, startNodePos, endNodePos) => {
  return {col,row,StartNode: row === startNodePos[0] && col === startNodePos[1],
  GoalNode: row === endNodePos[0] && col === endNodePos[1],
  distance: Infinity,
  isVisited: false,
  WallNode: false,
  previousNode: null};
};

const getNewGridWithWallToggled = (grid, row, col) => {
  const newGrid = grid.slice();
  const node = newGrid[row][col];
  const newNode = {
    ...node,
    WallNode: !node.WallNode,
  };
  newGrid[row][col] = newNode;
  return newGrid;
};

const getNewGridStartNode = (grid,rrow,rcol,row,col) => {
  const newGrid = grid.slice();
  const prevnode = newGrid[rrow][rcol]
  const node = newGrid[row][col];
  const prevnodeupdated = {
    ...prevnode,
    StartNode: false,
  }
  const newNode = {
    ...node,
    StartNode: true,
  }
  newGrid[rrow][rcol] = prevnodeupdated;
  newGrid[row][col] = newNode;
  return newGrid;
};

const getNewGridEndNode = (grid,rrow, rcol, row,col) => {
  const newGrid = grid.slice();
  const prevnode = newGrid[rrow][rcol]
  const node = newGrid[row][col]
  const prevnodeupdated = {
    ...prevnode,
    GoalNode: false,
  }
  const newNode = {
    ...node,
    GoalNode: true,
  }
  newGrid[rrow][rcol] = prevnodeupdated;
  newGrid[row][col] = newNode;
  return newGrid;
};

export default SearchVisualizer;

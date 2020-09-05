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
      mousePressed: false
    };
  }

  componentDidMount(){
    const grid = getInitialGrid();
    this.setState({grid: grid});
  }

  handleMouseDown(row,col){
    const newGrid = getNewGridWithWallToggled(this.state.grid, row, col);
    this.setState({grid: newGrid, mousePressed: true});
    console.log("Mouse clicked")
  }

  handleMouseEnter(row,col){
    if(!this.state.mousePressed) return;
    const newGrid = getNewGridWithWallToggled(this.state.grid,row,col);
    this.setState({grid: newGrid});
    console.log("drawing to")
    console.log(row,col)
  }

  handleMouseUp(){
    this.setState({mousePressed: false});
    console.log("Mouse Released")
  }



  render(){
    const {grid, mousePressed} = this.state;

    return(
      <>
        <button>
          Run
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

const getInitialGrid = () => {
  const grid = [];
  for(let row = 0; row< 10; row ++){
    const currentRow = [];
    for(let col = 0; col < 25; col ++){
      currentRow.push(createNode(col,row));
    }
    grid.push(currentRow);
  }
  return grid;
};

const createNode = (col,row) => {
  return {col,row,StartNode: row === START_NODE_ROW && col === START_NODE_COL,
  GoalNode: row === FINISH_NODE_ROW && col === FINISH_NODE_COL,
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

export default SearchVisualizer;

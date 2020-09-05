import React from "react";
import Node from "./Node"
import{dijkstra, getNodesInShortestPathOrder} from "./dijkstra"

import "./SearchVisualizer.css";



class SearchVisualizer extends React.Component{
  constructor(props){
    super(props);
    this.state = {
      grid: [],
      gridSize : [15,35],
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
    const size = this.state.gridSize;
    const grid = getInitialGrid(startNodePos, endNodePos, size);
    this.setState({grid: grid});
  }

  defaultGrid(){
    const startNodePos = this.state.startNodePos;
    const endNodePos = this.state.goalNodePos;
    const size = this.state.gridSize;
    const grid = getInitialGrid(startNodePos, endNodePos, size);
    this.setState({grid: grid, startNodePos: startNodePos, endNodePos: endNodePos});
    for(let row = 0; row<this.state.grid.length; row++){
      for(let col = 0; col < this.state.grid[row].length; col++){
        if(!grid[row][col].StartNode && !grid[row][col].GoalNode){
          let el = document.getElementById(`node-${row}-${col}`);
          el.className = "node";
        }
      }
    }
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
      console.log(row,col);
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

  animateShortestPath(nodesInShortestPathOrder) {
    for (let i = 0; i < nodesInShortestPathOrder.length; i++) {
      setTimeout(() => {
        const node = nodesInShortestPathOrder[i];
        if((node.row !== this.state.startNodePos[0] || node.col !== this.state.startNodePos[1]) &&
              (node.row !== this.state.goalNodePos[0] || node.col !== this.state.goalNodePos[1])){
                document.getElementById(`node-${node.row}-${node.col}`).className =
                'node node-shortest-path';
        }
      }, 10 * i);

    }
  }

  animateDijkstra(visitedNodesInOrder, nodesInShortestPathOrder){
    for(let i = 0; i <= visitedNodesInOrder.length; i ++){
      if(i === visitedNodesInOrder.length){
        setTimeout(()=>{
          this.animateShortestPath(nodesInShortestPathOrder);
        }, 10*i);
        return;
      }
      setTimeout(()=>{
        const node = visitedNodesInOrder[i];
        if((node.row !== this.state.startNodePos[0] || node.col !== this.state.startNodePos[1]) &&
              (node.row !== this.state.goalNodePos[0] || node.col !== this.state.goalNodePos[1])){
                let el = document.getElementById(`node-${node.row}-${node.col}`)
                el.className = 'node node-visited';
              }
      }, 10*i);
    }

  }

  visualizeDijkstra(){
    const newGrid = resetGrid(this.state.grid); //Need to make this way more rigorous, preserve WallNodes, reset distances...
    this.setState({grid: newGrid});
    const grid = this.state.grid;
    const startNode = grid[this.state.startNodePos[0]][this.state.startNodePos[1]];
    const goalNode = grid[this.state.goalNodePos[0]][this.state.goalNodePos[1]];
    console.log(startNode);
    const visitedNodesInOrder = dijkstra(grid, startNode, goalNode);
    const nodesInShortestPathOrder = getNodesInShortestPathOrder(goalNode);
    this.animateDijkstra(visitedNodesInOrder, nodesInShortestPathOrder);
  }


  render(){
    const {grid, mousePressed} = this.state;

    return(
      <>

        <button onClick = {() => this.visualizeDijkstra()}>
          Run Search
        </button>
        <button onClick = {() => this.defaultGrid()}>
          Remove Walls
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

const getInitialGrid = (startNodePos,endNodePos, size) => {
  const grid = [];
  for(let row = 0; row< size[0]; row ++){
    const currentRow = [];
    for(let col = 0; col < size[1]; col ++){
      currentRow.push(createNode(col,row, startNodePos,endNodePos));
    }
    grid.push(currentRow);
  }
  return grid;
};

const resetGrid= (grid) => {
  const newGrid = grid.slice();
  for(let row = 0; row < grid.length; row++){
    for(let col =0; col < grid[row].length; col++){
      const node = newGrid[row][col];
      if(!node.StartNode && !node.GoalNode && !node.WallNode){
        const newNode = createNode(col,row,[-1,-1],[-1,-1]) // ensure it doesnt get mistaken for a start/goalnode
        newGrid[row][col] = newNode;
        let el = document.getElementById(`node-${row}-${col}`);
        el.className = "node";
      }
      else if(node.StartNode){
        const newNode = createNode(col,row, [row,col], [-1,-1]);
        newGrid[row][col] = newNode;
      }
      else if(node.GoalNode){
        const newNode = createNode(col,row, [-1,-1], [row,col]);
        newGrid[row][col] = newNode;
      }
    }
  }
  return newGrid;
}

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

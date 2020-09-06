export function astar(grid, startNode, goalNode){
  const visitedNodesInOrder = [];
  startNode.distance = 0;
  const unvisitedNodes = getAllNodes(grid);
  while(!!unvisitedNodes.length){
    sortNodesByDistanceHeuristic(unvisitedNodes, goalNode)
    const closestNode = unvisitedNodes.shift()

    if(closestNode.WallNode) continue;
    if(closestNode.distance == Infinity) return visitedNodesInOrder;
    closestNode.isVisited = true;
    visitedNodesInOrder.push(closestNode);
    if(closestNode === goalNode) return visitedNodesInOrder;
    updateUnvisitedNeighbors(closestNode, grid);
  }
}
function getAllNodes(grid){
  const nodes = [];
  for(const row of grid){
    for(const node of row){
      nodes.push(node);
    }
  }
  return nodes;
}

function updateUnvisitedNeighbors(node,grid){
  const unvisitedNeighbors = getUnvisitedNeighbors(node,grid);
  for(const neighbor of unvisitedNeighbors){
    neighbor.distance = node.distance + 1;
    neighbor.previousNode = node;
  }
}

function getUnvisitedNeighbors(node,grid){
  const neighbors = []
  const {col,row} = node;
  console.log("neighbors")
  console.log(neighbors)
  if(row > 0) neighbors.push(grid[row-1][col]);
  if(row<grid.length-1) neighbors.push(grid[row+1][col]);
  if(col>0) neighbors.push(grid[row][col-1]);
  if(col< grid[0].length -1) neighbors.push(grid[row][col+1]);
  return neighbors.filter(neighbor => !neighbor.isVisited);
}

function sortNodesByDistanceHeuristic(unvisitedNodes, endNode){
  unvisitedNodes.sort((nodeA, nodeB)=> (nodeA.distance + heuristic(nodeA, endNode)) - (nodeB.distance + heuristic(nodeB, endNode)))
}

function heuristic(node, endNode){
  //manhattan distance heuristic
  return Math.abs(node.row-endNode.row) + Math.abs(node.col - endNode.col);
  //absolute distance
  // return Math.ceil(Math.sqrt(
  //   Math.pow(endNode.row - node.row, 2) + Math.pow(endNode.col - node.col, 2)
  // ));
}

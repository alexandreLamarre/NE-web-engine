export function greedy(grid, startNode, goalNode){
  const visitedNodesInOrder = [];
  startNode.distance = 0;
  const unvisitedNodes = getAllNodes(grid);
  console.log("greedy")
  let curNode = startNode;
  while(!!unvisitedNodes.length){
    sortNodesByDistanceHeuristic(unvisitedNodes, goalNode, curNode);
    const closestNode = unvisitedNodes.shift()
    curNode = closestNode;
    if(closestNode.WallNode) continue;
    if(closestNode.distance == Infinity) return visitedNodesInOrder;
    closestNode.isVisited = true;
    visitedNodesInOrder.push(closestNode);
    if(closestNode === goalNode) return visitedNodesInOrder;
    updateUnvisitedNeighbors(closestNode, grid, goalNode);
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

function updateUnvisitedNeighbors(node,grid,endNode){
  const unvisitedNeighbors = getUnvisitedNeighbors(node,grid);
  for(const neighbor of unvisitedNeighbors){
    // distance is actually distance to the goal
    //Also take into account distance to goal
    neighbor.distance = Math.abs(endNode.row - neighbor.row) + Math.abs(endNode.col - neighbor.col);
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

function sortNodesByDistanceHeuristic(unvisitedNodes, endNode, currentNode){
  unvisitedNodes.sort((nodeA,nodeB) => nodeA.distance - nodeB.distance)
}

// function heuristic(node, endNode){
//   if(node.row > 0 &&)
//   return Math.abs(node.row-endNode.row) + Math.abs(node.col - endNode.col);
  //manhattan distance heuristic
  // return Math.abs(node.row-endNode.row) + Math.abs(node.col - node)
  //absolute distance
  // return Math.sqrt(
  //   Math.pow(endNode.row - node.row, 2) + Math.pow(endNode.col - node.col, 2)
  // );
// }

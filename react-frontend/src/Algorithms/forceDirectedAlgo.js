var CREP = 20;
var CSPRING = 20;
var lx = 0;
var ly = 0;
/**
* Basic spring embedding algorithm
*/
export function forceDirectedLayout(vertices,edges,graph_distancex, graph_distancey, iterations, threshold, constant, cspring, crep){
  // relevant constants for spring embedding
  lx = graph_distancex;
  ly = graph_distancey;
  const K = iterations === undefined ? 100: iterations;
  const epsilon = threshold === undefined? 0.1: threshold;
  const delta = constant === undefined? 1.5: constant;
  CREP = cspring === undefined? 20: cspring;
  CSPRING = crep === undefined? 20: crep;

  //make copies of input
  let new_vertices = [];
  for(let i= 0; i < vertices.length; i++){
    new_vertices.push(vertices[i].slice());
  }
  let new_edges = [];
  //make a copy of edges and copy references of new_vertices
  for(let i = 0; i < vertices.length; i++){
    for(let j = 0; j < vertices.length; j++){
      for(let k =0; k < edges.length; k++){
        if(i === edges[k][0] && j === edges[k][1]){
          new_edges.push(new_vertices[i].slice(),new_vertices[j].slice());
        }
      }
    }
  }

  let t = 1;
  let maxFvt = Infinity;
  let animations = [];

  while(t<K && maxFvt > epsilon){
    let force_list = [];
    for(let i =0; i < new_vertices.length; i++){
      let f = [0,0]; // should be two dimensional
      let vert_connected = []; //represents vertices we should not repulse later
      for(let j = 0; j < new_edges.length; j++){
        //vertices should attract
        if(i === new_edges[j][0] && i !== new_edges[j][1]){
          const calcs = fattract(new_vertices[new_edges[j][0]], new_vertices[new_edges[j][1]]);
          // console.log(calcs);
          f[0] += calcs[0]; // should be two dimensional
          f[1] += calcs[1];
          vert_connected.push(new_edges[j][1]);
        }
        //vertices should attract
        if(i === new_edges[j][1] && i !== new_edges[j][0]){
          const calcs = fattract(new_vertices[new_edges[j][0]], new_vertices[new_edges[j][1]])
          f[0] += calcs[0]; // should be two dimensional
          f[1] += calcs[1];
          vert_connected.push(new_edges[j][0]);
        }
      }
      for(let j =0; j < new_vertices.length; j++){
        if(i === j ) continue;
        let connected = false;
        for(let k = 0; k < vert_connected.length; k++){
          if(j === vert_connected[k]) connected = true;
        }
        // vertices should repluse one another
        if(!connected){
          const calcs = frepulse(new_vertices[i], new_vertices[j]);
          f[0] += calcs[0];// should be two dimensional
          f[1] += calcs[1];
        }
      }
      force_list.push(f)
    }
    const iteration_animation = [];
    for(let i = 0; i < new_vertices.length; i++){
      const new_x = new_vertices[i][0] + delta*force_list[i][0];
      const new_y = new_vertices[i][1] + delta*force_list[i][1];
      new_vertices[i][0] = new_x//(new_x > graph_distancex-3)? (graph_distancex-3): ((new_x-3) < 0)? 0: (new_x-3); // should be two dimensional
      new_vertices[i][1] = new_y//(new_y > graph_distancey-3)? (graph_distancey-3): ((new_y -3)< 0)? 0: (new_y-3);
      iteration_animation.push(new_vertices[i].slice());
      const max_dist = distance(force_list[i], [0,0]);
      if(maxFvt === Infinity){
        maxFvt = max_dist;
      }
      else{
        maxFvt = maxFvt > max_dist? maxFvt: max_dist;
      }
    }
    animations.push(iteration_animation);
    t += 1
  }
  // animations.push(new_vertices.slice());
  const iteration_animation = [];
  for(let i = 0; i < new_vertices.length; i ++){
    if(new_vertices[i][0] < 0) new_vertices[i][0] = 0;
    if(new_vertices[i][1] < 0)new_vertices[i][1] = 0;
    if(new_vertices[i][0] > graph_distancex -6) new_vertices[i][0] = graph_distancex-6;
    if(new_vertices[i][1] > graph_distancey - 6) new_vertices[i][1] = graph_distancey-6;
    iteration_animation.push(new_vertices[i].slice())
  }
  animations.push(iteration_animation);
  return [new_vertices, animations];
}

function frepulse(x,y){
  const dist = distance(x,y);
  if(dist === 0){
     console.log("error");
     console.log(x);
     console.log(y);
   }
  const unitV = unitVector(x,y);
  return [(unitV[0]*CREP)/dist, (unitV[1]*CREP)/dist];

}

function fattract(x,y){
  const dist = distance(x,y);
  const unitV = unitVector(x,y);

  return [CSPRING* (Math.log(distance(x,y))/(lx))* unitV[0],
          CSPRING* (Math.log(distance(x,y))/(ly))*unitV[1]];
}

function distance(x,y){
  return  Math.sqrt(Math.pow((x[0] - y[0]), 2) + Math.pow((x[1] - y[1]), 2));
}

/**
* UnitVector from X to Y
*/
function unitVector(x,y){
  const new_x = y[0] - x[0];
  const new_y = y[1] - x[1];
  const dist = distance(x,y);
  return [new_x/dist, new_y/dist];
}
// export function forceDirectedLayout(vertices, edges){
//   let step = 1; // = initial step length //not sure what this value is supposed to be
//   let converged = false;
//   const K = vertices.length;
//
//   while(!converged){
//     let x0 = x; //not sure what this does;
//
//     for(let i = 0; i < vertices.length; i++){
//       let f = 0;
//       for(let j=0; j<edges.length; j++){
//         if(vertices[i] === edges[j][0] || vertices[i] === edges[j][1]){
//           const x1 = edges[j][0][0];
//           const x2 = edges[j][1][0];
//           const y1 = edges[j][0][1];
//           const y2 = edges[j][1][1];
//           const dist = distance(x1,x2,y1,y2);
//           const fa = fattract(edges[j][0], edges[j][1]);
//           f += (fa/dist) //* (xj - xi) // again not sure what this does
//         }
//       }
//       for(let j = 0; j < vertices.length; j++){
//         if(i === j)continue;
//         const x1 = vertices[i][0];
//         const x2 = vertices[j][0];
//         const y1 = vertices[i][1];
//         const y2 = vertices[j][1];
//         const dist = distance(x1,x2,y1,y2);
//         const fr = frepulse(vertices[i], vertices[j]);
//         f += (fr/dist) // *(xj - xi) not sure what this does;
//       }
//       vertices[i] = vertices[i] + step *f/Math.abs(f)
//     }
//     if(distance(x0, x) < K*tol){
//       converged = true;
//     }
//   }
//
//   return x
//
// }
//
// function distance(x1,x2,y1,y2){
//   return Math.sqrt(Math.pow((x2-x1),2) + Math.pow((y2-y1),2));
// }
//
// function fattract(){
//
// }
//
// function frepulse(){
//
// }

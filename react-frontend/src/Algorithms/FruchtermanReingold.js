var lx =0;
var ly = 0;
const CGRAV = 0.5; // NEW PARAMETER
export function fruchtermanReingold(vertices,edges,graph_distancex, graph_distancey, iterations, threshold, constant){

  lx = graph_distancex;
  ly = graph_distancey;
  const K = iterations === undefined ? 300: iterations;
  const epsilon = threshold === undefined? 0.1: threshold;
  const delta = constant === undefined? 1.5: constant;

  const initial_temperature = graph_distancex*(1/10)

  const temperatureArray = [];
  const degreeArray = [];
  const centerConstant = 1/(vertices.length)
  const pBarycenter = [0,0];

  for(let i = 0; i < vertices.length; i++){
    let count = 0;
    for(let j = 0; j < edges.length; j++){
      if(i === edges[j][0] && i!== edges[j][1]){
        count ++;
      }
      if(i === edges[j][1] && i !== edges[j][0]){
        count ++;
      }
    }
    degreeArray.push(count);
    temperatureArray.push(initial_temperature);
    pBarycenter[0] += centerConstant*vertices[i][0]
    pBarycenter[1] += centerConstant*vertices[i][1]
  }



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
  let animations = [];
  let maxFvt = Infinity;
  while(t<K && maxFvt > epsilon){
    maxFvt = Infinity;
    let force_list = [];
    for(let i =0; i < new_vertices.length; i++){
      let f = [0,0]; // should be two dimensional
      for(let j = 0; j < new_edges.length; j++){
        //vertices should attract
        if(i === new_edges[j][0] && i !== new_edges[j][1]){
          const calcs = fattract(new_vertices[new_edges[j][0]], new_vertices[new_edges[j][1]]) *1/(nodeMass(degreeArray[j]));
          // console.log(calcs);
          f[0] += calcs[0]; // should be two dimensional
          f[1] += calcs[1];
        }
        //vertices should attract
        if(i === new_edges[j][1] && i !== new_edges[j][0]){
          const calcs = fattract(new_vertices[new_edges[j][0]], new_vertices[new_edges[j][1]]) *1/(nodeMass(degreeArray[j]));
          f[0] += calcs[0]; // should be two dimensional
          f[1] += calcs[1];
        }
      }
      for(let j =0; j < new_vertices.length; j++){
        if(i === j ) continue;
        // vertices should repluse one another
        const calcs = frepulse(new_vertices[i], new_vertices[j]);
        f[0] += calcs[0];// should be two dimensional
        f[1] += calcs[1];

      }
      const fgrav = CGRAV * degreeArray[i]
      const unitGravityVector = unitVector(vertices[i], pBarycenter);
      f[0] += fgrav * unitGravityVector[0];
      f[1] += fgrav * unitGravityVector[1];
      f[0] *= 1/(Math.pow(10,8));
      f[1] *= 1/(Math.pow(10,8));
      if(t!== 1){
        const previous = animations[t-2][i]
        const current = f;
        const cosAngle = (current[0]+previous[0] + current[1]+previous[1])/(distance(previous, [0,0]) + distance(current,[0,0]))
        if(cosAngle -0.5 < 1 && cosAngle+ 0.5>1) {
          temperatureArray[i] += graph_distancex/10;
        }
        if(cosAngle -0.5 <-1 && cosAngle+0.5 > -1) {
          temperatureArray[i] -= graph_distancex/10;
        }
      }
      // console.log(temperatureArray);
      console.log(temperatureArray);
      f[0] *= temperatureArray[i]*(1/100)
      f[1] *= temperatureArray[i]*(1/100)
      force_list.push(f)
      // console.log(f);
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
  return [(unitV[0]*Math.pow(lx,2))/dist, (unitV[1]*Math.pow(lx,2))/dist];
}

function fattract(x,y){
  const dist2 = Math.pow(distance(x,y),2);
  const unitV = unitVector(y,x);

  return [(dist2/lx)*unitV[0],
          (dist2/lx)*unitV[1]];
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

function nodeMass(v){
  return 1/(1+(v)/2);
}

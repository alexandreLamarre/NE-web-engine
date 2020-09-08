import React from "react";
import {forceDirectedLayout} from "./forceDirectedAlgo";

import "./Network.css";

// function animateNetwork(animations, canvas, og_vertices, og_edges, delta, width,height){
//   const ctx = canvas.getContext("2d");
//   let vertices = [];
//   let edges = [];
//
//   for(let i= 0; i < og_vertices.length; i++){
//     vertices.push(og_vertices[i].slice());
//   }
//
//   for(let i = 0; i < og_vertices.length; i++){
//     for(let j = 0; j < og_vertices.length; j++){
//       for(let k =0; k < og_edges.length; k++){
//         if(og_vertices[i] === og_edges[k][0] && og_vertices[j] === og_edges[k][1]){
//           edges.push(vertices[i],vertices[j]);
//         }
//       }
//     }
//   }
//
//   for(let k = 0; k < animations.length; k++){
//     for(let i = 0; i < vertices.length; i++){
//       vertices[i] = animations[k][i];
//     }
//     setTimeout(() => {
//       // ctx.clearRect(0,0,width,height);
//       for(let i =0; i < vertices.length; i++){
//         ctx.fillStyle= "#FF0000"
//         ctx.fillRect(vertices[i][0],vertices[i][1], 6, 6);
//       }
//
//       for(let j = 0; j < edges.length; j++){
//         ctx.beginPath();
//         ctx.globalAlpha = 0.2;
//         ctx.moveTo(edges[j][0][0]+3, edges[j][0][1]+3);
//         ctx.lineTo(edges[j][1][0]+3, edges[j][1][1]+3);
//         ctx.stroke();
//         ctx.closePath();
//       }
//     }, k *50);
//   }
// }


class NetworkVisualizer extends React.Component{
  constructor(props){
    super(props);
    this.canvas =  React.createRef();
    this.state ={
      width : 0,
      height: 0,
      vertices: [],
      edges: [],
      numE: 300,
      numV: 150,
      delta: 2,
      animations: [],
    };

    this.stateRef = React.createRef(this.state);
  }

  componentDidMount(){
    const w = window.innerWidth * 0.9;
    const h = window.innerHeight * 0.55;

    const [vertices, edges] = createRandomNetwork(w, h, this.state.numV, this.state.numE);
    this.setState({width: w, height: h, vertices: vertices, edges: edges});
  }

  componentDidUpdate(){
    this.canvas.current.width = this.state.width;
    this.canvas.current.height = this.state.height;
    const ctx = this.canvas.current.getContext("2d");
    for(let i =0; i < this.state.vertices.length; i++){
      ctx.fillStyle= "#FF0000"
      ctx.fillRect(this.state.vertices[i][0], this.state.vertices[i][1], 6, 6);
    }

    for(let j = 0; j < this.state.edges.length; j++){
      ctx.beginPath();
      ctx.globalAlpha = 0.2;
      const index1 = this.state.edges[j][0];
      const index2 = this.state.edges[j][1];
      ctx.moveTo(this.state.vertices[index1][0],this.state.vertices[index1][1] );
      ctx.lineTo(this.state.vertices[index2][0],this.state.vertices[index2][1] );
      // ctx.moveTo(this.state.vertices[j][0][0]+3, this.state.edges[j][0][1]+3);
      // ctx.lineTo(this.state.edges[j][1][0]+3, this.state.edges[j][1][1]+3);
      ctx.stroke();
      ctx.closePath();
    }
  }

  generateForceDirectedLayout(){
    const values = forceDirectedLayout(this.state.vertices, this.state.edges,this.state.width, this.state.height);
    const new_vertices = values[0];
    const animations = values[1];
    console.log(animations);
    // console.log(animations);
    // // animateNetwork(animations, this.canvas.current,this.state.vertices, this.state.edges, this.state.delta, this.state.width,this.state.height);
    this.animateNetwork(animations);
  }

  animateNetwork(animations){
    for(let k = 0; k < animations.length; k++){
      setTimeout(() => {
        this.setState({vertices: animations[k]});
      }, k*50)
    }
  }

  resetNetwork(){
    const [vertices, edges] = createRandomNetwork(this.state.width, this.state.height, this.state.numV, this.state.numE, this.state.width, this.state.height);

    this.setState({vertices: vertices, edges: edges})
  }

  // animateNetwork(animations){
  //   for(let i = 0; i < animations.length; i++){
  //     const vertices = this.state.vertices;
  //     for(let j= 0; j < vertices; j++){
  //       vertices[j][0] += this.delta * animations[i][j][0];
  //       vertices[j][1] += this.delta * animations[i][j][1];
  //     }
  //     this.setTimeout(() => {
  //       this.setState({vertices: vertices});
  //     }, i* 100);
  //   }
  // }

  componentWillUnmount(){
    cancelAnimationFrame(this.rAF)
  }

  render(){

    return <div>
            <canvas
            className = "networkCanvas" ref = {this.canvas}>
            </canvas>
            <button onClick = {() => this.generateForceDirectedLayout()}>
            Force Directed Layout
            </button>
            <button onClick = {() => this.resetNetwork()}>
            Reset Network
            </button>
           </div>
  }
}

export default NetworkVisualizer;

function createRandomNetwork(maxWidth, maxHeight, numV, numE){
  //create random vertices
  let vertices = [];
  for(let i = 0; i< numV; i++){
    vertices.push(createRandomPos(maxWidth, maxHeight))
  }
  let edges = [];
  for(let i = 0; i<numE; i++){
    edges.push(connectRandomVertices(vertices.length, vertices))
  }

  return [vertices,edges];
}

function createRandomPos(maxWidth, maxHeight){
  return [Math.random()*(maxWidth+1-3), Math.random()*(maxHeight+1-3)];
}

function connectRandomVertices(end, vertices){
  var random1 = Math.floor(Math.random()*end);
  var random2 = Math.floor(Math.random()*end);
  return [random1, random2];
}

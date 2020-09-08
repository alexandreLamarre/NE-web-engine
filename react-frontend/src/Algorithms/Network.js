import React from "react";
import {forceDirectedLayout} from "./forceDirectedAlgo";

import "./Network.css";

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
      ctx.moveTo(this.state.edges[j][0][0]+3, this.state.edges[j][0][1]+3);
      ctx.lineTo(this.state.edges[j][1][0]+3, this.state.edges[j][1][1]+3);
      ctx.stroke();
      ctx.closePath();
    }
  }

  generateForceDirectedLayout(){
    const values = forceDirectedLayout(this.state.vertices, this.state.edges,this.state.width, this.state.height);
    const new_vertices = values[0];
    const animations = values[1];
    // console.log(new_vertices);
    // console.log(animations);
    this.setState({vertices: new_vertices});
    // this.animateNetwork(animations);
  }
  // animateNetwork(animations){
  //   for(let i = 0; i < animations.length; i++){
  //     setTimeout(() => {
  //       const vertices = this.stateRef.current.vertices;
  //       for(let j = 0; j < vertices.length; j++){
  //         vertices[j][0] += this.delta* animations[i][j][0];
  //         vertices[j][1] += this.delta* animations[i][j][1];
  //       }
  //       this.setState({vertices: vertices})
  //     }, i * 50);
  //   }
  // }

  resetNetwork(){
    const [vertices, edges] = createRandomNetwork(this.state.width, this.state.height, this.state.numV, this.state.numE);

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
  return [vertices[random1], vertices[random2]];
}

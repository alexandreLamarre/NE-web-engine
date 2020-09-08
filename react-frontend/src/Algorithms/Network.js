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
    };
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
    // this.rAF = requestAnimationFrame(this.animateNetwork(animations))
    // setTimeout(() => {
    //   console.log("supposedly stopped")
    //   cancelAnimationFrame(this.rAF);
    // }, 1000);

  }

  animateNetwork(animations){
    if(animations !== undefined){
      var af = animations.pop();
      console.log(af);
      const new_vertices = this.state.vertices;
      if(af !== undefined){
        for(let i = 0; i < af.length; i++){
          new_vertices[i][0] = this.delta * af[i][0];
          new_vertices[i][1] = this.delta * af[i][1];
        }
      }
      else{
        cancelAnimationFrame(this.rAF);
      }
      this.setState(prevState => ({new_vertices: new_vertices}));
      if(animations !== undefined){
        this.rAF = requestAnimationFrame(this.animateNetwork(animations))
      }
    }
  }

  resetNetwork(){
    const [vertices, edges] = createRandomNetwork(this.state.width, this.state.height, this.state.numV, this.state.numE);

    this.setState({vertices: vertices, edges: edges})
  }

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

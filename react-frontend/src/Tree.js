import React from "react"
import "./Tree.css"

function draw_a_tree(color){

  const canvas = document.getElementById("tree")
  canvas.width = 300
  canvas.height = 300

  const ctx = canvas.getContext("2d")

  function drawTree(startX, startY, len, angle, branchWidth, color1, color2){
    ctx.beginPath();
    ctx.save();
    ctx.strokeStyle = color1;
    ctx.fillStyle = color2;
    ctx.lineWidth = branchWidth;
    ctx.translate(startX,startY);
    ctx.rotate(angle*3.14159265358979/180);
    ctx.moveTo(0,0);
    ctx.lineTo(0, -len);
    ctx.stroke();

    if(len < 5){
      ctx.restore();
      return;
    }

    drawTree(0,-len,len*0.75, angle + 7, branchWidth, color, color);
    drawTree(0, -len,len*0.75, angle - 7, branchWidth, color, color);
    ctx.restore();

  }

  drawTree(canvas.width/2, canvas.height, 60,0, 2, color, color);
}


class Tree extends React.Component{
  constructor(props){
    super(props)
    this.state = {value: 'true'}
  }


  componentDidMount(){
    draw_a_tree("white");
    this.setState({value: 'false'});
  }

  animateTree(){
    draw_a_tree("#"+Math.floor(Math.random()*16777215).toString(16));
    console.log("animate");
  }

  draw_initial(){
    draw_a_tree("white");
  }
  render(){
    return(

      <canvas id = "tree">
      </canvas>
    )
  }
}

export default Tree

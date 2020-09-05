import React from "react"
function drawArrowhead(ctx,locx, locy, angle, sizex, sizey) {
    var hx = sizex / 2;
    var hy = sizey / 2;
    ctx.translate((locx ), (locy));
    ctx.rotate(angle);
    ctx.translate(-hx,-hy);

        ctx.beginPath();
    ctx.moveTo(0,0);
    ctx.lineTo(0,1*sizey);
    ctx.lineTo(1*sizex,1*hy);
    ctx.fill();

    ctx.translate(hx,hy);
    ctx.rotate(-angle);
    ctx.translate(-locx,-locy);
}

class MarkovGraph extends React.Component{
  constructor(props){
    super(props);

    this.state = {
      canvas_styles : {
        background: "#FFFFFF",
        border:"2px solid #000000"
      },
      height : 200,
      width : 800,
      states: ["a", "b", "c", "d", "e", "f", "g", "h", "i"],
      transitions: [[]]
    };

    this.canvas = React.createRef();

    this.setStates = this.setStates.bind(this);
    this.setTransitions = this.setTransitions.bind(this);

  }

  componentDidMount(){

    this.setState({height: 200* Math.ceil(this.state.states.length/7)})
  }
  componentDidUpdate(){
    this.drawToCanvas(this.getStates(), this.getTransitions());
  }

  setStates(new_states){
    this.setState({states: new_states});
  }

  setTransitions(new_transitions){
    this.setState({transitions: new_transitions});
  }

  getStates(){
    return this.state.states;
  }

  getTransitions(){
    return this.state.transitions;
  }
  drawToCanvas(states, transitions){
    //states is a 1 dimensional list of strings
    //transitions is a 2 dimensional list of probabilities

    var margin = 20;
    var c = this.canvas.current;
    var ctx = c.getContext("2d");
    ctx.beginPath();
    // draw node circles
    // Only Suppport 7 nodes per row
    var num_graph_rows = Math.ceil(states.length/7);
    var top_and_bottom = []

    for(var i =0; i<states.length; i ++){
      var radius = 40;
      var xPos = margin + radius+ (c.width)/(states.length) * i
      var yPos = 100 //+ 200*Math.floor(Math.abs(i-1)/7);
      var text = ctx.measureText(states[i]);
      ctx.fillText(states[i], xPos-Math.min(text.width/2, radius), yPos, 2*radius);
      ctx.moveTo(xPos+radius,yPos);
      top_and_bottom.push([[xPos, yPos-radius], [xPos,yPos+radius]]);
      ctx.arc(xPos, yPos, radius, 0, 2*Math.PI);
    }
    console.log(top_and_bottom);
    //assumption: transitions.length matches state.length and transitions[i].length
    // matches states.length
    for(var i =0; i < transitions.length; i++){
      for(var j = 0; j<transitions[i].length; j ++){
        console.log(transitions[i][j])
        if(transitions[i][j]> 0){
          if(i == j){
            var x1 = top_and_bottom[i][1][0];
            var y1 = top_and_bottom[i][1][1];
            ctx.moveTo(x1+20,y1+20)
            ctx.arc(x1,y1+20,20, 0, 2*Math.PI)
            // ctx.moveTo(x1,y1);
            // ctx.quadraticCurveTo(x1+30,(y1+y2)/2,x2,y2)
            //
            // ctx.moveTo(x2,y2);
            // ctx.quadraticCurveTo(x1-30,(y1+y2)/2,x1,y1)
          }
          else{
            console.log("should be drawing");
            var x1 = top_and_bottom[i][0][0];
            var y1 = top_and_bottom[i][0][1];
            var x2 = top_and_bottom[j][0][0];
            var y2 = top_and_bottom[j][0][1];
            var radius = 40;
            ctx.moveTo(x1,y1)
            ctx.quadraticCurveTo((x1+x2)/2, y1- 80, x2, y2);
            ctx.stroke();
            //draw arrowheads
            var angle = Math.atan2((y2-y1- 80), (x2-(x1+x2)/2));
            var arrowSizeX = 12;
            var arrowSizeY = 12;
            drawArrowhead(ctx,x2,y2,angle,arrowSizeX, arrowSizeY);
          }
        }
      }
    }
    ctx.stroke();
  }

  render(){
    return <div>
            <canvas ref = {this.canvas} width = "800" height = {this.state.height} style = {this.state.canvas_styles}>
            </canvas>
           </div>
  }
}

export default MarkovGraph;

import React from "react"
import "./CLI.css"
import Tree from "./Tree"



function createNode(element){
  return document.createElement(element);
}

function append(parent,el){
  return parent.appendChild(el);
}

function process_commands(ul,data){
  var n;
  var i;
  var j;
  var k;
  console.log(data);
  for(n = 0; n<data.info.length;n++){
    if(data.labels[n] !== null){
      let label = createNode("h2");
      label.innerHTML = data.labels[n];
      append(ul,label);
      let report = createNode("a")
      report.innerHTML = "Report a bug"
      report.href = "https://github.com/alexandreLamarre/NE-web-engine/issues/new"
      report.target = "_blank"
      append(ul, report)
    }
    if(data.errors[n] !== null || data.errors !== ""){
      let errors = createNode("p")
      // console.log(data.errors[n])
      errors.innerHTML = data.errors[n]
      errors.style = "color:#FE7272;"
      append(ul,errors)
    }
    if(data.labels[n] === "ZEROES" || data.labels[n] === "PARTIALDERIVATIVE" || data.labels[n] === "PARTIALINTEGRAL"){
    for(i = 0; i <data.info[n].length;i++){
      let sublabel = createNode("h3");
      sublabel.innerHTML = data.info[n][i][0];
      append(ul,sublabel);
      for(j = 0; j<data.info[n][i][1].length; j++){
        let sublabel_function  = createNode("h4");
        sublabel_function.innerHTML = "function: "+ data.info[n][i][1][j][0];
        append(ul, sublabel_function);
        for(k=0; k<data.info[n][i][1][j][1].length; k++){
           let math_var = createNode("h5")
           math_var.innerHTML = "In terms of variable: " + data.info[n][i][1][j][1][k][0];
           append(ul, math_var)
           let math_info = createNode("img")
           // console.log("hello")
           // console.log(data.info[n][i][1][j][1][k][1])
           math_info.src = "data:image/png;base64,"+ data.info[n][i][1][j][1][k][1]
           append(ul, math_info)

        }
      }
    }
  }
  if(data.labels[n] === "PLOT"){
    for(i = 0; i <data.info[n].length; i++){
      let math_info = createNode("img")
      // console.log("math_info")
      // console.log(data.info[n][i][1])
      math_info.src = "data:image/png;base64,"+ data.info[n][i][1]
      append(ul, math_info)
    }
  }
  if(data.labels[n] == "CHAIN"){
    // console.log("data.info[n].length")
    // console.log(data.info[n].length)
    for(i = 0; i < data.info[n].length; i ++){
      let statsublabel = createNode("h3");
      statsublabel.innerHTML = "Stationary Distribution";
      append(ul,statsublabel);
      for(j = 0; j < data.info[n][i][1].length; j ++){
        let stationary = createNode("img");
        stationary.src = "data:image/png;base64," + data.info[n][i][1][j][0]
        append(ul, stationary)

        let actual = createNode("h4")
        var output_str = ""
        // console.log("data.info[n][i][0]")
        // console.log(data.info[n][i][0][0][0])
        // console.log(data.info[n][i][1][0][1])
        console.log(data.info[n][i][0][j][0])
        for(k = 0; k<data.info[n][i][1][j][1].length; k++){
          // output_str += data.info[n][i][0]
          output_str += data.info[n][i][0][j][0][k] + " : " + data.info[n][i][1][j][1][k]+ "<br>"
        }
        actual.innerHTML = "Actual Stationary Distribution:  <br>" + output_str
        append(ul, actual)
      }


      let simulationsublabel = createNode("h3");
      simulationsublabel.innerHTML = "Simulation History";
      append(ul,simulationsublabel);
      for(j = 0; j < data.info[n][i][2].length; j++){
        let simulations = createNode("img")
        simulations.src = "data:image/png;base64,"+data.info[n][i][2][j]
        append(ul, simulations);
      }
    }
  }
  }

}

function process_input(ul, data){
  ul.style = "background-color: #145494"
  var length = ul.childNodes.length
  var i;
  for(i = 0; i <length; i ++){
    ul.removeChild(ul.childNodes[0]);
  }


  let originalInput = createNode("p");
  if (data.input === "" || data.input === null){
    originalInput.innerHTML = "Your input : None";

  }
  else{
    originalInput.innerHTML = "Your input : " + data.input;
  }
  append(ul, originalInput);
  let interpreted_info = createNode("p");
  if (data.interpreted === "" || data.interpreted == null){
    interpreted_info.innerHTML = "Interpreted input : None";
    interpreted_info.style = "color:#FE7272 ;"
  }
  else{
    interpreted_info.innerHTML = "Interpreted input: " + data.interpreted;
  }
  append(ul,interpreted_info);

  let error_info = createNode("p");
  if (data.errors === "" || data.errors === null){
    //do nothing
  }
  else{
    error_info.innerHTML = "Errors : " + data.errors;
    error_info.style="color:#FE7272;";
    append(ul, error_info);
  }
}



async function getInterpretedInput(input, component, animation){
  const url = "/input";
  const ul = document.getElementById("ul-info")
  let response = await fetch(url, {method: "POST", body: input,
    headers: new Headers({
    "content-type": "application/json"
    })}
  );
  let data = await response.json();
  console.log(data);
  process_input(ul, data);
  let commands_to_run = data.commands

  for(var i = 0; i < commands_to_run.length; i++){

    await getCommand(JSON.stringify(commands_to_run[i]));
  }
  clearInterval(animation);
  component.tree.current.draw_initial();
  component.setState({disabled:false});
}

async function getCommand(command){
  const ul = document.getElementById("ul-info");
  const url = "/input/commands";
  let response = await fetch(url, {method: "POST", body: command,
    headers: new Headers({
    "content-type": "application/json"
      })
    }
  );

  let data = await response.json();
  process_commands(ul,data)

}
// ================================================================================================

class CLI extends React.Component{
  constructor(props){
    super(props)
    this.tree = React.createRef();
    this.state = {value: '',
                  disabled: false,
                label: ''}

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event){
    this.setState({value: event.target.value})
  }
  componentWillUnmount(){
    clearInterval(this.tree.current.animateTree);
  }

  handleSubmit(event){

    // const url = "http://localhost:5000/input/" + this.state.value
    event.preventDefault();
    if(this.state.disabled === false){
      this.setState({disabled : true})
      const that = this
      var loadingAnimation = setInterval(this.tree.current.animateTree,350);

      getInterpretedInput(JSON.stringify(this.state.value), that, loadingAnimation);


    //   fetch(url, {method: "POST", body: JSON.stringify(this.state.value),
    //   headers: new Headers({
    //     "content-type": "application/json"
    //   })}
    //   ).then(function(response) {
    //   resp = response
    //   response.json().then(function(data) {
    //
    //     // console.log(data);
    //     process_input(ul,data)
    //   });
    // })
    // .catch(function(error) {
    //   console.log("Fetch error: " + error);
    // });


  //   fetch(url+"/commands", {method: "POST", body: JSON.stringify(this.state.value),
  //   headers: new Headers({
  //     "content-type": "application/json"
  //   })}
  //   ).then(function(response) {
  //
  //   resp = response
  //   response.json().then(function(data) {
  //
  //     // console.log(data);
  //     process_commands(ul,data);
  //     clearInterval(loadingAnimation);
  //     treeReference.current.draw_initial();
  //     that.setState({disabled:false})
  //   });
  // })
  // .catch(function(error) {
  //   console.log("Fetch error: " + error);
  //   clearInterval(loadingAnimation);
  //   that.setState({disabled:false})
  // });
  }
  }

  render(){
    return(

      <form onSubmit = {this.handleSubmit}>
        <label>

        <Tree ref={this.tree} ></Tree>
        <h6>
          Non-Euclidean Computational Engine - Functions
        </h6>
        <div className = "help">
          <a href = "https://github.com/alexandreLamarre/NE-web-engine#Quick-guide" rel="noopener" target="_blank">Help</a>
        </div>
        <div id="cliText">
          <textarea value ={this.state.value}
            onChange = {this.handleChange} draggable = "false" cols = "68" rows = "2"/>
          <input type = "submit" value = "Run" disabled = {this.state.disabled}/>
        </div>
        </label>

      </form>
    )
  }
}

export default CLI

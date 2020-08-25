import React from "react"
import "./CLI.css"
import ReactDOM from 'react-dom'
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
  for(n = 0; n<data.info.length;n++){
    if(data.labels[n] != null){
      let label = createNode("h2");
      label.innerHTML = data.labels[n];
      append(ul,label);
      let report = createNode("a")
      report.innerHTML = "Report a bug"
      report.href = "https://github.com/alexandreLamarre/NE-web-engine/issues/new"
      report.target = "_blank"
      append(ul, report)
    }
    if(data.errors[n] != null || data.errors != ""){
      let errors = createNode("p")
      console.log(data.errors[n])
      errors.innerHTML = data.errors[n]
      errors.style = "color:#FE7272;"
      append(ul,errors)
    }
    if(data.labels[n] == "ZEROES" || data.labels[n] == "PARTIALDERIVATIVE" || data.labels[n] == "PARTIALINTEGRAL"){
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
  if(data.labels[n] == "PLOT"){
    for(i = 0; i <data.info[n].length; i++){
      let math_info = createNode("img")
      console.log("math_info")
      console.log(data.info[n][i][1])
      math_info.src = "data:image/png;base64,"+ `${data.info[n][i][1]}`
      append(ul, math_info)
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
  if (data.input == "" || data.input == null){
    originalInput.innerHTML = "Your input : None";

  }
  else{
    originalInput.innerHTML = "Your input : " + data.input;
  }
  append(ul, originalInput);
  let interpreted_info = createNode("p");
  if (data.interpreted == "" || data.interpreted == null){
    interpreted_info.innerHTML = "Interpreted input : None";
  }
  else{
    interpreted_info.innerHTML = "Interpreted input: " + data.interpreted;
  }
  append(ul,interpreted_info);

  let error_info = createNode("p");
  if (data.errors == "" || data.errors == null){
    //do nothing
  }
  else{
    error_info.innerHTML = "Errors : " + data.errors;
    error_info.style="color:#FE7272;";
    append(ul, error_info);
  }
}

// ================================================================================================

class CLI extends React.Component{
  constructor(props){
    super(props)
    this.tree = React.createRef();
    this.state = {value: '',
                  interepreted: '',
                label: ''}

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleHelp = this.handleHelp.bind(this);

  }

  handleChange(event){
    this.setState({value: event.target.value})
  }

  handleHelp(){

  }

  handleSubmit(event){

    // const url = "http://localhost:5000/input/" + this.state.value
    event.preventDefault()
    var loadingAnimation = setInterval(this.tree.current.animateTree,300);
    var treeReference = this.tree
    const url = "/input"
    const ul = document.getElementById("ul-info")
    let resp = ""
    fetch(url, {method: "POST", body: JSON.stringify(this.state.value),
    headers: new Headers({
      "content-type": "application/json"
    })}
    ).then(function(response) {
    resp = response
    response.json().then(function(data) {

      console.log(data);
      process_input(ul,data)
    });
  })
  .catch(function(error) {
    console.log("Fetch error: " + error);
  });
  fetch(url+"/commands", {method: "POST", body: JSON.stringify(this.state.value),
  headers: new Headers({
    "content-type": "application/json"
  })}
  ).then(function(response) {

  resp = response
  response.json().then(function(data) {

    console.log(data);
    process_commands(ul,data);
    clearInterval(loadingAnimation);
    treeReference.current.draw_initial();
  });
})
.catch(function(error) {
  console.log("Fetch error: " + error);
  clearInterval(loadingAnimation);
});
  }

  render(){
    return(

      <form onSubmit = {this.handleSubmit}>
        <label>
        <Tree ref={this.tree} ></Tree>
        <h6>
          Non-Euclidean Computational Engine - Functions
        </h6>
        <div id="cliText">
          <textarea value ={this.state.value}
            onChange = {this.handleChange} draggable = "false" cols = "70" rows = "2"/>
          <input type = "submit" value = "Run" />
        </div>
        </label>

      </form>
    )
  }
}

export default CLI

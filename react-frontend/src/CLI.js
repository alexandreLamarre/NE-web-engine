import React from "react"
import "./CLI.css"

function createNode(element){
  return document.createElement(element);
}

function append(parent,el){
  return parent.appendChild(el);
}

function process_input(ul, data){
  ul.style = "background-color: #1B2631"
  var length = ul.childNodes.length
  var i;
  for(i = 0; i <length; i ++){
    ul.removeChild(ul.childNodes[0]);
  }
  let label = createNode("h2")
  label.innerHTML = `${data.label}`

  let interpreted = createNode("h3")
  interpreted.innerHTML = ` Interpreted`
  append(ul,interpreted)
  let interpreted_info = createNode("p")
  if (data.interpreted == ""){
    interpreted_info.innerHTML = `None`
  }
  else{
    interpreted_info.innerHTML = `${data.interpreted}$`
  }
  append(ul,interpreted_info)
  let uninterpreted = createNode("h3")
  uninterpreted.innerHTML = ` Uninterpreted`
  append(ul,uninterpreted)
  let uninterpreted_info = createNode("p")
  if (data.uninterpreted == ""){
    uninterpreted_info.innerHTML = `None`
  }
  else{
    uninterpreted_info.innerHTML = `${data.uninterpreted}`
  }
  append(ul,uninterpreted_info)
  let errors = createNode("h3")
  errors.innerHTML = `Errors`
  append(ul,errors)
  let error_info = createNode("p")
  if (data.Errors == ""){
    error_info.innerHTML = `None`
  }
  else{
    error_info.innerHTML = `${data.interpreted}`
  }
  append(ul, error_info)
}
class CLI extends React.Component{
  constructor(props){
    super(props)
    this.state = {value: '',
                  interepreted: '',
                label: ''}

    this.received = null
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);

  }

  handleChange(event){
    this.setState({value: event.target.value})
  }

  handleSubmit(event){

    // const url = "http://localhost:5000/input/" + this.state.value
    event.preventDefault()
    const url = "/input"

    const ul = document.getElementById("ul-info")
    let resp = ""
    fetch(url, {method: "POST", body: JSON.stringify(this.state.value),
    headers: new Headers({
      "content-type": "application/json"
    })}
    ).then(function(response) {
    // if (response.status !== 200) {
    //   console.log(`Looks like there was a problem. Status code: ${response.status}`);
    //   return;
    // }
    resp = response
    response.json().then(function(data) {

      console.log(data);
      process_input(ul,data)

    //  this.state.label = data.label
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
  // if (response.status !== 200) {
  //   console.log(`Looks like there was a problem. Status code: ${response.status}`);
  //   return;
  // }
  resp = response
  response.json().then(function(data) {

    console.log(data);
    // process_input(ul,data)

  //  this.state.label = data.label
  });
})
.catch(function(error) {
  console.log("Fetch error: " + error);
});
  }

  render(){
    return(
      <form onSubmit = {this.handleSubmit}>
        <label>
          <textarea value ={this.state.value}
            onChange = {this.handleChange} draggable = "false" cols = "70" rows = "2"/>
            <input type = "submit" value = "=" />

        </label>

      </form>
    )
  }
}

export default CLI

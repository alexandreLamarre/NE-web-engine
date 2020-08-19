import React from "react"
import "./CLI.css"
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
    const url = "/input/" +this.state.value
    let resp = ""
    fetch(url
    ).then(function(response) {
    // if (response.status !== 200) {
    //   console.log(`Looks like there was a problem. Status code: ${response.status}`);
    //   return;
    // }
    resp = response
    response.json().then(function(data) {

      console.log(data);

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
            <p>
            {this.state.label}
            {this.state.interpreted}
            </p>
        </label>

      </form>
    )
  }
}

export default CLI

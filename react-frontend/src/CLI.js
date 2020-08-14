import React from "react"

class CLI extends React.Component{
  constructor(props){
    super(props)
    this.state = {value: ''}

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event){
    this.setState({value: event.target.value})
  }

  handleSubmit(event){
    alert("Command submitted: " + this.state.value )
    event.preventDefault();
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

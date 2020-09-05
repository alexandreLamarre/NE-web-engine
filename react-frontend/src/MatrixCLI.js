import React from "react"
import Matrix from "./Matrix"
import ReactDOM from 'react-dom';
import "./MatrixCLI.css"
class MatrixCLI extends React.Component{
  constructor(props){
    super(props);
    this.state = {
      matrix_array: []
    }

    this.onClickAdd = this.onClickAdd.bind(this);
    this.onClickRemove = this.onClickRemove.bind(this);
    this.getValues = this.getValues.bind(this);
  }

  onClickAdd(){
    var new_values = [[0,0],[0,0]];
    var matrix = ReactDOM.render(React.createElement(Matrix, {
      columns: new_values
    }),document.getElementById("matrices"));
  }

  onClickRemove(){
    ReactDOM.unmountComponentAtNode(document.getElementById("matrices"));
  }
  getValues(){

  }

  render(){
    return <div id = "MatrixCLI">
              <textarea />
              <div id="matrices"></div>
              <button onClick = {this.onClickAdd}>
              Add Matrix
              </button>
              <button onClick = {this.onClickRemove}>
              Remove Matrix
              </button>
              <button onClick = {this.getValues}>
              Get matrix
              </button>
            </div>
  }
}

export default MatrixCLI;

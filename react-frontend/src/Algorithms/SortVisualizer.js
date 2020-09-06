import React from "react";
import "./SortVisualizer.css";
import {insertionSort} from "./insertionSort";
import {startQuickSort} from "./quickSort";
import {startMergeSort} from "./mergeSort";

class SortVisualizer extends React.Component{
  constructor(props){
    super(props);
    this.state = {
      array: [],
      containerWidth: 0,
      containerHeight: 0,
      barWidth: 1,
      comparisons: 0,
      arrayAccesses: 0,
    }
  }

  componentDidMount(){
    this.resetArray();
  }

  setBarWidth(value){
    // const val = Math.abs(value - 11);
    // this.hello(val);
    // this.resetArray();
  }

  getInsertionSorted(){
    const sortedArray = insertionSort(this.state.array);
    console.log(sortedArray);
    this.setState({array: sortedArray})

  }

  getQuickSorted(){
    const sortedArray = startQuickSort(this.state.array);
    console.log(sortedArray);
    this.setState({array:sortedArray});
  }

  getMergeSorted(){
    const sortedArray = startMergeSort(this.state.array);
    console.log(sortedArray);
    this.setState({array:sortedArray});
  }
  resetArray(){
    const array = [];
    const w = Math.floor(window.innerWidth *0.45);
    const h = Math.floor(window.innerHeight* 0.60);
    // console.log(w)
    // console.log(h)
    console.log("number of array elements")
    console.log(w/(this.state.barWidth+1))
    for(let i = 0; i < w/(this.state.barWidth+1); i++){
      array.push(randomIntFromIntervals(5,h));
    }
    // let el = document.getElementById("array-bar");
    // if(el){
    //   el.width = `${this.state.barWidth}px`;
    // }
    this.setState({array:array, containerWidth: w, containerHeight: h});

  }

  render(){
    const array = this.state.array;
    let barWidth = this.state.barWidth;
    const containerWidth = this.state.containerWidth*1.5;

    return<div className ="sort">
      <div className = "array-container">{array.map((value, idX) => (
        <div
        className = "array-bar"
        key = {idX}
        style = {{
          backgroundColor: 'green',
          height: `${value}px`,
          width: `${barWidth}px`
        }}></div>
      ))}
      <div className = "sliders">
        <input type = "range" min = "1" max = "10" default = "1" className = "slider"
        name = "arraysize"
        onInput = {(event)=> this.setBarWidth(event.target.value)}/>
        <label for="arraysize"> ArraySize </label>
      </div>
      </div>
      <div className = "buttons" style = {{maxWidth: `${containerWidth}px`}}>
      <button onClick = {()=> this.getInsertionSorted()} className ="b">
      Insertion Sort
      </button>
      <button className ="b" onClick = {()=> this.getQuickSorted()}>
      Quick Sort
      </button>
      <button className ="b" onClick = {()=>this.getMergeSorted()}>
      Merge Sort
      </button>
      <button className ="b">
      Bubble Sort
      </button>
      <button className ="b">
      Tim Sort
      </button>
      <button className ="b">
      Intro Sort
      </button>
      <button className ="b">
      Radix Sort
      </button>
      <button onClick = {() => this.resetArray()} className ="b">
      Reset Array
      </button>
      </div>
    </div >
  }
}

function randomIntFromIntervals(minValue, maxValue){
  return Math.floor(Math.random()*(maxValue-minValue+1) + minValue);
}

export default SortVisualizer;
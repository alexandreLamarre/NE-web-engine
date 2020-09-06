import React from "react";
import "./SortVisualizer.css";
import {insertionSort} from "./insertionSort";
import {startQuickSort} from "./quickSort";
import {startMergeSort} from "./mergeSort";
import {bubbleSort} from "./bubbleSort";
import {radixSort} from "./radixSort";
import {heapSort} from "./heapSort";
import {gravitySort} from "./gravitySort"

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

  animateSort(animationArray){
    const animations = animationArray;
    for(let i = 0; i < animations.length; i++){
      const arrayBars = document.getElementsByClassName("array-bar");
      if(animations[i].swap){
        //swap two elements;
        const [v1,v2] = animations[i].values;
        const array = this.state.array;
        const x = array[v1];
        const y = array[v2];
        const that = this
        swapArrayState(array,v1,v2,x,y, that);
        // setTimeout(() =>{
        //   array[v1] = y;
        //   array[v2] = x;
        //   this.setState({array:array});
        // }, i * 2)
      }
      if(animations[i].select){
        // const values = animations[i].values;
        // const array = this.state.array;
        // const arrayBars = document.getElementsByClassName('array-bar')
        // setTimeout(() => {
        //   for(let k = 0; k< values.length; k++){
        //     arrayBars[values[k]].color = "red";
        //   }
        // })

      }
    }
  }

  getInsertionSorted(){
    const sortedArray = insertionSort(this.state.array);
    console.log(sortedArray);
    this.setState({array: sortedArray})

  }

  getQuickSorted(){
    const {array, animationArray} = startQuickSort(this.state.array);
    console.log(animationArray);
    console.log(animationArray)
    console.log(array);
    // this.animateSort(animationArray)
    this.setState({array:array});
  }

  getMergeSorted(){
    const sortedArray = startMergeSort(this.state.array);
    console.log(sortedArray);
    this.setState({array:sortedArray});
  }

  getBubbleSorted(){
    const sortedArray = bubbleSort(this.state.array);
    console.log(sortedArray);
    this.setState({array:sortedArray})
  }

  getRadixSorted(){
    const sortedArray = radixSort(this.state.array);
    console.log(sortedArray);
    this.setState({array:sortedArray});
  }

  getHeapSorted(){
    const sortedArray = heapSort(this.state.array);
    console.log(sortedArray);
    this.setState({array:sortedArray});
  }

  getGravitySorted(){
    const sortedArray = gravitySort(this.state.array);
    console.log(sortedArray);
    this.setState({array: sortedArray});
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
      <button className ="b" onClick = {() => this.getBubbleSorted()}>
      Bubble Sort
      </button>
      <button className ="b">
      Tim Sort
      </button>
      <button className ="b">
      Intro Sort
      </button>
      <button className ="b" onClick = {() => this.getRadixSorted()}>
      Radix Sort
      </button>
      <button onClick = {() => this.resetArray()} className ="b">
      Reset Array
      </button>
      <button onClick = {() => this.getHeapSorted()} className = "b">
      Heap Sort
      </button>
      <button className = "b" onClick = {() => this.getGravitySorted()}>
      Gravity Sort
      </button>
      </div>
    </div >
  }
}

function randomIntFromIntervals(minValue, maxValue){
  return Math.floor(Math.random()*(maxValue-minValue+1) + minValue);
}

function sleep(ms){
  return new Promise(resolve => setTimeout(resolve,ms));
}

async function swapArrayState(array,v1,v2,x,y,that){
    sleep(10)
    array[v1] = y;
    array[v2] = x;
    that.setState({array:array});
}

export default SortVisualizer;

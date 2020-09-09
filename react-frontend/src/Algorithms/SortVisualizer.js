import React from "react";
import "./SortVisualizer.css";
import {insertionSort} from "./insertionSort";
import {startQuickSort} from "./quickSort";
import {startMergeSort} from "./mergeSort";
import {bubbleSort} from "./bubbleSort";
import {radixSort} from "./radixSort";
import {heapSort} from "./heapSort";
import {gravitySort} from "./gravitySort"
import {timSort} from "./timSort";
import {introSort} from "./introSort";

async function waitForSetState(v,that){
  await that.setState({barWidth: v});
  that.resetArray();
}

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
      running: false,
      sorted: false,
      width: 0,
      height: 0,
    }
    this.canvas = React.createRef();
  }

  componentDidMount(){
    const w = window.innerWidth * 0.9;
    const h = window.innerHeight * 0.55;
    this.canvas.current.width = w;
    this.canvas.current.height = h;
    this.setState({width: w, height: h});
    this.resetArray();
  }

  setBarWidth(value){
    const val = Math.abs(value - 11);
    console.log(val);
    waitForSetState(val, this);
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
  animateMergeSort(animations){
    for(var i =0; i < animations.length; i++){
      console.log("animating")
      const arrayBars = document.getElementsByClassName("array-bar");
      if(i%3 !==2){
        const [barOne, barTwo] = animations[i];
        const barOneStyle = arrayBars[barOne].style;
        const barTwoStyle = arrayBars[barTwo].style;
        console.log(barOneStyle)
        const color = i%3 === 0? "red":"green"
        console.log(color)
        setTimeout(()=>{
          barOneStyle.backgroundColor = color;
          barTwoStyle.backgroundColor = color;
        }, i * 5);
      } else{

      }
    }
  }

  animateInsertionSort(animations){
    for(let i = 0; i < animations.length; i ++){
      const arrayBars = document.getElementsByClassName("array-bar");
      if(i%3 !==2){
        const [barOne] = animations[i];
        const barOneStyle = arrayBars[barOne].style;
        const color = i%3 === 0? "red": "green";
        setTimeout(()=>{
          barOneStyle.backgroundColor = color;
        }, i* 1)
      }
      else{
        const [barOne,barTwo] = animations[i];
        const array = this.state.array;
        setTimeout(() => {
          const temp = array[barOne];
          array[barOne] = array[barTwo];
          array[barTwo] = temp;
          this.setState({array:array});
        }, i * 1)
      }

    }
  }


  getInsertionSorted(){
    const [sortedArray, animations] = insertionSort(this.state.array);
    console.log(sortedArray);
    console.log(animations);
    // this.animateInsertionSort(animations);
    this.setState({array: sortedArray, sorted: true})

  }

  getQuickSorted(){
    const {array, animationArray} = startQuickSort(this.state.array);
    console.log(animationArray);
    console.log(animationArray)
    console.log(array);
    // this.animateSort(animationArray)
    this.setState({array:array, sorted: true});
  }

  getMergeSorted(){
    const [new_array, animations] = startMergeSort(this.state.array);
    console.log("sorted array");
    console.log(new_array);
    console.log("animations")
    console.log(animations);
    // this.animateMergeSort(animations);
    this.setState({array:new_array, sorted: true});
  }

  getBubbleSorted(){
    const sortedArray = bubbleSort(this.state.array);
    console.log(sortedArray);
    this.setState({array:sortedArray, sorted: true})
  }

  getRadixSorted(){
    const sortedArray = radixSort(this.state.array);
    console.log(sortedArray);
    this.setState({array:sortedArray, sorted: true});
  }

  getHeapSorted(){
    const sortedArray = heapSort(this.state.array);
    console.log(sortedArray);
    this.setState({array:sortedArray, sorted: true});
  }

  getGravitySorted(){
    const sortedArray = gravitySort(this.state.array);
    console.log(sortedArray);
    this.setState({array: sortedArray, sorted: true});
  }

  getTimSorted(){
    const sortedArray = timSort(this.state.array);
    console.log(sortedArray);
    this.setState({array: sortedArray, sorted: true});
  }

  getIntroSorted(){
    const sortedArray = introSort(this.state.array);
    console.log(sortedArray);
    this.setState({array: sortedArray, sorted: true});
  }

  resetArray(){
    console.log("resetting")
    const array = [];
    // console.log(w)
    // console.log(h)
    const ctx = this.canvas.current.getContext("2d");
    ctx.clearRect(0,0, this.canvas.current.width, this.canvas.current.height);

    for(let i = 0; i < Math.floor(this.canvas.current.width/(1+this.state.barWidth))+1; i++){
      array.push(randomIntFromIntervals(5, this.canvas.current.height));
    }
    const margin = 1;
    for(let j = 0; j < Math.floor(this.canvas.current.width/(1+this.state.barWidth))+1; j ++){
      ctx.beginPath()
      ctx.strokeStyle = "green";
      ctx.lineWidth = this.state.barWidth;
      ctx.moveTo(j+this.state.barWidth*j, this.canvas.current.height);
      ctx.lineTo(j+this.state.barWidth*j, this.canvas.current.height - array[j]);
      ctx.stroke();
    }
    ctx.stroke();

    this.setState({
      array: array,
      sorted: false,
    });
  }

  render(){
    const array = this.state.array;
    let barWidth = this.state.barWidth;
    const containerWidth = this.state.containerWidth*1.5;

    return<div className ="array-container">
      <canvas id = "sortCanvas" ref = {this.canvas} className = "sortCanvas"></canvas>
      <div className = "sliders">
        <input type = "range" min = "1" max = "10" default = "1" className = "slider"
        name = "arraysize"
        onInput = {(event)=> this.setBarWidth(event.target.value)} disabled = {this.state.running}/>
        <label> ArraySize {this.state.array.length}</label>
      </div>
      <div className = "buttons">
      <button onClick = {()=> this.getInsertionSorted()} className ="b"
      disabled = {this.state.running || this.state.sorted}>
      Insertion Sort
      </button>
      <button className ="b" onClick = {()=> this.getQuickSorted()}
      disabled = {this.state.running || this.state.sorted}>
      Quick Sort
      </button>
      <button className ="b" onClick = {()=>this.getMergeSorted()}
      disabled = {this.state.running || this.state.sorted}>
      Merge Sort
      </button>
      <button className ="b" onClick = {() => this.getBubbleSorted()}
      disabled = {this.state.running || this.state.sorted}>
      Bubble Sort
      </button>
      <button className ="b" onClick = {() => this.getTimSorted()}
      disabled = {this.state.running || this.state.sorted}>
      Tim Sort
      </button>
      <button className ="b" onClick = {() => this.getIntroSorted()}
      disabled = {this.state.running || this.state.sorted}>
      Intro Sort
      </button>
      <button className ="b" onClick = {() => this.getRadixSorted()}
      disabled = {this.state.running || this.state.sorted}>
      Radix Sort
      </button>
      <button onClick = {() => this.resetArray()} className ="b">
      Reset Array
      </button>
      <button onClick = {() => this.getHeapSorted()} className = "b"
      disabled = {this.state.running || this.state.sorted}>
      Heap Sort
      </button>
      <button className = "b" onClick = {() => this.getGravitySorted()}
      disabled = {this.state.running || this.state.sorted}>
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

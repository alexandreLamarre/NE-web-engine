export function heapSort(arr){
  let array = arr.slice(0);
  buildMaxHeap(array);
  let end = array.length -1;
  while(end > 0){
    let temp = array[end];
    array[end] = array[0];
    array[0] = temp;
    heapify(array,0,end);
    end--;
  }
  return array;
}

function buildMaxHeap(array){
  let currentIndex = Math.floor(array.length/2);
  while(currentIndex >=0){
    heapify(array,currentIndex, array.length)
    currentIndex --;
  }
}

function heapify(array,start,end){
  if(start>= Math.floor(end/2)){
    return;
  }
  let left = start*2+1;
  let right = start*2+2< end? start*2+2:null
  let swap;

  if(right){
    swap = array[left] > array[right]? left:right;
  }else{
    swap = left;
  }
  if(array[start] < array[swap]){
    let temp = array[swap];
    array[swap] = array[start];
    array[start] = temp;
    heapify(array,swap,end);
  }

}

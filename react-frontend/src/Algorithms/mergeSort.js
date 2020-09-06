export function startMergeSort(arr){
  const array = arr;
  const new_array = mergeSort(array, 0, array.length-1);
  return new_array;
}

function mergeSort(array){

  if(array.length <=1){
    return array;
  }
  const pivot = Math.floor(array.length/2);

  const left = array.slice(0,pivot);
  const right = array.slice(pivot);

  return merge(mergeSort(left), mergeSort(right));
}

function merge(left,right){
  let resultArray = [], leftIndex = 0, rightIndex = 0;

  while(leftIndex < left.length && rightIndex < right.length){
    if(left[leftIndex] < right[rightIndex]){
      resultArray.push(left[leftIndex]);
      leftIndex++;
    } else{
      resultArray.push(right[rightIndex]);
      rightIndex ++;
    }
  }

  return resultArray.concat(left.slice(leftIndex)).concat(right.slice(rightIndex));
}

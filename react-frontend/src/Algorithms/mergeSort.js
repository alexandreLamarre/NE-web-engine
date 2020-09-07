let animations_array = [];

export function startMergeSort(arr){
  const array = arr;
  animations_array = [];
  console.log(animations_array)
  const new_array = mergeSort(array, 0, array.length-1);
  return [new_array, animations_array];
}

function mergeSort(array){
  // console.log(animations_array)
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
    animations_array.push([leftIndex, rightIndex]);
    animations_array.push([leftIndex, rightIndex]);
    if(left[leftIndex] < right[rightIndex]){
      animations_array.push([leftIndex,left[leftIndex]])
      resultArray.push(left[leftIndex]);
      leftIndex++;
    } else{
      animations_array.push([rightIndex, rightIndex]);
      resultArray.push(right[rightIndex]);
      rightIndex ++;
    }
  }

  return resultArray.concat(left.slice(leftIndex)).concat(right.slice(rightIndex));
}

export function startQuickSort(arr){
  const array = arr;
  const animationArray = [];
  quickSort(array, 0, array.length-1, animationArray);
  return {array,animationArray};
}

function quickSort(array, p, r, animationArray){
    if(p < r){
      let q = partition(array, p, r, animationArray);
      quickSort(array,p,q-1, animationArray);
      quickSort(array,q+1,r, animationArray);
    }
}

function partition(array, p ,r, animationArray){
  let x = array[r];
  let i = p-1;
  for(var j = p; j< r; j++){
    if(array[j] <= x){
      i = i+1;
      const oldVal = array[i]
      const newVal = array[j]
      array[i] = newVal;
      array[j] = oldVal;
      animationArray.push(createSortFrame(false,true,[i,j]));
    }
  }
  const oldVal = array[i+1]
  const newVal = array[r]
  array[i+1] = newVal;
  array[r] = oldVal;
  animationArray.push(createSortFrame(false,true,[i+1,r]))
  return i+1;

}

function createSortFrame(selected,swapped,values){
  return {select: selected, swap: swapped, values: values};
}

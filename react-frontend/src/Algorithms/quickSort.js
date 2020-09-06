export function startQuickSort(arr){
  const array = arr;
  quickSort(array, 0, array.length-1);
  return array
}

function quickSort(array, p, r){
    if(p < r){
      let q = partition(array, p, r);
      quickSort(array,p,q-1);
      quickSort(array,q+1,r);
    }
}

function partition(array, p ,r ){
  let x = array[r];
  let i = p-1;
  for(var j = p; j< r; j++){
    if(array[j] <= x){
      i = i+1;
      const oldVal = array[i]
      const newVal = array[j]
      array[i] = newVal;
      array[j] = oldVal;
    }
  }
  const oldVal = array[i+1]
  const newVal = array[r]
  array[i+1] = newVal;
  array[r] = oldVal;
  return i+1;

}

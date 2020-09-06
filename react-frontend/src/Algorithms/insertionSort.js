export function insertionSort(arr){
  const array = arr;
  for(let j = 0; j < array.length; j++){
    let key = array[j];
    let i = j - 1;
    while(i>=0 && array[i]>key){
      array[i+1] = array[i];
      i = i - 1;
    }
    array[i+1] = key;
  }
  return array
}

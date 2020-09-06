export function bubbleSort(arr){
  const array = arr;
  for(let i = 0; i < array.length; i++){
    for(let j= 0; j< array.length; j++){
      if(array[j] > array[j+1]){
        const v1 = array[j];
        const v2 = array[j+1];
        array[j] = v2;
        array[j+1] = v1;
      }
    }
  }
  return array;
}

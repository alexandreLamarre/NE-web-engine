export function insertionSort(arr){
  const array = arr;
  const animations_array = [];
  for(let j = 0; j < array.length; j++){
    let key = array[j];
    let i = j - 1;
    while(i>=0 && array[i]>key){
      array[i+1] = array[i];
      animations_array.push([i+1]);
      animations_array.push([i+1]);
      animations_array.push([i+1,i]);
      i = i - 1;
    }
    animations_array.push([i+1]);
    animations_array.push([i+1]);
    animations_array.push([i+1,j]);
    array[i+1] = key;
  }
  return [array, animations_array];
}

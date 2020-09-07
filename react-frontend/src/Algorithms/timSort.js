const RUN = 32;

export function timSort(arr){
  let array = arr.slice();
  console.log(array == arr);
  for(var i = 0; i < array.length; i += RUN){
    insertionSort(array,i, Math.min((i+31), (array.length-1)));
    // console.log("insertionSort")
    // console.log(array)
  }
  // console.log("before runs")
  // console.log(array)
  for(var size = RUN; size < array.length; size *= 2){
    for(var left = 0; left < array.length; left+=2*size){
      var mid = left + size - 1;
      var right = Math.min((left+2*size -1), (array.length-1));
      // console.log("before merge");
      // console.log(array);
      merge(array,left,mid,right);
      // console.log("after merge");
      // console.log(array);
    }
  }
  return array;
}


function insertionSort(array, left, right){
  for(var i = left+1; i <= right; i ++){
    var temp = array[i];
    var j = i - 1;
    while(j>=left && array[j] > temp){
      array[j+1] = array[j];
      j--;
    }
    array[j+1] = temp;
  }
}

function merge(array, l, m, r){
  var len1 = m - l + 1, len2 = r-m;
  var left = [];
  var right = [];
  let arraycopy = array.slice();
  for(var i = 0; i < len1; i++){
    left.push(arraycopy[l+i]);
  }
  for(var j = 0; j< len2; j++){
    right.push(arraycopy[m+1+j]);
  }
  // console.log("left")
  // console.log(left)
  // console.log("right")
  // console.log(right)
  var i = 0;
  var j = 0;
  var k =0;

  while(i < len1 && j < len2){
    if(left[i] <= right[j]){
      array[k] = left[i];
      i ++;
    }
    else{
      array[k] = right[j];
      j++;
    }
    k++;
  }

  //copy any remaining elements of left if any
  while(i<len1){
    array[k] =left[i];
    k++;
    i++;
  }

  while(j<len2){
    array[k] = right[j];
    k++;
    j++;
  }
}

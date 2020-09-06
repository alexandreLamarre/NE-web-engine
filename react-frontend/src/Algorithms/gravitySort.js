export function gravitySort(arr){
  const array = arr;

  let max = array[0];

  for(var i = 1; i < array.length; i++){
    if(array[i] > max){
      max = array[i];
    }
  }
  let beads = [];
  for(var k =0; k< max*array.length; k++){
    beads.push(0);
  }
  console.log(beads)
  for(var i = 0; i < array.length; i++){
    for(var j = 0; j < array[i]; j ++){
      beads[i*max+j] = 1;
    }
  }

  for(var j = 0; j<max; j++){
    var sum = 0;
    for(var i = 0; i < array.length; i++){
      sum = sum + beads[i*max+j];
      beads[i*max+j] = 0;
    }

    for(var i = array.length - sum; i < array.length; i++){
      beads[i*max+j] = 1;
    }
  }

  for(var i = 0; i < array.length; i++){
    for(var j =0; j< max && beads[i*max+j]; j++){
    }
    array[i] = j;
  }
  return array;
}

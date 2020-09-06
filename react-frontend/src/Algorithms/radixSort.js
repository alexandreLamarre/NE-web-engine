export function radixSort(array){
  let arr = array;
  let maxLength = 3;

  for (let i = 0; i < maxLength; i++) {
    let buckets = Array.from({ length: 10 }, () => []);

    for (let j = 0; j < arr.length; j++) {
      let num = getNum(arr[j], i);

      if (num !== undefined) buckets[num].push(arr[j]);
    };
    arr = buckets.flat();
  };
  return arr;
}

function getNum(num, index){
  const strNum = String(num);
  let end = strNum.length -1;
  const foundNum = strNum[end-index];

  if(foundNum === undefined) return 0;
  else return foundNum;
}

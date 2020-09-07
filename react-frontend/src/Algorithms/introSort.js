const size_threshold = 16;

export function introSort(arr){
  const array = arr;
  introsort_loop(array, 0, array.length, 2 * floor_lg(array.length));
  return array
}
function introsort_loop (a, lo, hi, depth_limit) {
    while (hi-lo > size_threshold) {
        if (depth_limit === 0) {
            heapsort(a, lo, hi);
            return;
        }
        depth_limit=depth_limit-1;
        var p = partition(a, lo, hi, medianof3(a, lo, lo+((hi-lo)/2)+1, hi-1));
        introsort_loop(a, p, hi, depth_limit);
        hi = p;
    }
    insertionsort(a, lo, hi);
}

function partition(a, lo, hi, x) {
    var i=lo, j=hi;
    while (true) {
        while (a[i] < x) i++;
        j=j-1;
        while (x < a[j]) j=j-1;
        if (i >= j) return i;
        exchange(a,i,j);
        i++;
    }
}

function medianof3(a, lo, mid, hi) {
    if (a[mid] < a[lo]) {
        if (a[hi] < a[mid]) {
            return a[mid];
        } else {
            return (a[hi] < a[lo]) ? a[hi] : a[lo];
        }
    } else {
        if (a[hi] < a[mid]) {
            return (a[hi] < a[lo]) ? a[lo] : a[hi];
        } else {
            return a[mid];
        }
    }
}

/*
* Heapsort algorithm
*/
function heapsort(a, lo, hi) {
    var n = hi-lo, i;
    for (i= n / 2; i >= 1; i--) {
        downheap(a,i,n,lo);
    }
    for (i = n; i > 1; i--) {
        exchange(a,lo,lo+i-1);
        downheap(a,1,i-1,lo);
    }
}

function downheap(a, i, n, lo) {
    var d = a[lo+i-1];
    var child;
    while (i<=n/2) {
        child = 2*i;
        if (child < n && a[lo+child-1] < a[lo+child]) {
            child++;
        }
        if (d >= a[lo+child-1]) break;
        a[lo+i-1] = a[lo+child-1];
        i = child;
    }
    a[lo+i-1] = d;
}

/*
* Insertion sort algorithm
*/
function insertionsort(a, lo, hi) {
    var i,j;
    var t;
    for (i=lo; i < hi; i++) {
        j=i;
        t = a[i];
        while(j!=lo && t < a[j-1]) {
            a[j] = a[j-1];
            j--;
        }
        a[j] = t;
    }
}

/*
* Common methods for all algorithms
*/
function exchange(a, i, j) {
    var t=a[i];
    a[i]=a[j];
    a[j]=t;
}

function floor_lg(a) {
    return (Math.floor(Math.log(a)/Math.log(2))) << 0;
}
//   const array = arr;
//
//   let maxDepth = Math.floor(Math.log(array.length))*2;
//   introSort(array,maxDepth);
//   return array;
// }
//
// function introSort(array,start,end,maxDepth){
//   var n = end-start;
//   if(n<=1) return;
//   else if (maxDepth === 0){
//     heapSort(array)
//   }
//   else{
//     let p = partition(array, start,end)
//     introSort(array,0, p, maxDepth-1);
//     introSort(array,p+1, maxDepth -1);
//   }
// }
//
// function partition(array,low,high){
//   let pivot = array[Math.floor(((high+low)/2))];
//   let i = low;
//   let j = high;
//   while(true){
//     while(array[i] < pivot){
//         i ++;
//     }
//     j --;
//     while(array[j] > pivot){
//         j --;
//     }
//
//     if(i >= j){
//       return j;
//     }
//     const temp = array[i];
//     array[i] = array[j];
//     array[j] = temp;
//     i++;
//   }
// }
// // function partition(array,lo,hi){
// //   let x = array[r];
// //   while(true){
// //     while(a[i]<x){
// //       i++;
// //     }
// //     j--;
// //     while(x<A[j]){
// //       j -= 1;
// //     }
// //     if(i >=j){
// //       return i;
// //     }
// //    exchange a[i] and a[j]
// //     i++;
// //   }
// //
// // }
//
//
// // function partition(array, p ,r){
// //   let x = array[r];
// //   let i = p-1;
// //   for(var j = p; j< r; j++){
// //     if(array[j] <= x){
// //       i = i+1;
// //       const oldVal = array[i]
// //       const newVal = array[j]
// //       array[i] = newVal;
// //       array[j] = oldVal;
// //       // animationArray.push(createSortFrame(false,true,[i,j]));
// //     }
// //   }
// //   const oldVal = array[i+1]
// //   const newVal = array[r]
// //   array[i+1] = newVal;
// //   array[r] = oldVal;
// //   // animationArray.push(createSortFrame(false,true,[i+1,r]))
// //   return i+1;
// //
// // }
//
// function heapSort(array){
//   buildMaxHeap(array);
//   let end = array.length -1;
//   while(end > 0){
//     let temp = array[end];
//     array[end] = array[0];
//     array[0] = temp;
//     heapify(array,0,end);
//     end--;
//   }
// }
//
// function buildMaxHeap(array){
//   let currentIndex = Math.floor(array.length/2);
//   while(currentIndex >=0){
//     heapify(array,currentIndex, array.length)
//     currentIndex --;
//   }
// }
//
// function heapify(array,start,end){
//   if(start>= Math.floor(end/2)){
//     return;
//   }
//   let left = start*2+1;
//   let right = start*2+2< end? start*2+2:null
//   let swap;
//
//   if(right){
//     swap = array[left] > array[right]? left:right;
//   }else{
//     swap = left;
//   }
//   if(array[start] < array[swap]){
//     let temp = array[swap];
//     array[swap] = array[start];
//     array[start] = temp;
//     heapify(array,swap,end);
//   }
//
// }

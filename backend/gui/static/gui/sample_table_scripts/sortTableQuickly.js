function compareValues(value1, value2, comparePattern, direction = "forward") {
  const numericPattern = /(^\d+\.?\d+$)|(^\d+$)/;
  const datePattern = /^\d{2}-\d{2}-\d{4}$/;

  // keep empty values at the bottom of the table
  if ((value1 == "none" || value1 == "") && value2 != "none" && value2 != "") {
    return 1;
  } else if (value2 == "none" || value2 == "") {
    return -1;
  }

  let compare1, compare2;
  // handle different data types
  if (String(comparePattern) == String(numericPattern)) {
    compare1 = parseFloat(value1);
    compare2 = parseFloat(value2);
    return direction == "forward" ? compare1 - compare2 : compare2 - compare1;
  } else if (String(comparePattern) == String(datePattern)) {
    split1 = value1.split("-");
    split2 = value2.split("-");
    compare1 = new Date(split1[2], split1[1] - 1, split1[0]);
    compare2 = new Date(split2[2], split2[1] - 1, split2[0]);
  } else {
    compare1 = value1;
    compare2 = value2;
  }

  // eventually the comparison between the values
  if (compare1 > compare2) {
    return direction == "forward" ? 1 : -1;
  } else if (compare1 < compare2) {
    return direction == "forward" ? -1 : 1;
  } else {
    return 0;
  }
}

function compareRows(comparePattern, index, direction) {
  return function (row1, row2) {
    // extract values from html elements
    let value1 = row1
      .getElementsByTagName("TD")
      [index + 1].innerHTML.toLowerCase();
    let value2 = row2
      .getElementsByTagName("TD")
      [index + 1].innerHTML.toLowerCase();

    return compareValues(value1, value2, comparePattern, direction);
  };
}

function findOutDataType(array, index) {
  const numericPattern = /(^\d+\.?\d+$)|(^\d+$)/;
  const datePattern = /^\d{2}-\d{2}-\d{4}$/;
  let comparePattern;

  for (let i = 0; i < array.length; i++) {
    value = array[i]
      .getElementsByTagName("TD")
      [index + 1].innerHTML.toLowerCase();

    if (value != "None") {
      comparePattern =
        (numericPattern.test(value) && numericPattern) ||
        (datePattern.test(value) && datePattern);
      return comparePattern;
    }
  }
}

function sortTableFunctional(index, button) {
  let table, rows, direction, sortedRows, comparePattern;

  table = document.getElementById("sampleTable");
  rows = table.rows;

  arrayRows = Array.prototype.slice.call(rows).slice(1);

  comparePattern = findOutDataType(arrayRows, index);
  direction = button.value != "forward" ? "forward" : "reversed";
  button.value = direction;

  sortedRows = arrayRows.sort(compareRows(comparePattern, index, direction));

  let new_tbody = document.createElement("tbody");
  new_tbody.id = "data-rows";
  for (let i = 0; i < sortedRows.length; i++) {
    new_tbody.appendChild(sortedRows[i]);
  }

  let old_tbody = document.getElementById("data-rows");

  table.replaceChild(new_tbody, old_tbody);

  stripesAndCount();
}

// table.rows[1:] als initialer array
// function mergeSort(array, l, r) {
//   let m;
//   if (l == r) {
//     return array;
//   } else {
//     m = Math.floor((l + r) / 2);
//     let leftArray = mergeSort(arr, l, m);
//     let rightArray = mergeSort(arr, m + 1, r);
//     mergedArray = merge(leftArray, rightArray);
//     return mergedArray;
//   }
// }

// function merge(leftArray, rightArray) {
//   let mergedList;
//   while (leftArray.length != 0 && rightArray != 0) {
//     if(leftArray[])
//   }
// }

function sortTable(index, button) {
  let table, rows, switching, i, x, y, shouldSwitch;
  table = document.getElementById("sampleTable");
  switching = true;

  const numericPattern = /^\d+\.?\d+$/;
  const datePattern = /^\d{2}-\d{2}-\d{4}$/;
  let comparePattern;
  let patternSet = false;

  /* Make a loop that will continue until
      no switching has been done: */
  while (switching) {
    // Start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    /* Loop through all table rows (except the
        first, which contains table headers): */
    for (i = 1; i < rows.length - 1; i++) {
      // Start by saying there should be no switching:
      shouldSwitch = false;
      /* Get the two elements you want to compare,
          one from current row and one from the next: */
      x = rows[i].getElementsByTagName("TD")[index + 1];
      y = rows[i + 1].getElementsByTagName("TD")[index + 1];

      let xString = x.innerHTML.toLowerCase();
      let yString = y.innerHTML.toLowerCase();

      // ensuring that empty values are always on the bottom of the table
      if (
        (xString == "none" || xString == "") &&
        yString != "none" &&
        yString != ""
      ) {
        shouldSwitch = true;
        break;
      } else if (yString == "none" || yString == "") {
        continue;
      }

      if (!patternSet) {
        comparePattern =
          (numericPattern.test(xString) && numericPattern) ||
          (datePattern.test(xString) && datePattern);
        patternSet = true;
      }

      let compareX, compareY;

      if (comparePattern == numericPattern) {
        compareX = parseFloat(xString);
        compareY = parseFloat(yString);
      } else if (comparePattern == datePattern) {
        splitX = xString.split("-");
        splitY = yString.split("-");
        compareX = new Date(splitX[2], splitX[1] - 1, splitX[0]);
        compareY = new Date(splitY[2], splitY[1] - 1, splitY[0]);
      } else {
        compareX = xString;
        compareY = yString;
      }

      // if not sorted or reversed sort it forward
      if (button.value == "unsorted" || button.value == "reversed") {
        if (compareX > compareY) {
          shouldSwitch = true;
          break;
        }
      } else {
        if (compareX < compareY) {
          shouldSwitch = true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      /* If a switch has been marked, make the switch
          and mark that a switch has been done: */
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
    }
  }
  // stripe table
  var displayedRowNumber = 1;
  for (i = 0; i < rows.length; i++) {
    if (rows[i].style.display != "none") {
      if (displayedRowNumber % 2 == 0) {
        rows[i].style.background = "#d4daebf8";
      } else {
        rows[i].style.background = "#fff7f7";
      }
      displayedRowNumber += 1;
      // console.log(`displayedRowNumber ${displayedRowNumber}`);
    }
  }
  if (button.value == "unsorted" || button.value == "reversed") {
    button.value = "forward";
  } else {
    button.value = "reversed";
  }
}

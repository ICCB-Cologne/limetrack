function sortTable(index) {
  var table, rows, switching, i, x, y, shouldSwitch;
  table = document.getElementById("sampleTable");
  switching = true;
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
      // Check if the two rows should switch place:
      if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
        // If so, mark as a switch and break the loop:
        shouldSwitch = true;
        break;
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
}

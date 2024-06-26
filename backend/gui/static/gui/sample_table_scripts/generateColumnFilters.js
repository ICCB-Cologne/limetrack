function getColumnValues(id, index) {
  const headRow = document.getElementById("head-row");
  const allRows = document.getElementById("data-rows").children;
  const numberOfRows = allRows.length;

  // get all distinct values of the selected column
  let columnNumber = index + 1;
  const column = new Set();
  for (let i = 0; i < numberOfRows; i++) {
    var value = allRows[i].children[columnNumber].innerHTML;
    column.add(value);
  }

  var dropdownID = id.replace("button", "dropdown");
  const dropdown = document.getElementById(dropdownID);
  dropdown.innerHTML = "";

  // create and style sort button
  var sortPanel = document.createElement("li");
  var sortButton = document.createElement("button");
  sortButton.type = "button";
  sortButton.className = "btn btn-secondary ";
  sortButton.style.width = "100%";
  sortPanel.className = "dropdown-item";
  sortButton.innerHTML = "Sort";
  sortButton.addEventListener("click", function () {
    sortTable(index);
  });
  sortPanel.appendChild(sortButton);
  dropdown.appendChild(sortPanel);

  var line = document.createElement("hr");
  line.style.marginTop = "5px";
  line.style.marginBottom = 0;
  dropdown.appendChild(line);

  // create and append Select All Button
  var selectAll = document.createElement("label");
  selectAll.className = "dropdown-item";
  selectAll.style = "z-index:10";
  var selectAllInput = document.createElement("input");
  selectAllInput.type = "checkbox";
  selectAllInput.setAttribute("checked", true);
  selectAll.addEventListener("input", function () {
    selectAllColumnFilters(dropdownID);
  });
  selectAll.appendChild(selectAllInput);
  selectAll.innerHTML += " Select all";
  dropdown.appendChild(selectAll);

  // append all values as checkbox inputs to the dropdown
  for (let value of column) {
    var item = document.createElement("label");
    item.className = "dropdown-item";
    item.style = "z-index:10";
    var input = document.createElement("input");
    input.type = "checkbox";
    input.setAttribute("checked", true);
    item.addEventListener("input", function () {
      filterColumn(dropdownID);
    });
    item.appendChild(input);
    value = "  " + value;
    item.innerHTML += value;
    dropdown.appendChild(item);
  }
}

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

function filterColumn(id) {
  var input, filter, table, tr, td, tds, ths, i, txtValue, idx, column;

  var dropdownFilter = document.getElementById(id);
  var inputs = dropdownFilter.getElementsByTagName("input");
  var checkedInputs = [];

  // get all unchecked inputs of the column
  for (let input of inputs) {
    if (input.checked == false) {
      let value = input.parentNode.innerText || input.parentNode.textContent;
      checkedInputs.push(value.slice(1));
    }
  }

  var column = id.replace("dropdown for ", "");

  filter = checkedInputs;
  table = document.getElementById("sampleTable");
  tr = table.getElementsByTagName("tr");

  // get all column names
  ths = tr[0].getElementsByTagName("th");

  // find out indexes of columns
  for (i = 0; i < ths.length; i++) {
    if (ths[i].getAttribute("name") == column) {
      activeFilters.set(i, checkedInputs);
    }
  }
  var indexes = Array.from(activeFilters.keys());

  // Loop through all table rows, and hide those who can be found in the active filters map
  for (i = 1; i < tr.length; i++) {
    // check every column, that has active filters
    for (let idx of indexes) {
      td = tr[i].getElementsByTagName("td")[idx];
      if (td) {
        txtValue = td.textContent || td.innerText;
        if (activeFilters.get(idx).indexOf(txtValue) < 0) {
          tr[i].style.display = "";
          // if one filter does not match the row, hide it
        } else {
          tr[i].style.display = "none";
          break;
        }
      }
    }
  }
  // stripe table and count displayed rows
  var newRowNumber = 1;
  for (i = 1; i < tr.length; i++) {
    // console.log(tr[i].style.display);
    if (tr[i].style.display != "none") {
      if (newRowNumber % 2 == 0) {
        tr[i].style.background = "#fff7f7";
      } else {
        tr[i].style.background = "#d4daebf8";
      }
      newRowNumber += 1;
    }
  }
  numberSelected = document.getElementById("id-selected-samples");
  numberSelected.innerHTML = newRowNumber - 1;
}

function selectAllColumnFilters(dropdownID) {
  const dropdown = document.getElementById(dropdownID);
  console.log(dropdownID);
  const all_inputs = dropdown.getElementsByTagName("input");
  for (let i = 1; i < all_inputs.length; i++) {
    if (all_inputs[0].checked == false) {
      all_inputs[i].checked = true;
      all_inputs[i].click();
    } else {
      all_inputs[i].checked = false;
      all_inputs[i].click();
    }
  }
}

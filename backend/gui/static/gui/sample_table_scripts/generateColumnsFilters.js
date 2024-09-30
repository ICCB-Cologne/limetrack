function getColumnValues(id, index) {
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

  // append entity filters
  if (dropdownID == "dropdown for SATURN3 Sample Code") {
    addEntityFilters(dropdownID, " PDAC");
    addEntityFilters(dropdownID, " CRC");
    addEntityFilters(dropdownID, " BC");
  }

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

function addEntityFilters(dropdownID, entity) {
  var selectEntity = document.createElement("label");
  selectEntity.className = "dropdown-item";
  selectEntity.style = "z-index:10";
  var selectEntityInput = document.createElement("input");
  selectEntityInput.type = "checkbox";
  selectEntityInput.setAttribute("checked", true);
  selectEntity.addEventListener("input", function () {
    selectAllFiltersForEntity(entity, dropdownID);
  });

  selectEntity.appendChild(selectEntityInput);
  selectEntity.innerHTML += entity;
  const dropdown = document.getElementById(dropdownID);
  dropdown.appendChild(selectEntity);
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
  updateActiveFilters(id);
  filterTable();
}

function searchTable() {
  updateSearchFilter();
  filterTable();
}

function updateActiveFilters(id) {
  // get table and table rows
  table = document.getElementById("sampleTable");
  tr = table.getElementsByTagName("tr");

  // get all column names
  ths = tr[0].getElementsByTagName("th");

  var column = id.replace("dropdown for ", "");
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
  for (let i = 0; i < ths.length; i++) {
    if (ths[i].getAttribute("name") == column) {
      activeFilters.set(i, checkedInputs);
    }
  }
}

function updateSearchFilter() {
  var input, filter, table, tr, td, tds, ths, i, txtValue, idx;
  input = document.getElementById("tableSearchInput");
  column = document.getElementById("selectTableSearchColumn").value;
  filter = input.value.toUpperCase();
  table = document.getElementById("sampleTable");
  tr = table.getElementsByTagName("tr");

  // get all column names
  ths = tr[0].getElementsByTagName("th");
  // find out index of column
  for (i = 0; i < ths.length; i++) {
    if (ths[i].getAttribute("name") == column) {
      activeSearchFilter.set(i, filter);
    }
  }
}

function filterTable() {
  var searchFilter, table, tr, td, ths, i, txtValue, searchIndex;

  // get table and table rows
  table = document.getElementById("sampleTable");
  tr = table.getElementsByTagName("tr");

  // get all column names
  ths = tr[0].getElementsByTagName("th");

  // console.log(`activeFilters: ${activeFilters}`);
  // console.log(activeFilters);
  // console.log(`activeSearchFilter: ${activeSearchFilter}`);
  // console.log(activeSearchFilter);

  // indexes of columns to be filtered
  var indexes = Array.from(activeFilters.keys());
  activeSearchFilter.forEach(function (value, key) {
    indexes.indexOf(key) && indexes.push(key);
    searchIndex = key;
    searchFilter = value;
  });

  // console.log("indexes");
  // console.log(indexes);

  // Loop through all table rows, and hide those who can be found in the active filters map
  // and don't match the search filter
  for (i = 1; i < tr.length; i++) {
    // check every column, that has active column filters
    // console.log(`Row number ${i}`);
    for (let idx of indexes) {
      // console.log(`Check index ${idx}`);
      td = tr[i].getElementsByTagName("td")[idx];
      if (td) {
        txtValue = td.textContent || td.innerText;
        // console.log(`Text value:    ${txtValue}`);
        // console.log(`In active Filters?:    ${activeFilters.has(idx)}`);
        if (activeFilters.has(idx)) {
          if (activeFilters.get(idx).indexOf(txtValue) < 0) {
            // console.log("OK!");
            tr[i].style.display = "";
          } else {
            // console.log("Filtered out!");
            tr[i].style.display = "none";
            break;
          }
        }
        // filter searched column
        if (idx == searchIndex) {
          // console.log(`Search Filter: ${searchFilter}`);
          if (txtValue.toUpperCase().indexOf(searchFilter) > -1) {
            // console.log("OK!");
            tr[i].style.display = "";
          } else {
            // console.log("Filtered out!");
            tr[i].style.display = "none";
            break;
          }
        }
      }
    }
  }
  stripesAndCount();
}

function countPatients() {
  var filteredPatientNumber;
  var patientNumber;

  const allRows = document.getElementById("data-rows").children;
  const headRow = document.getElementById("head-row").children;

  var SAT3Index;
  for (let i = 0; i < headRow.length; i++) {
    var value = headRow[i].getAttribute("name");
    if (value == "SATURN3 Sample Code") {
      SAT3Index = i;
      break;
    }
  }
  let columnNumber = SAT3Index;
  const filteredPatients = new Set();
  const patients = new Set();
  for (let i = 0; i < allRows.length; i++) {
    let patientID = allRows[i].children[columnNumber].innerHTML.slice(4, 9);
    if (allRows[i].style.display != "none") {
      filteredPatients.add(patientID);
    }
    patients.add(patientID);
  }
  filteredPatientNumber = document.getElementById("id-filtered-patient-number");
  filteredPatientNumber.innerHTML = filteredPatients.size;
  patientNumber = document.getElementById("id-patient-number");
  patientNumber.innerHTML = patients.size;
}

function stripesAndCount() {
  var table, tr;

  table = document.getElementById("sampleTable");
  tr = table.getElementsByTagName("tr");
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
  countPatients();
}

const entityMap = new Map([
  [" PDAC", "S3P"],
  [" CRC", "S3C"],
  [" BC", "S3M"],
]);

function selectAllFiltersForEntity(entity, dropdownID) {
  const dropdown = document.getElementById(dropdownID);

  const all_inputs = dropdown.getElementsByTagName("input");
  const all_labels = dropdown.getElementsByTagName("label");
  var index;

  switch (entity) {
    case " PDAC":
      index = 1;
      break;
    case " CRC":
      index = 2;
      break;
    case " BC":
      index = 3;
      break;
  }

  for (let i = 1; i < all_labels.length; i++) {
    if (all_labels[i].innerText.slice(1, 4) == entityMap.get(entity)) {
      var input = all_labels[i].getElementsByTagName("input")[0];
      if (all_inputs[index].checked == false) {
        all_inputs[i].checked = false;
        // all_inputs[i].checked && all_inputs[i].click();
      } else {
        all_inputs[i].checked = true;
        // all_inputs[i].checked || all_inputs[i].click();
      }
    }
  }
  filterColumn(dropdownID);
}

function selectAllColumnFilters(dropdownID) {
  const dropdown = document.getElementById(dropdownID);
  const all_inputs = dropdown.getElementsByTagName("input");
  for (let i = 1; i < all_inputs.length; i++) {
    if (all_inputs[0].checked == false) {
      all_inputs[i].checked = false;
      // all_inputs[i].checked && all_inputs[i].click();
    } else {
      all_inputs[i].checked = true;
      // all_inputs[i].checked || all_inputs[i].click();
    }
  }
  filterColumn(dropdownID);
}

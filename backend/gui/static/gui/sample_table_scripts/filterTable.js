function filterColumn(id) {
  updateActiveFilters(id);
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
      let value =  input.parentNode.textContent || input.parentNode.innerText;
      checkedInputs.push(value.trim());
    }
  }
  for (let i = 0; i < ths.length; i++) {
    if (ths[i].getAttribute("name") == column) {
      activeFilters.set(i, checkedInputs);
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

  // indexes of columns to be filtered
  var indexes = Array.from(activeFilters.keys());
  activeSearchFilter.forEach(function (value, key) {
    indexes.indexOf(key) && indexes.push(key);
    searchIndex = key;
    searchFilter = value;
  });

  // Loop through all table rows, and hide those who can be found in the active filters map
  // and don't match the search filter
  for (i = 1; i < tr.length; i++) {
    // check every column, that has active column filters
    for (let idx of indexes) {
      td = tr[i].getElementsByTagName("td")[idx];
      if (td) {        
        txtValue = td.textContent || td.innerText;  
        if (txtValue !== "") {
          txtValue = txtValue.trim()
        }
        if (activeFilters.has(idx)) {
          if (activeFilters.get(idx).indexOf(txtValue) < 0) {
            tr[i].style.display = "";
          } else {
            tr[i].style.display = "none";
            break;
          }
        }
        // filter searched column
        if (idx == searchIndex) {
          if (txtValue.toUpperCase().indexOf(searchFilter) > -1) {
            tr[i].style.display = "";
          } else {
            tr[i].style.display = "none";
            break;
          }
        }
      }
    }
  }
  stripesAndCount();
}

function stripesAndCount() {
  var table, tr;

  table = document.getElementById("sampleTable");
  tr = table.getElementsByTagName("tr");
  // stripe table and count displayed rows
  var newRowNumber = 1;
  for (i = 1; i < tr.length; i++) {
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

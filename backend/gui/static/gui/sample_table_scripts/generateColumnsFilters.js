function getColumnValues(id, index) {
  const allRows = document.getElementById("data-rows").children;
  const numberOfRows = allRows.length;

  // get all distinct values of the selected column
  let columnNumber = index + 1;
  const columnSet = new Set();
  for (let i = 0; i < numberOfRows; i++) {
    var value = allRows[i].children[columnNumber].innerHTML;
    columnSet.add(value);
  }

  const column = [];
  columnSet.forEach((v) => column.push(v));
  column.sort(function (a, b) {
    return a.toLowerCase().localeCompare(b.toLowerCase());
  });

  var dropdownID = id.replace("button", "dropdown");
  const dropdown = document.getElementById(dropdownID);
  dropdown.innerHTML = "";

  // create and style sort button
  var sortPanel = document.createElement("li");
  var sortButton = document.createElement("button");
  sortButton.value = "unsorted";
  sortButton.type = "button";
  sortButton.className = "btn btn-secondary ";
  sortButton.style.width = "100%";
  sortPanel.className = "dropdown-item";
  sortButton.innerHTML = "Sort";
  sortButton.addEventListener("click", function () {
    sortTableFunctional(index, sortButton);
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

const entityMap = new Map([
  [" PDAC", "S3P"],
  [" CRC", "S3C"],
  [" BC", "S3M"],
]);

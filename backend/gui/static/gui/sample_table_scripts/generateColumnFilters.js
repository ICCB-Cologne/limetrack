function getColumnValues() {
  const headRow = document.getElementById("head-row");
  const allRows = document.getElementById("data-rows").children;
  const numberOfRows = allRows.length;

  let columnNumber = 2;
  const column = new Set();
  for (let i = 0; i < numberOfRows; i++) {
    var value = allRows[i].children[columnNumber].innerHTML;
    column.add(value);
  }

  console.log(column);
  const dropdown = document.getElementById("dropdown for Recruiting Site");
  dropdown.innerHTML = "";
  for (let value of column) {
    var item = document.createElement("li");
    item.className = "dropdown-item";
    var input = document.createElement("input");
    input.type = "checkbox";
    item.appendChild(input);
    value = "  " + value;
    item.innerHTML += value;
    dropdown.appendChild(item);
  }
}

function searchsTable() {
  // Declare variables
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
      idx = i;
    }
  }
  // Loop through all table rows, and hide those who don't match the search query
  var newRowNumber = 1;
  for (i = 1; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[idx];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
        // stripe table
        if (newRowNumber % 2 == 0) {
          tr[i].style.background = "#fff7f7";
        } else {
          tr[i].style.background = "#d4daebf8";
        }
        newRowNumber += 1;
      } else {
        tr[i].style.display = "none";
      }
    }
  }
  numberSelected = document.getElementById("id-selected-samples");
  numberSelected.innerHTML = newRowNumber - 1;
}

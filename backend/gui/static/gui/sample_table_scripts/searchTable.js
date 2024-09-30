function searchTable() {
  updateSearchFilter();
  filterTable();
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

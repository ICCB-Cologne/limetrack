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
  console.log("Filtered");
  console.log(filteredPatients.size);
  patientNumber = document.getElementById("id-patient-number");
  patientNumber.innerHTML = patients.size;
  console.log("All");
  console.log(patients.size);
}

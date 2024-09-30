// delete record with ID id
function deleteID(id, csrf) {
  const form = document.getElementById("id-form");

  // Clear existing inputs
  form.innerHTML = "";

  // Add CSRF token input
  const csrfTokenInput = document.createElement("input");
  csrfTokenInput.type = "hidden";
  csrfTokenInput.name = "csrfmiddlewaretoken";
  csrfTokenInput.value = csrf;
  form.appendChild(csrfTokenInput);

  // Add ID input
  const idInput = document.createElement("input");
  idInput.type = "hidden";
  idInput.name = "id";
  idInput.value = id;
  form.appendChild(idInput);

  const filterForm = document.getElementById("column-filter");
  var formData = new FormData(filterForm);
  const all_inputs = filterForm.getElementsByTagName("input");

  for (let i = 1; i < all_inputs.length; i++) {
    var name = all_inputs[i].name;
    if (formData.has(name)) {
      newInput = document.createElement("input");
      newInput.type = "hidden";
      newInput.name = name;
      newInput.value = "on";
      if (all_inputs[i].type == "text") {
        newInput.value = all_inputs[i].value;
      }

      form.appendChild(newInput);
    }
  }

  form.submit();
}

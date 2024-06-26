function submitForm(id) {
  const form = document.getElementById("id-form");

  // Clear existing inputs
  form.innerHTML = "";

  // Add CSRF token input
  const csrfTokenInput = document.createElement("input");
  csrfTokenInput.type = "hidden";
  csrfTokenInput.name = "csrfmiddlewaretoken";
  csrfTokenInput.value = "{{ csrf_token }}";
  form.appendChild(csrfTokenInput);

  // Add ID input
  const idInput = document.createElement("input");
  idInput.type = "hidden";
  idInput.name = "id";
  idInput.value = id;
  form.appendChild(idInput);

  // Submit the form
  form.submit();
}

// takes form data out of the filter dropdown and posts it as
// a new form to FilteredDownloadView
function downloadWithFilter() {
  const form = document.getElementById("column-filter");
  var formData = new FormData(form);

  const downloadForm = document.getElementById("filter-download");

  // Clear existing inputs
  downloadForm.innerHTML = "";

  // Add CSRF token input
  const csrfTokenInput = document.createElement("input");
  csrfTokenInput.type = "hidden";
  csrfTokenInput.name = "csrfmiddlewaretoken";
  csrfTokenInput.value = "{{ csrf_token }}";
  downloadForm.appendChild(csrfTokenInput);

  const all_inputs = form.getElementsByTagName("input");

  // append all input values to the download form
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

      downloadForm.appendChild(newInput);
    }
  }

  downloadForm.submit();
}

// Get the modal
var modal = document.getElementById("exampleModal");
var modalBody = document.getElementById("modalBody");

// Get the button that opens the modal
var btn = document.getElementById("modalButton");

btn.onclick = function () {
  modalBody.innerHTML = "";
  form = document.getElementById("start-of-form");
  formData = new FormData(form);
  // output as an object
  formDataObject = Object.fromEntries(formData);
  console.log(formDataObject);

  for (var pair of formData.entries()) {
    console.log(pair[1]);
    if (pair[0] != "csrfmiddlewaretoken") {
      const newDiv = document.createElement("div");
      newDiv.innerHTML = `<p> ${pair[0]} ---- ${pair[1]} </p>`;
      modalBody.appendChild(newDiv);
    }
  }
};

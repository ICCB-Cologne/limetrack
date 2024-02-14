// Get the modal
var modal = document.getElementById("exampleModal");
var modalBody = document.getElementById("modalBody");

// Get the button that opens the modal
var btn = document.getElementById("modalButton");

const exampleModal = document.getElementById("exampleModal");
if (exampleModal) {
  exampleModal.addEventListener("show.bs.modal", (event) => {
    form = document.getElementById("start-of-form");
    formData = new FormData(form);

    // Update the modal's content.
    modalBody.innerHTML = "";
    //TODO: Boolean Fields need to be displayed if they are set on 'off' = False
    for (var pair of formData.entries()) {
      if (pair[0] != "csrfmiddlewaretoken") {
        const newDiv = document.createElement("div");
        newDiv.innerHTML = `<p> ${pair[0]} ---- ${pair[1]} </p>`;
        modalBody.appendChild(newDiv);
      }
    }
    modalTitle.textContent = `New message to ${recipient}`;
    modalBodyInput.value = recipient;
  });
}

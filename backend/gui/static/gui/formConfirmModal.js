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

    labels = form.getElementsByTagName("label");
    const labelNames = [];
    for (let i = 0; i < labels.length; i++) {
      labelNames.push(labels[i].innerHTML.slice(0, -1));
    }
    // console.log(labelNames);

    // Update the modal's content.
    modalBody.innerHTML = "";
    //TODO: Boolean Fields need to be displayed if they are set on 'off' = False

    const tablediv = document.createElement("div");
    const table = document.createElement("table");
    table.className = "table table-light table-hover table-bordered";
    tablediv.appendChild(table);

    const thead = document.createElement("thead");
    const tbody = document.createElement("tbody");

    // const corresponding_organoid_value = document.getElementById(
    //   "id_corresponding_organoid"
    // ).checked;

    var sat3 = "";
    for (var pair of formData.entries()) {
      if (pair[0] != "csrfmiddlewaretoken") {
        if (pair[0].includes("saturn3_sample_code_")) {
          sat3 = sat3.concat(pair[1].toString());

          if (
            pair[0] != "saturn3_sample_code_3" &&
            pair[0] != "saturn3_sample_code_6" &&
            pair[0] != "saturn3_sample_code_7"
          ) {
            sat3 = sat3.concat("-");
          }

          if ("saturn3_sample_code_7" != pair[0]) {
            continue;
          }
          var name = "saturn3_sample_code";
          var value = sat3;
        } else {
          var name = pair[0];
          var value = pair[1];
        }

        row = document.createElement("tr");
        row.className = "";
        row.innerHTML = `
          <td class=""> ${name} </td>
          <td>${value}</td>`;
        tbody.appendChild(row);
      }
      modalBody.appendChild(tablediv);
    }
    table.appendChild(thead);
    table.appendChild(tbody);
  });
}

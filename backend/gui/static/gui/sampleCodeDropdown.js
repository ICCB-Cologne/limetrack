const entitiy = new Map([
  ["S3M", "M - Mamma"],
  ["S3C", "C - Colon"],
  ["S3P", "P - Pancreas"],
]);

const tissueType = new Map([
  ["B", "B - Normal blood"],
  ["T", "T - Tumorous tissue"],
  ["M", "M - Metastatis"],
  ["S", "S - Sphere/Organoid"],
  ["X", "X - Xenograft"],
  ["L", "L - Plasma"],
  ["N", "N - Normal/health tissue"],
  ["C", "C - 2D cultivated cells"],
  ["F", "F - Buffy Coat/PBMCs"],
  ["R", "R - Other"],
]);

const storageFormat = new Map([
  ["S", "S - Snap frozen"],
  ["V", "V - Viable frozen diss. Cells"],
  ["F", "F - Viable frozen tissue"],
  ["P", "P - FFPE"],
  ["Y", "Y - Formalin"],
]);

const analyteType = new Map([
  ["D", "D - DNA"],
  ["R", "R - RNA"],
  ["C", "C - Chip"],
  ["W", "W - DNA Libraries"],
  ["Y", "Y - RNA Libraries"],
  ["T", "T - ctDNA"],
  ["M", "M - depleted RNA"],
  ["L", "L - ATAC"],
  ["G", "G - scATAC"],
  ["H", "H - scRNA"],
  ["N", "N - None"],
]);

function fullName() {
  console.log(this.options);
  for (option of this.options) {
    console.log(option.textContent);
    switch (this.name) {
      case "saturn3_sample_code_0":
        option.textContent = entitiy.get(option.value);
        break;

      case "saturn3_sample_code_3":
        option.textContent = tissueType.get(option.value);
        break;

      case "saturn3_sample_code_5":
        option.textContent = storageFormat.get(option.value);
        break;

      case "saturn3_sample_code_6":
        option.textContent = analyteType.get(option.value);
        break;
    }
  }
}

function antiFullName() {
  console.log(this.options);
  for (option of this.options) {
    if (this.name == "saturn3_sample_code_0") {
      option.textContent = option.value[2];
    } else {
      option.textContent = option.value;
    }
  }
}

// Entity
document
  .getElementById("id_saturn3_sample_code_0")
  .addEventListener("focus", fullName);

document
  .getElementById("id_saturn3_sample_code_0")
  .addEventListener("blur", antiFullName);

// Tissue Type
document
  .getElementById("id_saturn3_sample_code_3")
  .addEventListener("focus", fullName);

document
  .getElementById("id_saturn3_sample_code_3")
  .addEventListener("blur", antiFullName);

// Storage format
document
  .getElementById("id_saturn3_sample_code_5")
  .addEventListener("focus", fullName);

document
  .getElementById("id_saturn3_sample_code_5")
  .addEventListener("blur", antiFullName);

// Analyte type
document
  .getElementById("id_saturn3_sample_code_6")
  .addEventListener("focus", fullName);

document
  .getElementById("id_saturn3_sample_code_6")
  .addEventListener("blur", antiFullName);

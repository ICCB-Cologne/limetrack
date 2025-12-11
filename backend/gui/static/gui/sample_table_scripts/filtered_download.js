function extract_keys(headers, exclude = []) {
  let keys = [];

  headers.querySelectorAll("th:not([hidden])").forEach((element) => {
    for (child of element.childNodes) {
      if (child.nodeType === Node.TEXT_NODE) {
        let name = child.textContent.trim();

        if (exclude.includes(name) === false) {
          keys.push(name);
          break;
        }
      }
    }
  });

  return keys;
}

function create_record(keys, row, date = []) {
  let record = {};

  row.querySelectorAll("td:not([hidden])").forEach((element, index) => {
    // if td elements are "filled" with an empty string then
    // they don't have childNodes. That's taken in account here.
    if (!element.hasChildNodes()) {
      record[keys[index]] = "";
    }
    for (child of element.childNodes) {
      if (child.nodeType === Node.TEXT_NODE) {
        let text = child.textContent.trim();
        if (text !== "" && text !== "None") {
          record[keys[index]] = text;
          break;
        } else if (keys[index] !== "Action") {
          record[keys[index]] = "";
          break;
        }
      }
    }
  });

  return record;
}

function table_to_json(tablename) {
  let json_buffer = [];

  let table = document.getElementById(tablename);
  let rows = table.querySelectorAll("tr:not([style*='display: none;'])");
  let keys = extract_keys(rows[0]);

  for (let i = 1; i < rows.length; i++) {
    let record = create_record(keys, rows[i]);
    json_buffer.push(record);
  }

  return JSON.stringify({samples: json_buffer});
}

function download(filename, type, text) {
  let mime_type = "text/csv;base64";

  if (type == "Excel") {
    mime_type = "application/vnd.ms-excel;base64";
  }

  let element = document.createElement("a");
  element.setAttribute("href", `data:${mime_type},${encodeURIComponent(text)}`);
  element.setAttribute("download", filename);
  element.style.display = "none";
  document.body.appendChild(element);
  element.click();
  document.body.removeChild(element);
}

function downloadWithFilter(type, data) {
  let data = table_to_json("sampleTable");

  let request = $.ajax({
    type: "POST",
    url: `/filtered_download/?type=${type}`,
    data: {
      csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0]
        .value,
      data: data,
    },
    dataType: "text",
    success: (data, status, xhr) => {
      let filename = xhr.getResponseHeader("filename");
      console.log(filename);
      console.log(xhr.responseText)
      download(filename, type, xhr.responseText);
    },
    error: (e) => console.log(e),
  });
}

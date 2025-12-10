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

function downloadNew(filename, type, blob) {
  let mime_type = "text/csv;base64";

  if (type == "Excel") {
    mime_type = "application/vnd.ms-excel;base64";
  }

  let element = document.createElement("a");
  element.setAttribute("href", `${window.URL.createObjectURL(blob)}`);
  element.setAttribute("download", filename);
  element.style.display = "none";
  document.body.appendChild(element);
  element.click();
  document.body.removeChild(element);
}



function downloadWithFilter(type) {
  let data = table_to_json("sampleTable")
  // const bigAssJson = {
  // userId: 123,
  // items: Array.from({ length: 720000 }).map((_, i) => ({
  //   id: i,
  //   value: `Item ${i}`,
  //   })),
  // }; 
  // let data = JSON.stringify(bigAssJson)

  let fetch_type = "1"

  switch (fetch_type){
    case "1":
      sendBigJson(data, type);
      break;
    case "2": 
      sendBigJson2(data, type);
      break;
    case "3":
      downloadWithFilterNew(type, data);
      break;
    case "4":
      downloadWithFilterOld(type, data);
      break;
  }


}

function downloadWithFilterNew(type, data) {
    console.log("NEW WAY")
  let request = $.ajax({
    type: "POST",
    url: `/filtered_download/?type=${type}`,
    beforeSend: (xhr) => {xhr.setRequestHeader("X-CSRFToken", document.getElementsByName("csrfmiddlewaretoken")[0].value);},
    data: data,
    dataType: "text",
    success: (data, status, xhr) => {
      console.log("SUCCESS is no LUCK!!!!");
      let filename = xhr.getResponseHeader("filename");
      console.log(filename);
      console.log(type);
      console.log(xhr.responseText);
      
      download(filename, type, xhr.responseText);
    },
    error: (e) => {
      console.log("ERROR is LUCK!!!!");
      console.log(e)},
  });
}

function downloadWithFilterOld(type, data) {
  // let data = table_to_json("sampleTable");

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

async function sendBigJson(data, type) {
    console.log("2")
    const bigPayload = data
    try {
      const response = await fetch(`/filtered_download/?type=${type}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": document.getElementsByName("csrfmiddlewaretoken")[0].value, // Django CSRF
        },
        body: bigPayload,
      });
      console.log("we here")

      if (!response.ok) {
        console.error("Server error:", response.status, await response.text());
        return;
      }
      // const data = await response.json();
      const filename = response.headers.get("filename")
      const text = await response.text()
      console.log(text)
      console.log(filename);
      // const blob = await response.blob()
      // console.log(text)
      console.log("Server replied:");
      download(filename, type, text)

    } catch (err) {
      console.error("Network error:", err);
    }
  }



  function sendBigJson2(data, type){
    console.log("1")
    var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance 
    var theUrl = `/filtered_download/?type=${type}`;
    xmlhttp.open("POST", theUrl, true);
    xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xmlhttp.setRequestHeader("X-CSRFToken", document.getElementsByName("csrfmiddlewaretoken")[0].value); // Django CSRF);
    xmlhttp.send(data);
    downloadNew
    }
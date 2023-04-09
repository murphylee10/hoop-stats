createDropdown(document.querySelector("#season"));
let buildButton = document.querySelector("#build");
buildButton.addEventListener("click", displayPrediction);

function generatePrediction(dict) {
    return new Promise((resolve, reject) => {
      fetch("/predict-player-result", {
        method: "POST",
        body: JSON.stringify(dict),
      })
        .then((response) => response.json())
        .then((data) => {
          resolve(data);
        })
        .catch((error) => {
          reject(error.message);
        });
    });
  }
  
function displayPrediction() {
  let dict = {};
  dict["p_name"] = document.querySelector("#p_name").value;
  dict["season"] = document.querySelector("#season").value;
  let cols = ["gp", "pts", "reb", "ast", "fg_pct", "fg3_pct", "ft_pct"];
  for (let i = 0; i < cols.length; ++i) {
    dict[cols[i]] = document.querySelector("#" + cols[i]).value;
  }
  generatePrediction(dict).then((response) => {
    let output = document.querySelector("#output");
    let pre_message = document.querySelector("p.message");
    let pre_table = document.querySelector("table");
    if (pre_table !== null) {
      pre_table.remove();
    }
    if (pre_message !== null) {
      pre_message.remove();
    }
    if (!response["OK"]) {
      let message = document.createElement("p");
      message.setAttribute("class", "message");
      message.append(response["message"]);
      output.append(message);
      return;
    }
    let stats = response["stats"];
    console.log(String(stats));
    let table = document.createElement("table");
    let headers = document.createElement("tr");
    for (let i = 0; i < cols.length; ++i) {
      let str_header = cols[i];
      let pos = str_header.search("_pct");
      if (pos !== -1) {
        str_header = str_header.slice(0, pos) + "%";
      }
      let header = document.createElement("th");
      header.append(str_header);
      headers.append(header);
    }
    table.append(headers);
    for (let i = 0; i < stats.length; ++i) {
      let row = document.createElement("tr");
      for (let j = 0; j < stats[i].length; ++j) {
        let cell = document.createElement("td");
        cell.append(stats[i][j]);
        row.append(cell);
      }
      table.append(row);
    }
    output.append(table);
  });
}
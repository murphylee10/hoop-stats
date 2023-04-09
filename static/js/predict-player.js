createDropdown(document.querySelector("#season"));
let buildButton = document.querySelector("#build");
buildButton.addEventListener("click", displayPrediction);

function generatePrediction(dict) {
  //sends a post request to app.py
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
  //dictionary with values from the html form
  let dict = {};
  dict["p_name"] = document.querySelector("#p_name").value;
  dict["season"] = document.querySelector("#season").value;
  let cols = ["gp", "pts", "reb", "ast", "fg_pct", "fg3_pct", "ft_pct"];
  for (let i = 0; i < cols.length; ++i) {
    dict[cols[i]] = document.querySelector("#" + cols[i]).value;
  }
  generatePrediction(dict).then((response) => {
    let output = document.querySelector("#output");
    // reset header
    let rem_header = document.querySelector('#pred-header h2');
    if (rem_header != null) {
      rem_header.remove()
    }
    let pred_header_div = document.querySelector('.pred-header')
    let new_header = document.createElement('h2')
    new_header.innerText = "Predicted Player Stats"
    pred_header_div.appendChild(new_header)
    //reset messages and table
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
    //the returned stats from app.py
    let stats = response["stats"];
    console.log(String(stats));
    //display the stats as a table
    let table = document.createElement("table");
    let headers = document.createElement("tr");
    let season_header = document.createElement("th");
    season_header.append("Season");
    headers.append(season_header);
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
      let season_cell = document.createElement("td");
      season_cell.append(
        String(Number(dict["season"]) + i - 1) +
          "-" +
          String(Number(dict["season"]) + i)
      );
      row.append(season_cell);
      for (let j = 0; j < stats[i].length; ++j) {
        let cell = document.createElement("td");
        cell.append(stats[i][j]);
        row.append(cell);
      }
      table.append(row);
    }
    output.append(table);

    // output = document.getElementById("output");

    // const header = document.createElement("h2");
    // header.textContent = "Predicted Season Stats";
    // output.appendChild(header);

    // table = document.createElement("table");
    // output.appendChild(table);

    // const headerRow = document.createElement("tr");
    // table.appendChild(headerRow);

    // [
    //   "Name",
    //   "Position",
    //   "Points",
    //   "Rebounds",
    //   "Assists",
    //   "Blocks",
    //   "Steals",
    // ].forEach((header) => {
    //   const th = document.createElement("th");
    //   th.textContent = header;
    //   headerRow.appendChild(th);
    // });

    // data.forEach((player) => {
    //   const row = document.createElement("tr");
    //   table.appendChild(row);
    //   Object.values(player).forEach((value) => {
    //     const td = document.createElement("td");
    //     td.textContent = value;
    //     row.appendChild(td);
    //   });
    // });
  });
}



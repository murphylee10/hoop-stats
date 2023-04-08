let compareBy = document.querySelector("#season");
compareBy.addEventListener("change", changeOptions);

let duelButton = document.querySelector("#duel");
duelButton.addEventListener("click", displayDuel);

function changeOptions() {

  if (compareBy.value === "custom") {
    
    let input = document.querySelector("#input");
    let seasons = document.createElement("div");
    
    seasons.setAttribute("id", "seasons");
    let season1 = document.createElement("select");
    season1.setAttribute("name", "season1");
    season1.setAttribute("id", "season1");
    createDropdown(season1);
    let season2 = document.createElement("select");
    season2.setAttribute("name", "season2");
    season2.setAttribute("id", "season2");
    createDropdown(season2);
    
    let head1 = document.createElement("h3");
    head1.append("Season (Player 1)");
    let head2 = document.createElement("h3");
    head2.append("Season (Player 2)");

    seasons.append(head1);
    seasons.append(season1);
    seasons.append(head2);
    seasons.append(season2);
    input.insertBefore(seasons, duelButton);

  } else {

    let seasons = document.querySelector("#seasons");
    if (seasons !== null) {
      seasons.remove();
    }
    
  }

}

function generateDuel(dict) {
  return new Promise((resolve, reject) => {
    fetch("/duel-result", {
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

function displayDuel() {
  let dict = {};
  dict["p1"] = document.querySelector("#p1").value;
  dict["p2"] = document.querySelector("#p2").value;
  let cols = ["gp", "pts", "reb", "ast", "fg_pct", "fg3_pct", "ft_pct"];
  for (let i = 0; i < cols.length; ++i) {
    dict[cols[i]] = document.querySelector("#" + cols[i]).checked;
  }
  dict["season"] = document.querySelector("#season").value;
  if (dict["season"] == "custom") {
    dict["season1"] = document.querySelector("#season1").value;
    dict["season2"] = document.querySelector("#season2").value;
  }
  generateDuel(dict).then((response) => {
    let output = document.querySelector("#output");
    let pre_message = document.querySelector("p.message");
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
    let pre_table = document.querySelector("table");
    if (pre_table !== null) {
      pre_table.remove();
    }
    let stats1 = response["stats1"];
    let stats2 = response["stats2"];
    console.log(String(stats1));
    console.log(String(stats2));
    let table = document.createElement("table");
    let headers = document.createElement("tr");
    for (let i = 0; i < cols.length; ++i) {
      if (!dict[cols[i]]) {
        continue;
      }
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
    let row1 = document.createElement("tr");
    let row2 = document.createElement("tr");
    for (let i = 0, j = 0; i < cols.length; ++i) {
      if (!dict[cols[i]]) {
        continue;
      }
      let cell = document.createElement("td");
      cell.append(stats1[j]);
      row1.append(cell);
      ++j;
    }
    for (let i = 0, j = 0; i < cols.length; ++i) {
      if (!dict[cols[i]]) {
        continue;
      }
      let cell = document.createElement("td");
      cell.append(stats2[j]);
      row2.append(cell);
      ++j;
    }
    table.append(row1);
    table.append(row2);
    output.append(table);
  });
}
let compareBy = document.querySelector("#season");
compareBy.addEventListener("change", changeOptions);

let duelButton = document.querySelector("#duel");
duelButton.addEventListener("click", displayDuel);

function changeOptions() {
  //add dropdowns for custom season choices
  if (compareBy.value === "custom") {
    // let input = document.querySelector("#input");
    let season_div = document.querySelector('.season');

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
    // input.insertBefore(seasons, duelButton);
    season_div.insertBefore(seasons, duelButton);
  } else {
    let seasons = document.querySelector("#seasons");
    if (seasons !== null) {
      seasons.remove();
    }
  }
}

function generateDuel(dict) {
  //send a post request to app.py
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
  //dictionary with values from the HTML form
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
    //reset messages and table
    let output = document.querySelector("#output");
    let pre_message = document.querySelector("p.message");
    let pre_table = document.querySelector("table");
    let pre_winner = document.querySelector("#winner");
    if (pre_table !== null) {
      pre_table.remove();
    }
    if (pre_message !== null) {
      pre_message.remove();
    }
    if (pre_winner !== null) {
      pre_winner.remove();
    }
    if (!response["OK"]) {
      let message = document.createElement("p");
      message.setAttribute("class", "message");
      message.append(response["message"]);
      output.append(message);
      return;
    }
    //the returned stats from app.py
    let stats1 = response["stats1"];
    let stats2 = response["stats2"];
    console.log(String(stats1));
    console.log(String(stats2));
    //display the stats as a table
    let table = document.createElement("table");
    let headers = document.createElement("tr");
    let name_header = document.createElement("th");
    name_header.append("Player");
    headers.append(name_header);
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
    row1.append(stats1[stats1.length - 1]);
    row2.append(stats2[stats2.length - 1]);
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
    let cnt1 = 0, cnt2 = 0;
    for (let i = 0; i < stats1.length - 1; ++i) {
      if (stats1[i] > stats2[i]) {
        ++cnt1;
      } else {
        ++cnt2;
      }
    }
    let winner = document.createElement("h3");
    winner.setAttribute("id", "winner");
    winner.append("Winner: ");
    if (cnt1 > cnt2) {
      winner.append(stats1[stats1.length - 1]);
    } else {
      winner.append(stats2[stats2.length - 1]);
    }
    let surround = document.querySelector('.surround');
    surround.append(winner);
    //put the stats into a dictionary
    let p1_dict = {}
    let p2_dict = {}
    for (let i = 0, j = 0; i < cols.length; ++i) {
      if (!dict[cols[i]]) {
        continue;
      }
      p1_dict[cols[i]] = stats1[j];
      ++j;
    }
    p1_dict["name"] = stats1[stats1.length - 1];
    for (let i = 0, j = 0; i < cols.length; ++i) {
      if (!dict[cols[i]]) {
        continue;
      }
      p2_dict[cols[i]] = stats2[j];
      ++j;
    }
    p2_dict["name"] = stats2[stats2.length - 1];
    if (cnt1 > cnt2) {
      p1_dict["winner"] = true;
      p2_dict["winner"] = false;
    } else {
      p1_dict["winner"] = false;
      p2_dict["winner"] = true;
    }
    console.log(p1_dict);
    console.log(p2_dict);
  });
}
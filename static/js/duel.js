let compareBy = document.querySelector("#year");
compareBy.addEventListener("change", changeOptions);

function changeOptions() {
  if (compareBy.value === "custom") {

    let query = document.querySelector("#duel-form");
    let duelButton = document.querySelector("#duel");
    let extra = document.createElement("div");
    
    extra.setAttribute("id", "extra");
    let season1 = document.createElement("select");
    season1.setAttribute("id", "season1");
    createDropdown(season1);
    let season2 = document.createElement("select");
    season2.setAttribute("id", "season2");
    createDropdown(season2);
    
    let head1 = document.createElement("h3");
    head1.append("Season (Player 1)");
    let head2 = document.createElement("h3");
    head2.append("Season (Player 2)");

    extra.append(head1);
    extra.append(season1);
    extra.append(head2);
    extra.append(season2);
    query.insertBefore(extra, duelButton);

  } else {

    let extra = document.querySelector("#extra");
    if (extra !== null) {
      extra.remove();
    }
    
  }
}

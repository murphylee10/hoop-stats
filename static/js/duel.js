let compareBy = document.querySelector("#year");
compareBy.addEventListener("change", changeOptions);
function changeOptions() {
    if (compareBy.value === "custom") {
        let query = document.querySelector("#QUERY");
        let duelButton = document.querySelector("#duel");
        let extra = document.createElement("div");
        extra.setAttribute("id", "extra");
        let year1 = document.createElement("input");
        year1.setAttribute("type", "text");
        year1.setAttribute("id", "year-1");
        year1.setAttribute("placeholder", "Year (Player 1)");
        let year2 = document.createElement("input");
        year2.setAttribute("type", "text");
        year2.setAttribute("id", "year-2");
        year2.setAttribute("placeholder", "Year (Player 2)");
        extra.append(year1);
        extra.append(year2);
        query.insertBefore(extra, duelButton);
    } else {
        let extra = document.querySelector("#extra");
        if (extra !== null) {
            extra.remove();
        }
    }
}
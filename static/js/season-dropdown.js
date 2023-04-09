function createDropdown(dropdown) {
    //adds the season options to dropdown
    let current_date = new Date();
    let current_year = current_date.getFullYear();
    for (let year = 1980; year <= current_year; ++year) {
        let season = document.createElement("option");
        season.append(String(year - 1) + "-" + String(year));
        season.setAttribute("value", String(year));
        dropdown.append(season);
    }
}
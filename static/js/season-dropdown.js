function createDropdown(dropdown) {
    let current_date = new Date();
    let current_year = current_date.getFullYear();
    for (let year = 1977; year <= current_year; ++year) {
        let season = document.createElement("option");
        season.append(String(year - 1) + "-" + String(year));
        season.setAttribute("value", String(year));
        dropdown.append(season);
    }
}
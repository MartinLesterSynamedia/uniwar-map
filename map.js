function createMap(width, height) {
    var html = ""
    for (y = 0; y < height; y++) {
        html = html + '<div class="map_row">';
        for (x = 0; x < width; x++) {
            html = html + '<div class="map_cell"></div>';
        }
        html = html + '</div>';
    }

    $("#map_area").append(html);
}
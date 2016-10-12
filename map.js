var terrain_lookup = {
    " " : "",
    "_" : "terrain01.png",
    "B" : "terrain02.png",
    "F" : "terrain03.png",
    "M" : "terrain04.png",
    "S" : "terrain05.png",
    "D" : "terrain06.png",
    "w" : "terrain07.png",
    "P" : "terrain08.png",
    "+" : "terrain09.png",
};

function createMap( map_name ) {
    var map_url = "./map/" + map_name;

    $.ajax({
        url : map_url,
        type: "GET",

        success: function(data, textStatus, jqXHR)
        {
            var xml = jqXHR.responseText;
            var xmlDoc = $.parseXML( xml );
            var $xml = $( xmlDoc );

            var title = $xml.find( "title" ).text();
            var width = $xml.find( "width" ).text();
            var height = $xml.find( "height" ).text();
            var tile_set = $xml.find( "tile_set" ).text().toLowerCase();

            // Create a blank map of the correct size
            var html = "";
            for (y = 0; y < height; y++) {
                html = html + '<div class="map_row">';
                for (x = 0; x < width; x++) {
                    html = html + '<div class="map_cell" id="cell_' + x + '_' + y + '"></div>';
                }
                html = html + '</div>';
            }

            $("#map_area").append(html);
            $(".map_row:odd").addClass("map_row_odd");

            // Put the correct images into each of the backgrounds
            var $map_data = $xml.find( "map_data" );
            for (row = 0; row < height; row++) {
                var row_id = "row";
                if (row<10) {
                    row_id = row_id + "0";
                }
                row_id = row_id + row;
                var row_data = $xml.find( row_id ).text();
                var x = 0;

                row_data.split(", ").forEach(function(tile) {
                    // Strip the single quotes
                    tile = tile.substring(1, tile.length-1);
                    var terrain = terrain_lookup[tile];
                    if (terrain != "") {
                        var cell = "#cell_" + row + "_" + x;
                        $(cell).css("background", "url(/assets/tiles80/" + tile_set + "/" + terrain)
                    }
                    x = x + 1;
                });


            }
        },

        error: function (jqXHR, textStatus, errorThrown)
        {
            $("#debug").append("failed: " + errorThrown);
        }
    });
}

//    background:      url("assets/tiles80/terrain0001.png");

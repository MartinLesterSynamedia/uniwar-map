var tile_size = 80;

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

function debug( message ) {
    $("#debug").append( message + "<br/>" );
}

function createMap( map_name ) {
    var map_url = "../xml/" + map_name;

    $("#title").html( "Loading " + map_name );

    $.ajax({
        url : map_url,
        type: "GET",

        success: function(data, textStatus, jqXHR)
        {
            var xml = jqXHR.responseText;
            var xmlDoc = $.parseXML( xml );
            var $xml = $( xmlDoc );

            var title = $xml.find( "title" ).text();
            $("#title").html( title );

            var width = $xml.find( "width" ).text();
            var height = $xml.find( "height" ).text();

            drawEmptyMap( width, height );
            loadTerrain( height, $xml );

            removeBlankRows();
            removeBlankCols();
        },

        error: function (jqXHR, textStatus, errorThrown)
        {
            debug( "failed: " + errorThrown );
        }
    });
}

function drawEmptyMap( width, height ) {
    // Create a blank map of the correct size
    var html = "";
    for (y = 0; y < height; y++) {
        html = html + '<div class="map_row" id="row_' + y + '">';
        for (x = 0; x < width; x++) {
            html = html + '<div class="map_cell" id="cell_' + x + '_' + y + '">';
            html = html + '</div>';
        }
        html = html + '</div>';
    }

    $("#map_area").append(html);
    $(".map_row:odd").addClass("map_row_odd");
}

function loadTerrain( rows, $xml ) {
    // Put the correct images into each of the backgrounds
    var tile_set = $xml.find( "tile_set" ).text().toLowerCase();
    var $map_data = $xml.find( "map_data" );

    for (row = 0; row < rows; row++) {
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
            if ($.trim(tile) != "") {
                var terrain = terrain_lookup[tile];
                var cellid = "#cell_" + x + "_" + row;
                var $cell = $( cellid );
                $cell.css("background-image", "url(/assets/tiles80/" + tile_set + "/" + terrain);
                $cell.prop('title', cellid + '\ntile = ' + tile + '\nterrain = ' + terrain );
            }
            x = x + 1;
        });
    }
}

/* Remove empty rows and columns starting from the edges.
   Means we don't remove empty rows/columns from the middle as that would change the map */
function removeBlankRows() {
    // Starting at the top find all empty rows till we get to a row with a tile and remove them
    $(".map_row").each( checkCells );

    // Starting at the bottom find all empty rows till we get to a row with a tile and remove them
    $($(".map_row").get().reverse()).each( checkCells );
}

function checkCells( i, element ) {
    $this = $(element);
    var done = false;
    $this.children().each( function() {
        if (hasTerrain( this )) {
            done = true;
            return false;
        }
    });
    if (done) {
        return false;
    }
    $this.remove();
}

function hasTerrain( element ) {
     return $(element).css("background-image") != "none";
}

function removeBlankCols() {
    // Starting at the left find all empty rows till we get to a row with a tile and remove them
    var done = false;
    while (!done) {
        $(".map_cell:first-child").each( function() {
            if ( hasTerrain( this ) ) {
                done = true;
                return false;
            }
        });
        if (!done) {
            $(".map_cell:first-child").remove();
        }
    }

    // Starting at the right find all empty rows till we get to a row with a tile and remove them
    done = false;
    while (!done) {
        $(".map_cell:last-child").each( function() {
            if ( hasTerrain( this ) ) {
                done = true;
                return false;
            }
        });
        if (!done) {
            $(".map_cell:last-child").remove();
        }
    }
}

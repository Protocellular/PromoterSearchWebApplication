// Javascript search functionality
//  Executes Search via an AJAX call. Also provides live filterable result
//  functionality.

function runSearch( term ) {
    // hide and clear the previous results, if any
    $('#promoter_results').hide();
    $('#filters').hide();

    // transforms all the form parameters into a string to send to server
    var frmStr = $('#main_search').serialize();

    $.ajax({
        url: './search_promoters.cgi',
        dataType: 'json',
        data: frmStr,
        success: function(data, textStatus, jqXHR) {
            processJSON(data);
        },
        error: function(jqXHR, textStatus, errorThrown){
            alert("Failed to perform promoter search! textStatus: (" + textStatus +
                  ") and errorThrown: (" + errorThrown + ")");
        }
    });

    // obtains search filters based on properties of search query results
    $.ajax({
        url: "./get_search_filters.cgi",
        dataType: 'json',
        data: frmStr,
        success: function(data, textStatus, jqXHR) {
            getFilters(data);
        },
        error: function(jqXHR, textStatus, errorThrown){
            alert("Failed to perform filter search! textStatus: (" + textStatus +
                  ") and errorThrown: (" + errorThrown + ")");
        }
    });
}

// Processes a passed JSON structure with promoter data and displays it to results
function processJSON( data ) {
    // set the span that lists the number of results
    $('#match_count').text( data.match_count );

    // this will be used to keep track of row identifiers
    var next_row_num = 1;

    // iterate over each match and add a row to the result div for each
    $.each( data.matches, function(i, item) {
        var this_row_id = 'result_row_' + next_row_num++;

        $("#results").append( "<li class='resultitem' data-chassis='" + item.chassis + "' data-pol='"  + item.polymerase +
         "' data-dir='" + item.direction + "' data-reg='" + item.regulation_type + "' data-group='" + item.design_group +
         "' data-designer='" + item.designer + "' data-rating='" + item.rating + "' data-usage='" + item.times_used + "'>" +
         "<a href='http://parts.igem.org/Part:" + encodeURIComponent(item.bba_id) + "'>" +
           item.bba_id + " - " + item.name +
        "</a><br>Chassis: " + item.chassis + "<br>Polymerase: " + item.polymerase +
        "<br>Direction: " + item.direction + "<br>Regulation Type: " + item.regulation_type +
        "<br>Design Group: " + item.design_group + "<br>Designer: " + item.designer +
        "<br>Rating: " + item.rating + "<br>Times Used: " + item.times_used +
        "<br><a href='#' data-seq='"+item.sequence+"' class='sequence'>Sequence</a>" +

        "<br><br></div>")
    });

    //Shows the result section and filter sidebar that was previously hidden
    $('#promoter_results').show();
    $('#filters').show();
}

function getFilters(data) {
    $.each( data.pols.slice(1), function(i, item) {
        $("#polymerase").append( "<label for='polinfo'><input type='checkbox' class='filterlabel filterlabelpol' data-pol='" +
        item.label +  "'/>" + item.label  + "   (" + item.count +  ")"  +  "</label><br>" )
    });

    $.each( data.regulation.slice(1), function(i, item) {
        $("#regulation").append( "<label for='reginfo'><input type='checkbox' class='filterlabel filterlabelreg' data-reg='" +
        item.label + "'>" + item.label  + "   (" + item.count + ")"  +  "</label><br>" )
    });

    $.each( data.direction.slice(1), function(i, item) {
        $("#direction").append( "<label for='dirinfo'><input type='checkbox' class='filterlabel filterlabeldir'  data-dir='" +
        item.label + "'>" + item.label  + "   (" + item.count + ")"  +  "</label><br>" )
    });

    $.each( data.chassis.slice(1), function(i, item) {
        $("#chassis").append( "<label for='cha'><input type='checkbox' class='filterlabel filterlabelcha'  data-chassis='" + item.label + "' value='" + item.label + "'>" +
        item.label  + "   (" + item.count + ")"  +  "</label><br>" )
    });

    $.each( data.rating.slice(1), function(i, item) {
        $("#rating").append( "<label for='rat'><input type='checkbox' class='filterlabel filterlabelrat' data-rating='" + item.label + "' value='" + item.label + "'>" +
        item.label  + "   (" + item.count + ")"  +  "</label><br>" )
    });

    $.each( data.times_used.slice(1), function(i, item) {
        $("#uses").append( "<label for='use'><input type='checkbox' class='filterlabel filterlabeluse' data-usage='" + item.label + "' value='" + item.label + "'>" +
        item.label  + "   (" + item.count + ")"  +  "</label><br>" )
    });

    $.each( data.design_group.slice(1), function(i, item) {
        $("#group").append( "<label for='group'><input type='checkbox' class='filterlabel filterlabelgroup'  data-group='" + item.label + "' value='" + item.label + "'>" +
        item.label  + "   (" + item.count + ")"  +  "</label><br>" )
    });

    $.each( data.designer.slice(1), function(i, item) {
        $("#designer").append( "<label for='design'><input type='checkbox' class='filterlabel filterlabeldesign' data-designer='" + item.label + "' value='" + item.label + "'>" +
        item.label  + "   (" + item.count + ")"  +  "</label><br>" )
    });
}

$(document).ready( function() {
    $('#submit').click( function() {
        runSearch();
        return false;  // prevents 'normal' form submission
    });
    $("#reset").click(function(){
    $("#results").show();
    $( "input:checkbox:checked" ).prop( "checked", false );
});

// filter search results with checkboxes in sidebar
$( document ).on("click", '.filterlabel', function() {

    var arr = ['pol', 'reg', 'dir', 'chassis', 'rating', 'usage', 'group', 'designer'];

    for (var i = 0; i < arr.length; i++) {
        var name = arr[i];
        var attr = $(this).data(name);
        if (attr) {
            break
        }
    }
    //console.log(name, attr)
    if ($(this).prop('checked')) {
        $('li.resultitem:not(.hidden)[data-'+name+'="'+attr+'"]').addClass('keep')
        $('li.resultitem:not(.keep)').addClass('hidden').hide()
        $('.keep').removeClass('keep')
    }
    else {
        if ($('input.filterlabel:checked').length === 0) {
            $('li.resultitem').show().removeClass('hidden');
        } else {
            var checked = $('input:checked').click()
            checked.click()
        }
    }
    var count = $('li.resultitem:visible').length;

    // update span with new match count
    $('#match_count').text( count );
});

// opens a pop-up containing sequence data upon click
$( document ).on('click', '.sequence', function() {
    alert($(this).data('seq'))
})

});

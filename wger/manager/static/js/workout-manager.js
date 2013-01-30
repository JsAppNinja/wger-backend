/*
 * Own functions
 *
 */


function get_current_language()
{
    /* Returns a short name, like 'en' or 'de' */
    return $('#current-language').data('currentLanguage');
}

/*
 * Define an own widget, which is basically an autocompleter that groups
 * results by category
 */
$.widget( "custom.catcomplete", $.ui.autocomplete, {
        _renderMenu: function( ul, items ) {
            var that = this,
                currentCategory = "";
            $.each( items, function( index, item ) {
                if ( item.category != currentCategory ) {
                    ul.append( "<li class='ui-autocomplete-category'>" + item.category + "</li>" );
                    currentCategory = item.category;
                }
                that._renderItemData( ul, item );
            });
        }
    });


/*
 * Setup JQuery sortables to make the sets sortable
 */
function setup_sortable()
{
    // Hide the edit options for the set, this is done with the in-place editing
    $(".set-options").hide();

    $(".workout-table tbody").sortable({
        handle: '.dragndrop-handle',
        revert: true,
        update : function (event, ui) {
                // Monkey around the HTML, till we find the IDs of the set and the day
                var day_element = ui.item.parent().parent().find('tr').first().attr('id'); //day-xy
                var day_id = day_element.match(/\d+/);

                // returns something in the form "set-1,set-2,set-3,"
                var order = $( this ).sortable('toArray');

                //$("#ajax-info").show();
                //$("#ajax-info").addClass('success');
                $.get('/' + get_current_language() + "/workout/api/edit-set" + "?do=set_order&day_id=" + day_id + "&order=" + order)


                // TODO: it seems to be necessary to call the view two times before it returns
                //       current data.
                $.get('/' + get_current_language() + "/workout/day/view/" + day_id);
                $("#div-day-" + day_id).load('/' + get_current_language() + "/workout/day/view/" + day_id);
        }

    })

    // Allow the settings within an exercise to be sortable
    $(".settings-list").sortable({
        placeholder: 'sortable-settings',
        revert: true,
        tolerance: 'pointer',
        helper: function(event, ui) {
            //return ui;
            return $('<div class="sortable-settings-drag">' + ui.html() + '</div>');
        },
        update : function (event, ui) {
            // returns something in the form "setting-1,setting-2,setting-3,"
            var order = $( this ).sortable('toArray');

            // Load the day-ID
            var day_element = ui.item.parents('table').find('tr').attr('id'); //day-xy
            var day_id = day_element.match(/\d+/);

            //$("#ajax-info").show();
            //$("#ajax-info").addClass('success');
            $("#ajax-info").load('/' + get_current_language() + "/workout/api/edit-settting?do=set_order&order=" + order);

            // TODO: it seems to be necessary to call the view two times before it returns
            //       current data.
            $.get('/' + get_current_language() + "/workout/day/view/" + day_id);
            $("#div-day-" + day_id).load('/' + get_current_language() + "/workout/day/view/" + day_id);
        }
    });
}


/*
 * Setup JQuery calls to edit the sets
 */
function setup_ajax_set_edit()
{
    // Unbind all other click events so we don't do this more than once
    $(".ajax-set-edit").off();

    $(".ajax-set-edit").click(function(e) {
        e.preventDefault();

        var set_id = $(this).parents('tr').attr('id').match(/\d+/);
        var exercise_id = $(this).parents('.ajax-set-edit-target').attr('id').match(/\d+/);

        load_edit_set($(this).parents('.ajax-set-edit-target'), set_id, exercise_id)
    });
}

function load_edit_set(element, set_id, exercise_id)
{
    $(element).load('/' + get_current_language() + "/workout/api/edit-set?do=edit_set&set=" + set_id + "&exercise=" + exercise_id);
}

function setup_inplace_editing()
{
    $(".ajax-form-cancel").each(function(index, element) {


        var exercise_id = $(this).parents('.ajax-set-edit-target').attr('id').match(/\d+/);
        var day_id = $(this).parents('table').attr('id').match(/\d+/);
        var set_id = $(this).parents('tr').attr('id').match(/\d+/);

        // Editing of set
        $(element).click(function(e) {
            e.preventDefault();
            $("#div-day-" + day_id).load('/' + get_current_language() + "/workout/day/view/" + day_id);
        })

        // Send the Form
        $('.ajax-form-set-edit').submit(function(e) {
          e.preventDefault();

          url = '/' + get_current_language() + "/workout/api/edit-set?do=edit_set&set=" + set_id + "&exercise=" + exercise_id
          form_data = $(this).serialize();
          $.post( url, form_data);

          $("#div-day-" + day_id).load('/' + get_current_language() + "/workout/day/view/" + day_id);
        });

        // Init the autocompleter
        $(".ajax-form-exercise-list").catcomplete({
                source: '/' + get_current_language() + "/exercise/search/",
                minLength: 2,
                select: function(event, ui) {

                    // After clicking on a result set the value of the hidden field
                    $('#set-' + set_id + '-exercercise-id-hidden').val(ui.item.id);
                }
            });
    });
}

/*
 *
 * Functions related to the user's preferences
 *
 */
function toggle_comments()
{
    $("#exercise-comments-toggle").click(function(e) {
        e.preventDefault();


        if ( showComment == 0 )
        {
            $('.exercise-comments').show();
            showComment = 1;
        }
        else if ( showComment == 1 )
        {
            $('.exercise-comments').hide();
            showComment = 0;
        }

        $("#ajax-info").load('/' + get_current_language() + "/workout/api/user-preferences?do=set_show-comments&show=" + showComment);
    });
}

function set_english_ingredients()
{
    $("#ajax-english-ingredients").click(function(e) {
        e.preventDefault();


        if ( useEnglishIngredients == 0 )
        {
            $('#english-ingredients-status').attr("src", '/' + get_current_language() + "/static/images/icons/status-on.svg");
            useEnglishIngredients = 1;
        }
        else if ( useEnglishIngredients == 1 )
        {
             $('#english-ingredients-status').attr("src", '/' + get_current_language() + "/static/images/icons/status-off.svg");
             useEnglishIngredients = 0;
        }

        $("#ajax-info").load('/' + get_current_language() + "/workout/api/user-preferences?do=set_english-ingredients&show=" + useEnglishIngredients);
    });
}


/*
 * Init calls for tinyMCE editor
 */
function init_tinymce() {

    // Only try to init it on pages that loaded its JS file (so they probably need it)
    if (typeof tinyMCE != 'undefined')
    {
        tinyMCE.init({
            // General options
            mode : "textareas",
            theme : "simple",
            width : "100%",
            height : "200",
            entity_encoding : "raw"
        });
   }
}


/*
 * Open a modal dialog for form editing
 */
function form_modal_dialog()
{
    // Initialise a modal dialog
    $("#ajax-info").dialog({
                autoOpen: false,
                width: 600,
                modal: true,
                position: 'top'
    });

    // Unbind all other click events so we don't do this more than once
    $(".modal-dialog").off();

    // Load the edit dialog when the user clicks on an edit link
    $(".modal-dialog").click(function(e) {
        e.preventDefault();
        var targetUrl = $(this).attr("href");

        // Show a loader while we fetch the real page
        $("#ajax-info").html('<div style="text-align:center;">'+
                                '<img src="/static/images/loader.svg" ' +
                                     'width="48" ' +
                                     'height="48"> ' +
                             '</div>');
        $("#ajax-info").dialog({title: 'Loading...'});
        $("#ajax-info").dialog("open");

        $("#ajax-info").load(targetUrl + " .ym-form", function(responseText, textStatus) {
            // Call other custom initialisation functions
            // (e.g. if the form as an autocompleter, it has to be initialised again)
            if (typeof custom_modal_init != "undefined")
            {
                custom_modal_init();
            }

            // Set the new title
            $("#ajax-info").dialog({title: $(responseText).find("#page-title").html()});

            // If there is a form in the modal dialog (there usually is) prevent the submit
            // button from submitting it and do it here with an AJAX request. If there
            // are errors (there is an element with the class 'ym-error' in the result)
            // reload the content back into the dialog so the user can correct the entries.
            // If there isn't assume all was saved correctly and load that result into the
            // page's main DIV (#main-content). All this must be done like this because there
            // doesn't seem to be any reliable and easy way to detect redirects with AJAX.
            if ($(responseText).find(".ym-form").length > 0)
            {
                modal_dialog_form_edit();
            }
        });
    });
}


function modal_dialog_form_edit()
{
    form = $("#ajax-info").find(".ym-form");
    submit = $(form).find("#form-save");

    submit.click(function(e) {
        e.preventDefault();
        form_action = form.attr('action');
        form_data = form.serialize();

        // Unbind all click elements, so the form doesn't get submitted twice
        // if the user clicks 2 times on the button (while there is already a request
        // happening in the background)
        submit.off();

        // Show a loader while we fetch the real page
        $("#ajax-info .ym-form").html('<div style="text-align:center;">'+
                                '<img src="/static/images/loader.svg" ' +
                                     'width="48" ' +
                                     'height="48"> ' +
                             '</div>');
        $("#ajax-info").dialog({title: 'Processing...'}); // TODO: translate this


        // OK, we did the POST, what do we do with the result?
        $.post(form_action, form_data, function(data) {

            if($(data).find('.ym-form .ym-error').length > 0)
            {
                // we must do the same with the new form as before, binding the click-event,
                // checking for errors etc, so it calls itself here again.

                $("#ajax-info .ym-form").html($(data).find('.ym-form').html());
                $("#ajax-info").dialog({title: $(data).find("#main-content h2").html()});

                modal_dialog_form_edit();
            }
            else
            {
                $("#ajax-info").dialog("close");

                // If there  was a redirect we must change the URL of the browser. Otherwise
                // a reload would not change the adress bar, but the content would.
                // Since it is not possible to get this URL from the AJAX request, we read it out
                // from a hidden HTML DIV in the document...
                current_url = $(data).find("#current-url").data('currentUrl');
                if(document.URL.indexOf(current_url))
                {
                    history.pushState({}, "", current_url);
                }

                // Note: loading the new page like this executes all its JS code
                $('body').html(data);
            }

            // Call other custom initialisation functions
            // (e.g. if the form as an autocompleter, it has to be initialised again)
            if (typeof custom_modal_init != "undefined")
            {
                custom_modal_init();
            }

            if (typeof custom_page_init != "undefined")
            {
                custom_page_init();
            }


        });
    });

}



function init_ingredient_autocompleter()
{
    // Init the autocompleter
    $("#id_ingredient_searchfield").autocomplete({
        source: '/' + get_current_language() + "/nutrition/ingredient/search/",
        minLength: 2,
        select: function(event, ui) {

            // After clicking on a result set the value of the hidden field
            $('#id_ingredient').val(ui.item.id);
        }
    });
}


/*
 * Returns a random hex string. This is useful, e.g. to add a unique ID to generated
 * HTML elements
 */
function hex_random()
{
    return Math.floor(
        Math.random() * 0x10000 /* 65536 */
    ).toString(16);
}


/*
 * Template-like function that adds form elements to the ajax exercise selection
 * in the edit set page
 */
function add_exercise(exercise)
{
    var result_div = '<div id="DIV-ID" class="ajax-exercise-select"> \
<a href="#"> \
<img src="/static/images/icons/status-off.svg" \
     width="14" \
     height="14" \
     alt="Delete"> \
</a> EXERCISE \
<input type="hidden" name="exercises" value="EXCERCISE-ID"> \
</div>';

    // Replace the values into the 'template'
    result_div = result_div.replace('DIV-ID', hex_random());
    result_div = result_div.replace('EXERCISE', exercise.value);
    result_div = result_div.replace('EXCERCISE-ID', exercise.id);

    $(result_div).prependTo("#exercise-search-log");
    $("#exercise-search-log").scrollTop(0);
}

function init_edit_set()
{
    // Initialise the autocompleter (our widget, defined above)
    $("#exercise-search").catcomplete({
            source: '/' + get_current_language() + "/exercise/search/",
            minLength: 2,
            select: function(event, ui) {

                // Add the exercise to the list
                add_exercise(ui.item);

                // Remove the result div (also contains the hidden form element) when the user
                // clicks on the delete link
                $(".ajax-exercise-select a").click(function(e) {
                    e.preventDefault();
                    $(this).parent('div').remove();
                });

                // Reset the autocompleter
                $(this).val("");
                return false;
            }
        });

    // Remove the result div again
    // TODO: it seems it's necessary to have this twice, see if there's a better
    //       way to handle it
    $(".ajax-exercise-select a").click(function(e) {
        e.preventDefault();
        $(this).parent('div').remove();
    });
}

function init_weight_datepicker()
{
    $( "#id_creation_date" ).datepicker();
}

function init_weight_log_datepicker()
{
    $( "#id_date" ).datepicker();
}


/*
 *
 * D3js functions
 *
 */
// Simple helper function that simply returns the y component of an entry
function y_value(d) { return d.y; }

function getDate(d) {
    return new Date(d);
}

function weight_chart(data)
{
    // Return if there is no data to process
    if(data == '')
    {
        return;
    }

    var minDate = getDate(data[0].x),
        maxDate = getDate(data[data.length-1].x);

    var margin = {top: 10, right: 10, bottom: 150, left: 40},
        margin2 = {top: 290, right: 10, bottom: 50, left: 40},
        width = 600 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;
        height2 = 390 - margin2.top - margin2.bottom;

    var x = d3.time.scale()
        .domain([minDate, maxDate])
        .range([0, width]);
    var x2 = d3.time.scale()
        .domain([minDate, maxDate])
        .range([0, width]);

    var min_y_value = d3.min(data, y_value) - 1;
    var max_y_value = d3.max(data, y_value) + 1;


    var y = d3.scale.linear()
        .domain([min_y_value, max_y_value])
        .range([height, 0]);
    var y2 = d3.scale.linear()
        .domain([min_y_value, max_y_value])
        .range([height2, 0]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .ticks(6)
        .orient("bottom");

    var xAxis2 = d3.svg.axis()
        .scale(x2)
        .ticks(6)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");

    var brush = d3.svg.brush()
        .x(x2)
        .on("brush", brush);

    var line = d3.svg.line()
        .x(function(d) { return x(getDate(d.x)); })
        .y(function(d) { return y(d.y); })
        .interpolate('cardinal');

    var line2 = d3.svg.line()
        .x(function(d) { return x2(getDate(d.x)); })
        .y(function(d) { return y2(d.y); })
        .interpolate('cardinal');

    var area = d3.svg.area()
        .x(line.x())
        .y1(line.y())
        .y0(y(min_y_value))
        .interpolate('cardinal');

    var area2 = d3.svg.area()
        .x(line2.x())
        .y1(line2.y())
        .y0(y2(min_y_value))
        .interpolate('cardinal');

    // Reset the content of weight_diagram, otherwise if there is a filter
    // a new SVG will be appended to it
    $("#weight_diagram").html("");

    var svg = d3.select("#weight_diagram").append("svg")
        .datum(data)
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom);

    svg.append("defs").append("clipPath")
        .attr("id", "clip")
      .append("rect")
        .attr("width", width)
        .attr("height", height);

    var focus = svg.append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var context = svg.append("g")
        .attr("transform", "translate(" + margin2.left + "," + margin2.top + ")");

    focus.append("path")
        .attr("class", "area")
        .attr("clip-path", "url(#clip)")
        .attr("d", area);

    focus.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    focus.append("g")
        .attr("class", "y axis")
        .call(yAxis);

    focus.append("path")
        .attr("class", "line")
        .attr("clip-path", "url(#clip)")
        .attr("d", line);

    focus.selectAll(".dot")
        .data(data.filter(function(d) { return d.y; }))
      .enter().append("circle")
        .attr("clip-path", "url(#clip)")
        .attr("class", "dot modal-dialog")
        .attr("href", function(d) { return '/' + get_current_language() + '/weight/' + d.id + '/edit/'; })
        .attr("id", function(d) { return d.id; })
        .attr("cx", line.x())
        .attr("cy", line.y())
        .attr("r", 5);

    context.append("path")
        .attr("class", "area")
        .attr("d", area2);

    context.append("path")
        .attr("class", "line")
        .attr("d", line2);

    context.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height2 + ")")
      .call(xAxis2);

    context.append("g")
          .attr("class", "x brush")
          .call(brush)
        .selectAll("rect")
          .attr("y", -6)
          .attr("height", height2 + 7);

  function brush() {
      x.domain(brush.empty() ? x2.domain() : brush.extent());
      focus.select("path").attr("d", area);
      focus.select(".line").attr("d", line);

      focus.selectAll(".dot")
          .attr("cx", line.x())
          .attr("cy", line.y());

      focus.select(".x.axis").call(xAxis);
    }

    // Make the circles clickable: open their edit dialog
    form_modal_dialog();
}



function weight_log_chart(data, div_id, reps_i18n)
{
    var margin = {top: 20, right: 80, bottom: 30, left: 50},
        width = 600 - margin.left - margin.right,
        height = 200 - margin.top - margin.bottom;

    var parseDate = d3.time.format("%Y-%m-%d").parse;

    var x = d3.time.scale()
        .range([0, width]);

    var y = d3.scale.linear()
        .range([height, 0]);

    var color = d3.scale.category10();

    var xAxis = d3.svg.axis()
        .scale(x)
        .ticks(6)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .ticks(6)
        .orient("left");

    var line = d3.svg.line()
        .interpolate("cardinal")
        .tension(0.6)
        .x(function(d) { return x(d.date); })
        .y(function(d) { return y(d.weight); });

    var svg = d3.select("#svg-" + div_id).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


      color.domain(d3.keys(data[0]).filter(function(key){
                                      //console.log(key);
                                          return ($.inArray(key, ['date', 'id']) == -1);
                                          })
                          );

      data.forEach(function(d) {
        d.date = parseDate(d.date);
      });


      var reps = color.domain().map(function(name) {

       temp_values = data.filter(function(d) {
              return(+d[name] > 0);
              });

        filtered_values = temp_values.map(function(d) {
            return {date: d.date,
                    weight: +d[name],
                    log_id: d.id};
            });

        return {
          name: name,
          values: filtered_values
        };
      });

      x.domain(d3.extent(data, function(d) { return d.date; }));

      // Add 1 kg of "breathing room" on the min value, so the diagrams don't
      // too flat
      y.domain([
        d3.min(reps, function(c) { return d3.min(c.values, function(v) { return v.weight - 1; }); }),
        d3.max(reps, function(c) { return d3.max(c.values, function(v) { return v.weight; }); })
      ]);

      svg.append("g")
          .attr("class", "x axis")
          .attr("transform", "translate(0," + height + ")")
          .call(xAxis);

      svg.append("g")
          .attr("class", "y axis")
          .call(yAxis)
        .append("text")
          .attr("transform", "rotate(-90)")
          .attr("y", 6)
          .attr("dy", ".71em");
          //.style("text-anchor", "end")
          //.text("Weight");

      var log_series = svg.selectAll(".log_series")
          .data(reps)
        .enter().append("g")
          .attr("class", "log_series");

      log_series.append("path")
          .attr("class", "line")
          .attr("d", function(d) { return line(d.values); })
          .style("stroke", function(d) { return color(d.name); });

        reps.forEach(function(d){
            color_name = d.name
            temp_name = hex_random();
            color_class = 'color-' + color(color_name).replace('#', '');

            svg.selectAll(".dot" + temp_name)
              .data(d.values)
            .enter().append("circle")
              .attr("class", "dot modal-dialog " + color_class)
              .attr("cx", line.x())
              .attr("cy", line.y())
              .attr("id", function(d) { return d.log_id; })
              .attr("href", function(d) { return '/' + get_current_language() + '/workout/log/edit-entry/' +  d.log_id.match(/\d+/); })
              .attr("r", 5)
              .style("stroke", function(d) {
                return color(color_name);
              });
        });


      log_series.append("text")
          .datum(function(d) { return {name: d.name, value: d.values[d.values.length - 1]}; })
          .attr("transform", function(d) { return "translate(" + x(d.value.date) + "," + y(d.value.weight) + ")"; })
          .attr("x", 6)
          .attr("dy", ".35em")
          .text(function(d) { return d.name + " " + reps_i18n; });

    // Make the circles clickable: open their edit dialog
    form_modal_dialog();
}

function toggle_weight_log_table()
{
    $(".weight-chart-table-toggle").click(function(e) {
        e.preventDefault();
        target = $(this).data('toggleTarget');
        $('#' + target).toggle({effect: 'blind', duration: 600});
        });
}

/*
 *
 * Helper function to load the target of a link into the main-content DIV (the
 * main left colum)
 *
 */
function load_maincontent()
{
    $(".load-maincontent").click(function(e) {
        e.preventDefault();
        var targetUrl = $(this).attr("href");

        $.get(targetUrl, function(data) {
            // Load the data
            $('#main-content').html($(data).find('#main-content').html());

            // Update the browser's history
            current_url = $(data).find("#current-url").data('currentUrl');
            history.pushState({}, "", current_url);

            load_maincontent();
        });
    });
}

/*
 * Helper function to prefetch images on a page
 */
function prefetch_images(imageArray)
{
    $(imageArray).each(function(){
        (new Image()).src = this;
        //console.log('Preloading image' + this);
    });
}


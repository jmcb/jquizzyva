var add_search = function(this_pane)
    {
        tabs.search_items++

        var comp = $("#search_component").clone()

        comp.attr("id", "search_component"+tabs.search_items)
        comp.children().children().each(function(index)
            {
                if ($(this).attr("id"))
                {
                    $(this).attr("id", $(this).attr("id")+tabs.search_items)
                }
                if ($(this).attr("for"))
                {
                    $(this).attr("for", $(this).attr("for")+tabs.search_items)
                }
            })
        $(".add", comp).button({icons: {primary: "ui-icon-plus"}, text: false}).click(function(){add_search(this_pane)})
        $(".delete", comp).button({icons: {primary: "ui-icon-minus"}, text: false}).click(function(){
            $(this).parent().parent().empty()
            return false
        })
        $(".negated", comp).button({icons: {primary: "ui-icon-closethick"}, text:false})
        $(".search_types", comp).selectmenu({
            style:'dropdown', 
            width: 300}
        ).change(function()
            {
                var make_input = function()
                    {
                        return $("<input type='text'>").addClass("ui-widget-header").addClass("ui-state-default").addClass("ui-corner-all").height($("#load_button").innerHeight()-1).keypress(function(event)
                        {
                            var row = $(this).parent().parent()
                            var is_number = row_elements(row) == 2

                            var keys = String.fromCharCode(event.which).toUpperCase()
                            if (/[A-Z\[\]\*\?\^0-9]*/.test(keys))
                            {
                                if (!is_number && /\d/.test(keys))
                                {
                                    return false
                                }
                                else if (is_number && /[^\d]/.test(keys))
                                {
                                    return false
                                }
                            }
                        }).keyup(function()
                            {
                                $(this).val($(this).val().toUpperCase())
                            })
                    }

                var val = $(this).val()
                if (val == "AnagramMatch" || val == "SubanagramMatch" || val == "PatternMatch")
                {
                    var row = $(".search_term_first", $(this).parent().parent())
                    if (!row.children().length)
                        row.empty().append(make_input())
                    else if (/\d/.test($("input", row).val()))
                        $("input", row).val("")

                    row = $(".search_term_second", $(this).parent().parent())
                    if (row.children().length)
                        row.empty()
                }
                else
                {
                    var row = $(".search_term_first", $(this).parent().parent())
                    if (!row.children().length)
                        row.empty().append(make_input())
                    else if (/[^\d]/.test($("input", row).val()))
                        $("input", row).val("")

                    row = $(".search_term_second", $(this).parent().parent())
                    if (!row.children().length)
                        row.empty().append(make_input())
                    else if (/[^\d]/.test($("input", row).val()))
                        $("input", row).val("")
                }
            }).change()

        comp.insertBefore($(".search_button_table", $(this_pane)))
        return comp
    }

var add_search_pane = function ()
{
    tabs.search_tabs++
    var this_pane = "#search_pane" + tabs.search_tabs
    $("#tabs").tabs("add", this_pane, "Search&nbsp;&nbsp;")
    $(this_pane).append($("#search_pane").children().clone())
    $(".results_grid", $(this_pane)).flexigrid({
        height:'auto',
        striped: true,
        sortname: "alphagram",
        sortorder: "asc",
        dataType: "json",
        autoload: false,
        resizable: false,
        minColToggle: 0,
        colModel: [
            {"display": "?", name: "alphagram", width: 50, sortable: false, align: 'center'},
            {"display": "<", name: "front_hooks", width: 50, sortable: false, align: 'right'},
            {"display": "Word", name: "word", width: 150, sortable: true, align: 'center'},
            {"display": ">", name: "back_hooks", width: 50, sortable: false, align: 'left'},
            {"display": "Definition", name: "definition", width: 400, sortable: false, align: "left"},
        ],
        width: 700,
        height: 300,
    })
    lexicon_selector($(".search_lexicon_select", $(this_pane)))
    $("#do_search", $(this_pane)).button({icons: {primary: "ui-icon-search"}}).click(function()
        {
            var result = []
            var validate_failed = false

            $(".search_components", this_pane).each(function()
                {
                    if (!validate_row(this))
                    {
                        validate_failed = true
                        return false
                    }

                    result.push(serialise_row(this))
                })

            if (validate_failed)
                return false

            var progress = dialog("Searching, please wait...")

            lexicon = $(".search_lexicon_select", this_pane).children().first().val()

            var data = {"s": JSON.stringify(result), "l": lexicon}

            $.post("http://wxwhatever.com/cgi-bin/search.json?", data, function(data)
                {
                    progress.dialog("close")

                    var results = {total: data.length, page: 1, rows: []}
                    $.each(data, function(index) {
                        results.rows.push({cell: this})
                    })

                    $(".results_grid", this_pane).flexAddData(results)

                    if (results.total == 0)
                    {
                        $(".flash_messages", this_pane).empty()
                        $("<span>No results.</span>").attr("id", "cur_flash_message").appendTo(".flash_messages", this_pane).fadeIn().fadeOut().fadeIn()
                        setTimeout(function() {
                            $("#cur_flash_message").fadeOut(500)
                        }, 3000)
                    }
                })

            $(document).ajaxError(function (e, xhr, settings, exception)
            {
                progress.dialog("close")
                dialog("Error!", "Error in: " + settings.url + ' \n' + 'error:\n' + xhr.responseText, true)
            })

            return false
        })

    add_search(this_pane)
    $(".delete", this_pane).button("option", "disabled", true)
    $("#tabs").tabs("select", $("#tabs").tabs("length") - 1)
    return $(this_pane)
}

var row_elements = function (row)
{
    var search_type = $(".search_types", row).val()
    if (search_type == "AnagramMatch" || search_type == "SubanagramMatch" || search_type == "PatternMatch")
    {
        return 1
    }
    else
    {
        return 2
    }
}

var serialise_row = function (row) {
    var search_type = $(".search_types", row).val()
    var negated = $(".search_negated", row).hasClass("ui-state-active")
    if (row_elements(row) == 1)
    {
        return {"search_type": search_type, "negated": negated, search_string: $(".search_term_first input", row).val()}
    }
    else
    {
        return {"search_type": search_type, "negated": negated, search_range_start: parseInt($(".search_term_first input", row).val()), search_range_stop: parseInt($(".search_term_second input", row).val())}
    }
}

var validate_row = function (row)
{
    var search_type = $(".search_types", row).val()
    var flash_message = ""
    var par = $(this).parent().parent().parent().parent().parent()

    if ($(".search_term_first input", row).val().trim()=="")
    {
        flash_message = "Can't search for nothing!"
    }

    if (row_elements(row) == 1)
    {
        var term = $(".search_term_first input", row).val()
        // Validate that the pattern is valid.
        if (/\[\^?[A-Z]*$/.test(term))
            flash_message = "Character set does not end!"
        if (/^[A-Z\*\?]*\]/.test(term))
            flash_message = "Character set does not start!"
        if (/\[\^?\]/.test(term))
            flash_message = "Empty character set!"
        if (/\[\^?[A-Z]*[\?\*]+[A-Z]*\]/.test(term))
            flash_message = "Can't have wildcards in character sets!"
    }

    if (row_elements(row) == 2)
    {
        if ($(".search_term_second input", row).val().trim() == "")
            $(".search_term_second input", row).val($(".search_term_first input", row).val())
    }


    if (flash_message.trim() != "")
    {
        $(".flash_messages", par).empty()
        $("<span>"+flash_message+"</span>").attr("id", "cur_flash_message").appendTo(".flash_messages", par).fadeIn().fadeOut().fadeIn()
        setTimeout(function() {
            $("#cur_flash_message").fadeOut(500)
        }, 3000)

        return false
    }

    return true
}

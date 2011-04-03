var saver = function() {

    var cur_tab = $("#tabs").tabs("option", "selected")
    var cur_pane = $("#search_pane" + cur_tab)

    if (!cur_pane.length)
        return false

    var result = []
    var validate_failed = false

    $(".search_components", cur_pane).each(function()
        {
            if (!validate_row(this, true))
            {
                validate_failed = true
                return false
            }

            result.push(serialise_row(this))
        })

    if (validate_failed)
        return false

    var lexicon = $(".search_lexicon_select", cur_pane).children().first().val()

    var form = $("<form method='POST' action='http://wxwhatever.com/cgi-bin/search.json'>")
    form.append($("<input type='hidden' name='v'>").val(JSON.stringify(result)))
    form.append($("<input type='hidden' name='l'>").val(current_lexicon()))
    form.css("display", "none")
    $("body").append(form)
    form.submit()
    form.remove()
}

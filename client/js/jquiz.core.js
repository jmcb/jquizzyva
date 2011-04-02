var dialog = function (title, text, no_load)
{
    var dia = $("<div>"
        ).append(
            $("<p>").addClass(
                (no_load) ? "" : "loading_div"
                ).html("&nbsp;")
        ).addClass("jquiz_dialog"
        ).dialog({
            modal: true,
            buttons: ((no_load) ? {
                "OK": function() {
                    $(this).dialog("close")
                    }
                } : {}),
            close: 
                function() {
                    $(this).dialog("destroy").remove()
                },
            title: text,
            }
        ).dialog("open")
    return dia
}

var current_lexicon = function (no_default)
{
    var cur = $.cookie("jquiz_default_lexicon")
    
    if (!cur && no_default)
        return "CSW"

    return cur
}

var lexicon_selector = function (element_to_append)
{
    var selector = $("#search_lexicon_base").clone().attr("id", "")
    var lexicon = current_lexicon(true)

    if (lexicon)
    {
        selector.children().each(
            function()
            {
                if ($(this).val() == lexicon)
                    $(this).attr("selected", true)
            })
    }
    
    if (element_to_append.length)
        selector.appendTo(element_to_append)

    selector.selectmenu({
        style: 'dropdown',
        width: 300
    })

    return selector
}

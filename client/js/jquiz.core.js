var dialog = function (text, no_load)
{
    var dia = $("<div>").append($("<p>").text(text)).append($("<p>").addClass((no_load) ? "" : "loading_div").html("&nbsp;")).addClass("jquiz_dialog").dialog({modal: true, buttons: ((no_load) ? {"OK": function() {$(this).dialog("close")}} : {}), close: function() {$(this).dialog("destroy").remove();}}).dialog("open")
    return dia;
}

var lexicon_selector = function (element_to_append)
{
    var selector = $(".search_lexicon").clone()
    var lexicon = $.cookie("jquiz_default_lexicon")

    if (lexicon)
    {
        selector.children().each(
            function()
            {
                if ($(this).val() == lexicon)
                    $(this).attr("selected", true);
            })
    }
    
    if (element_to_append.length)
        selector.appendTo(element_to_append)

    selector.selectmenu({
        style: 'dropdown',
        width: 300});

    return selector
}

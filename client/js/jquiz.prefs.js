var preferences = function ()
{
    var column = $("<td>")

    var table = $("<table>").append(
        $("<tr>").append(
            column.clone().append($("<p>Select default lexicon:</p>"))
                ).append(
            column.clone().attr("id", "default_lexicon"))
            )

    var get_lexicon = function (event) {
        $.cookie("jquiz_default_lexicon", $("#default_lexicon").children().first().val(), {expires: 14})
        $(this).dialog("destroy").remove()
    }

    var dia = $("<div>").append(table).addClass("jquiz_dialog").dialog({
        modal: true,
        buttons: {
            "OK": get_lexicon
        },
        close: get_lexicon,
        width: 500,
        title: "jQuizzyva Preferences"
    }).dialog("open")

    lexicon_selector($("#default_lexicon"))

    return dia
}

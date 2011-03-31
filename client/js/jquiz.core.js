var dialog = function (text, no_load)
{
    var dia = $("<div>").append($("<p>").text(text)).append($("<p>").addClass((no_load) ? "" : "loading_div").html("&nbsp;")).addClass("jquiz_dialog").dialog({modal: true, buttons: ((no_load) ? {"OK": function() {$(this).dialog("close")}} : {}), close: function() {$(this).dialog("destroy").remove();}}).dialog("open")
    return dia;
}

var loader = function ()
{
    var dia = $("<div>").append($("<p>").text("Please select saved search to load:")).append($("<form>").append($("<input id='uploader' type='file'>"))).addClass("jquiz_dialog").dialog({modal: true, width: 400, close: function () { $(this).dialog("destroy").remove(); }}).dialog("open")
    $("#uploader", dia).fileinput({buttonText:"Select", buttonOptions: {icons: {primary: "ui-icon-folder-open"}}});
    $(".fileinput-input", dia).innerHeight($(".fileinput-wrapper .ui-button").innerHeight());
    $("input[type=file]", dia).attr("name", "d");
    $("form", dia).attr("action", "http://wxwhatever.com/cgi-bin/search.json?l=CSW").append($("<input type='hidden'").attr("name", "MAX_FILE_SIZE").val("100000")).attr("enctype", "multipart/form-data").attr("method", "POST").append($("<p>").append($("<input type='submit'>").val("Upload").attr("id", "load_saved_search_submit").button({icons: {primary: "ui-icon-transfer-e-w"}}))).ajaxForm({
        type: 'POST',
        url: 'http://wxwhatever.com/cgi-bin/search.json?l=CSW',
        dataType: 'json',
        success: function (responseText, statusText, xhr, element)
        {
            load_save(responseText);
        },
        iframe: 'iframe',
    });

    return dia;
}

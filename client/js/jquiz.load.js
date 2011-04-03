var load_save = function (data)
{
    var pane
    $.each(data, function (index)
        {
            if (index == 0)
            {
                pane = add_search_pane()
                new_row = pane
            }
            else
            {
                new_row = add_search(pane)
            }

            var st = this.search_type

            $(".search_types", new_row).selectmenu("value", st)
            
            var ind = $(".search_types", new_row).selectmenu("index")

            if (ind < 5)
            {
                $(".search_term_first input", new_row).val(this.search_string)
            }
            else
            {
                $(".search_term_first input", new_row).val(this.search_range_start)
                $(".search_term_second input", new_row).val(this.search_range_stop)
            }

            if (this.negated)
            {
                if ($(".negated", new_row).val() != "off")
                    $(".negated", new_row).button("widget").trigger("click.button")
            }
        }
    )
}

var loader = function ()
{
    var dia = $(
        "<div>"
        ).append(
            "<p>"
        ).append(
            $("<form>").append(
                $("<input id='uploader' type='file'>")
            )
        ).addClass("jquiz_dialog").dialog({
            modal: true,
            width: 500,
            title: "Please select saved search to load",
            close: function () {
                $(this).dialog("destroy").remove()
            }
        }).dialog("open")

    $("#uploader", dia).fileinput({
        buttonText:"Select",
        buttonOptions: {
            icons: {
                primary: "ui-icon-folder-open"
            }
        }
    })
    $(".fileinput-input", dia
        ).innerHeight(
            $(".fileinput-wrapper .ui-button"
                ).innerHeight()
            )

    $("input[type=file]", dia
        ).attr("name", "d")

    $("form", dia
        ).attr(
            "action", "http://wxwhatever.com/cgi-bin/search.json?l=" + current_lexicon()
        ).append(
            $("<input type='hidden'"
                ).attr("name", "MAX_FILE_SIZE"
                ).val("100000")
            ).attr(
                "enctype", "multipart/form-data"
            ).attr(
                "method", "POST"
            ).append(
                $("<p>").append(
                    $(
                        "<input type='submit'>"
                    ).val(
                        "Upload"
                    ).attr(
                        "id", "load_saved_search_submit"
                    ).button({
                        icons: {
                            primary: "ui-icon-transfer-e-w"
                        }
                    })
                )
            ).ajaxForm({
                type: 'POST',
                url: 'http://wxwhatever.com/cgi-bin/search.json?l=CSW',
                dataType: 'json',
                success: function (responseText, statusText, xhr, element)
                {
                    load_save(responseText)
                    dia.dialog("close")
                },
                iframe: 'iframe',
            }
        )

    return dia
}

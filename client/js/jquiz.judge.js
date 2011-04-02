var judge_mode = function()
{
    tabs.judge_mode = true;
    tabs.prompt_mode = false;
    tabs.challenge_mode = false;
    tabs.challenge_count = 0;
    tabs.loading = false;

    $("body").children().hide()
    $("#judge_pane").show();
    $("#return_button").click(function()
    {
        $("body").children().not(".ui-helper-hidden").not("ui-selectmenu-menu-popup").not("ul").show();
        $(".ui-tabs-panel .search_types").selectmenu("destroy").selectmenu({
                style:'dropdown', 
                width: 300});
        $("#judge_pane").hide();
        tabs.judge_mode = false;
    });
    var this_pane = $("#judge_pane");

    var reset_func = function()
    {
        $("#judge_entry").empty();
        $("#judge_message").html("Challenger: How many words would you like to challenge?");
        tabs.prompt_mode = false;
        tabs.challenge_mode = false;
    }

    var do_prompt = function()
    {
        tabs.prompt_mode = true;
        tabs.challenge_mode = false;
        var count = parseInt($("#judge_entry").html());
        tabs.challenge_count = count;
        $("#judge_message").html("1. Enter your word" + ((count != 1) ? "s, separated with COMMA." : "."));
        $("#judge_message").append("<br />").append("2. Press TAB or ENTER to challenge.");
        $("#judge_entry").html("");
    }

    var do_challenge = function()
    {
        tabs.prompt_mode = false;
        tabs.challenge_mode = true;
        tabs.loading = true;
        var words = []
        $.each($("#judge_entry").html().split(","), function()
            {
                if (this.trim() != "")
                    words.push(this.trim());
            });

        var data = {"w": JSON.stringify(words), "l": current_lexicon()};

        $("#judge_entry").empty().addClass("loading_div");

        $.post("http://wxwhatever.com/cgi-bin/search.json?", data, function(data)
            {
                tabs.loading = false;

                $("#judge_entry").removeClass("loading_div")
                if (data == "yes")
                    $("#judge_entry").empty().append($("<span>").css("color", "#00ff00").html("Yes, the play " + words.join(", ") + " is acceptable!"));
                else
                    $("#judge_entry").empty().append($("<span>").css("color", "#ff0000").html("No. " + words.join(", ") + " is not acceptable!"));

                $("#judge_entry").oneTime(5000, "reset", reset_func);
            });

        $(document).ajaxError(function (e, xhr, settings, exception)
        {
            tabs.loading = false;
            $("#judge_entry").removeClass("loading_div")
            dialog('Error in: ' + settings.url + ' \n' + 'error:\n' + xhr.responseText, true);
        });
    }

    reset_func();

    $("#judge_entry").html("");

    $(document).unbind("keypress").unbind("keydown");

    $(document).keypress(function(event) {
        if (!tabs.judge_mode || tabs.prompt_mode || tabs.challenge_mode)
            return;

        var keys = String.fromCharCode(event.which);
        var cur_cont = $("#judge_entry").html();


        if ("1234567890".indexOf(keys) != -1)
        {
            $("#judge_entry").append(keys);
            $("#judge_entry").stopTime();
            $("#judge_entry").oneTime(2500, do_prompt);
            return false;
        }
        }).keydown(
    function(event)
    {
        if (!tabs.judge_mode || tabs.prompt_mode || tabs.challenge_mode)
            return;

        var cur_cont = $("#judge_entry").html();
        if (event.which == 8)
        {
            $("#judge_entry").html(cur_cont.substr(0, cur_cont.length - 1));
            return false;
        }
        else if (event.which == 13)
        {
            var count = parseInt($("#judge_entry").html());
            if (!count)
                return false;

            $("#judge_entry").stopTime();

            do_prompt();
            return false;
        }
    }).keypress(function(event)
    {
        if (!tabs.judge_mode || !tabs.prompt_mode)
            return;

        var keys = String.fromCharCode(event.which).toUpperCase();
        if ("ABCDEFGHIJKLMNOPQRSTUVWXYZ".indexOf(keys) != -1)
        {
            $("#judge_entry").append(keys);
            return false;
        }
        else if (event.which == 44)
        {
            if (tabs.challenge_count <= 1)
                return false;
            
            tabs.challenge_count--;

            $("#judge_entry").append(", ");
            return false;
        }
    }).keydown(
    function(event)
    {
        if (!tabs.judge_mode || !tabs.prompt_mode)
            return;

        var cur_cont = $("#judge_entry").html();

        if (event.which == 8)
        {
            if ($("#judge_entry").text().substr(-1) == ",")
                tabs.challenge_count++;

            $("#judge_entry").html(cur_cont.substr(0, cur_cont.length - 1));
            return false;
        }
        else if (event.which == 9)
        {
            do_challenge();
            return false;
        }
    }).keypress(function(event)
    {
        if (!tabs.judge_mode || !tabs.challenge_mode || tabs.loading)
            return;

        $("#judge_entry").stopTime();
        reset_func();
    });
}

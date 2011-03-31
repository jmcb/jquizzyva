var add_quiz_pane = function()
{
    tabs.quiz_tabs++;
    var this_pane = "#quiz_pane" + tabs.quiz_tabs;
    $("#tabs").tabs("add", this_pane, "Quiz&nbsp;&nbsp;");
    $(this_pane).append($("#quiz_pane").children().clone());
    $("#tabs").tabs("select", $("#tabs").tabs("length") - 1);
}

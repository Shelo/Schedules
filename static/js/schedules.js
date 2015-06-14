$(".schedules-block").click(function()
{
    $(this).toggleClass("schedules-block-selected");
});

$(".schedules-block-row").click(function()
{
    var row = $(this).parent();
    console.log(row.children());

    row.children().each(function()
    {
        if (!$(this).hasClass("schedules-block-row"))
        {
            $(this).toggleClass("schedules-block-selected");
        }
    });
});
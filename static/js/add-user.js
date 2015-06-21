function submitNewUser(postUrl, csrf)
{
    var userInput = $('#users');
    var username = userInput.val();

    userInput.val("");

    $.post(postUrl, {
        username: username,
        csrfmiddlewaretoken: csrf
    }, function(data)
    {
        if (data == "true")
        {
            showMessage("Successfully added " + username + ".", "success");
        }
        else if (data == "false")
        {
            showMessage("Error trying to add " + username + ".", "alert");
        }
        else if (data == "")
        {
            showMessage("User " + username + " is a member.", "info");
        }
    })
        .fail(function()
    {
        alert("Interval server error.");
    });
}

function showMessage(message, alertType)
{
    var alert = $('<div class="alert-box ' + alertType + '">');
    alert.text(message);
    $('#add-users-messages').prepend(alert);
    alert.delay(3000).slideUp();
}

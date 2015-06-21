function displayMembers(url, removeUrl, csrf)
{
    var container = $('#remove-members-container');
    var loading = $('#remove-members-retrieving');

    $.ajax({
        dataType: 'json',
        url: url
    })
        .done(function(data)
        {
            container.empty();

            for (var i  = 0; i < data.length; i++)
            {
                var user = data[i];

                var tr = $('<tr>');
                var username = $('<td>');
                var fullname = $('<td>');
                var remove = $('<td>');
                var button = $('<i class="fi-x fg-red pointer">');

                // set the button callback.
                button.data('username', user.username);
                button.data('row', tr);
                button.click(function()
                {
                    removeMember($(this), removeUrl, csrf);
                });

                // add button to the remove column.
                remove.append(button);

                username.text(user.username);
                fullname.text(user.fullname);

                tr.append(username);
                tr.append(fullname);
                tr.append(remove);

                container.append(tr);
            }

            loading.remove();
        });
}

function removeMember(button, url, csrf)
{
    var username = button.data('username');

    $.ajax({
        data: {
            username: username,
            csrfmiddlewaretoken: csrf
        },
        url: url,
        method: 'post',
    })
        .done(function(data)
        {
            if (data)
            {
                button.data('row').remove();
            }
        })
}
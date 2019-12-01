function create_user() {
    var salt = "K80Tgi^w1&jc";
    var username = $("#username").val();
    var password = $("#password").val();

    if (username =='') {
        $('input[type="text"]').css("border","2px solid red");
        $('input[type="text"]').css("box-shadow","0 0 3px red");
        alert("Please provide a username.");
    }
    else if (password =='') {
        $('input[type="password"]').css("border","2px solid red");
        $('input[type="password"]').css("box-shadow","0 0 3px red");
        alert("Please provide a password.");
    } else {
        $.post(username, { password_hash: sha1(salt + username + password + salt + username) }, function(response) {
            if (response.status == "success") {
                window.location.href = response.redirect;
            } else {
                alert("Could not log in: " + response.message);
            }
        }, "json");
    }
}

$(document).ready(function() {
    $("#createuser").click(create_user);
    $('form').submit(false);
});

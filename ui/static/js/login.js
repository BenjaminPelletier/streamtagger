function login() {
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
        $.post("login", { username: username, password_hash: sha1(salt + password + salt) }, function(response) {
            if (response.success) {
                window.location.href = response.redirect;
            } else {
                alert("Could not log in: " + response.message);
            }
        }, "json");
    }
}

function keyup_login(event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        login();
    }
}

$(document).ready(function() {
    $("#login").click(login);
    $("#username").keyup(keyup_login);
    $("#password").keyup(keyup_login);
});

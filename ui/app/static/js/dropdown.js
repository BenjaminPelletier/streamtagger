/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function show_user_dropdown(element_id) {
  document.getElementById(element_id).classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn') && !event.target.matches('.actionbtn')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}

function logout() {
    window.location.href = "/logout";
}

function goHome() {
    window.location.href = '/';
}

function goTags() {
    window.location.href = '/tags';
}

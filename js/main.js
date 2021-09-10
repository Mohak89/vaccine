fetch("../navbar.html")
    .then((response) => response.text())
    .then((html) => {
        document.getElementById("navBar").innerHTML = html;
    })
    .then(() => {
        var toggle_button = document.getElementById("toggleButton")
        toggle_button.addEventListener("click", () => {
            var classes = document.getElementsByClassName("mainMenu")[0].classList
            if (classes.contains("active")) {
                classes.remove("active")
                toggle_button.classList.remove("cross")
            } else {
                toggle_button.classList.add("cross")
                classes.add("active")
            }
        })
    })
fetch("../footer.html")
    .then((response) => response.text())
    .then((html) => {
        document.getElementById("footer").innerHTML = html;
    })
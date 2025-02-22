function enterForge() {
    let name = document.getElementById("username").value;
    let responseText = document.getElementById("response-text");

    if (name.trim() === "") {
        responseText.innerHTML = "You must give the Inquisitor your name.";
    } else {
        responseText.innerHTML = `Welcome, ${name}. Choose your path.`;
        setTimeout(() => {
            window.location.href = "choose.html"; // Redirect to the next page
        }, 2000);
    }

    responseText.classList.remove("hidden");
}


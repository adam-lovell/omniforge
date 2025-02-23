function submitDesire() {
    let desire = document.getElementById("desire").value;
    if (desire.trim() === "") {
        alert("You must state your desire to the Inquisitor.");
    } else {
        localStorage.setItem("userDesire", desire); // Store desire for later use
        window.location.href = "vetra.html"; // Redirect to Vetra
    }
}



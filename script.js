document.addEventListener("DOMContentLoaded", function () {
    const responseText = document.getElementById("response-text");
    const inputField = document.getElementById("username");
    const submitButton = document.getElementById("submit-button");

    let step = 0;  // Track conversation steps

    submitButton.addEventListener("click", function () {
        let input = inputField.value.trim();

        if (input === "") {
            responseText.innerHTML = "You must give the Inquisitor your name.";
            return;
        }

        if (step === 0) {
            responseText.innerHTML = `Welcome, ${input}.<br>What is it you desire?`;
            inputField.value = "";
            step = 1;
        } 
        else if (step === 1) {
            responseText.innerHTML = `How will you achieve this desire?`;
            inputField.value = "";
            step = 2;
        } 
        else if (step === 2) {
            responseText.innerHTML = `The Inquisitor offers guidance. Choose your path:`;
            setTimeout(() => {
                window.location.href = "choose.html";  // Redirect to choice page
            }, 2000);
        }
    });
});



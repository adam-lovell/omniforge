// Load Firebase SDK
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-app.js";
import { getFirestore, collection, addDoc } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-firestore.js";

// Firebase Configuration
const firebaseConfig = {
  apiKey: "AIzaSyCfanKgFO98R1uKPpEAUUFOW1U66knL8Zs",
  authDomain: "hellforge-13d88.firebaseapp.com",
  projectId: "hellforge-13d88",
  storageBucket: "hellforge-13d88.appspot.com",
  messagingSenderId: "453743116508",
  appId: "1:453743116508:web:8beaee82ff6b78a2167419",
  measurementId: "G-WRCFGP7F79"
};

// Initialize Firebase & Firestore
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

// Submit Desire Function (Updated Redirect to manifest.html)
async function submitDesire() {
    let desire = document.getElementById("desire").value.trim();

    if (desire === "") {
        alert("You must state your desire to the Inquisitor.");
    } else {
        try {
            await addDoc(collection(db, "desires"), { text: desire });
            alert("Desire recorded in Firestore!");
            localStorage.setItem("userDesire", desire);
            window.location.href = "manifest.html"; // Now redirects correctly
        } catch (error) {
            console.error("Error adding document: ", error);
            alert("Failed to save to Firebase.");
        }
    }
}

// Attach event listener to button
document.addEventListener("DOMContentLoaded", function () {
    document.querySelector("button").addEventListener("click", submitDesire);
});

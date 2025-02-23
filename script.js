// Load Firebase from CDN
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
firebase.initializeApp(firebaseConfig);
const db = firebase.firestore(); // Using Firestore (Old API)

// Submit Desire Function
function submitDesire() {
    let desire = document.getElementById("desire").value;
    if (desire.trim() === "") {
        alert("You must state your desire to the Inquisitor.");
    } else {
        db.collection("desires").add({ text: desire })
            .then(() => {
                alert("Desire recorded in Firestore!");
                localStorage.setItem("userDesire", desire);
                window.location.href = "vetra.html";
            })
            .catch(error => {
                console.error("Error adding document: ", error);
                alert("Failed to save to Firebase.");
            });
    }
}

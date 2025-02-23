// Import Firebase modules
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getFirestore, collection, addDoc } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js";

// ✅ Firebase Config (Fixed storageBucket URL)
const firebaseConfig = {
  apiKey: "AIzaSyCfanKgFO98R1uKPpEAUUFOW1U66knL8Zs",
  authDomain: "hellforge-13d88.firebaseapp.com",
  projectId: "hellforge-13d88",
  storageBucket: "hellforge-13d88.appspot.com",
  messagingSenderId: "453743116508",
  appId: "1:453743116508:web:8beaee82ff6b78a2167419",
  measurementId: "G-WRCFGP7F79"
};

// ✅ Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

// ✅ Save Desire to Firestore
async function saveToFirestore(desire) {
    try {
        const docRef = await addDoc(collection(db, "desires"), {
            text: desire,
            timestamp: new Date()
        });
        console.log("Desire stored with ID:", docRef.id);
    } catch (e) {
        console.error("🔥 ERROR SAVING DESIRE:", e);
    }
}

// ✅ Submit Desire Function (Now Saves to Firestore)
async function submitDesire() {
    let desire = document.getElementById("desire").value.trim();
    
    if (desire === "") {
        alert("You must state your desire to the Inquisitor.");
        return;
    }

    await saveToFirestore(desire); // 🔥 Save the desire to Firestore
    localStorage.setItem("userDesire", desire); // Store locally
    window.location.href = "vetra.html"; // Redirect to Vetra
}

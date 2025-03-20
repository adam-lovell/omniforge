// ✅ Import Firebase Modules
import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js';
import { getFirestore } from 'https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js';

// ✅ Firebase Config
export const firebaseConfig = {
    apiKey: "AIzaSyCfanKgFO98R1uKPpEAUUFOW1U66knL8Zs",
    authDomain: "hellforge-13d88.firebaseapp.com",
    projectId: "hellforge-13d88",
    storageBucket: "hellforge-13d88.firebasestorage.app",
    messagingSenderId: "453743116508",
    appId: "1:453743116508:web:8beaee82ff6b78a2167419",
    measurementId: "G-WRCFGP7F79"
};

// ✅ Initialize Firebase App & Firestore
export const app = initializeApp(firebaseConfig);
export const db = getFirestore(app);

console.log("🔥 Firebase Initialized in firebaseConfig.js");

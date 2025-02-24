// script.js (Updated VETRA JS with Firebase Integration)

// Import Firebase SDK via CDN (best for GitHub pages)
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import {
  getFirestore,
  collection,
  addDoc,
  getDocs,
  query,
  deleteDoc,
  doc
} from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";

// Firebase configuration (Your exact provided config)
const firebaseConfig = {
  apiKey: "AIzaSyCfanKgFO98R1uKPpEAUUFOW1U66knL8Zs",
  authDomain: "hellforge-13d88.firebaseapp.com",
  projectId: "hellforge-13d88",
  storageBucket: "hellforge-13d88.firebasestorage.app",
  messagingSenderId: "453743116508",
  appId: "1:453743116508:web:8beaee82ff6b78a2167419",
  measurementId: "G-WRCFGP7F79"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

// Firestore collection reference
const tasksCollection = collection(db, "vetra_tasks");

// Core VETRA functions (fully Firebase-powered)
window.addBurden = async () => {
  const burden = document.getElementById("burdenInput").value;
  if (!burden) {
    alert("State your burdens clearly, mortal.");
    return;
  }

  await addDoc(tasksCollection, { description: burden, timestamp: new Date() });
  alert(`Burden '${burden}' added.`);
  document.getElementById("burdenInput").value = "";
};

window.viewBurdens = async () => {
  const querySnapshot = await getDocs(query(tasksCollection));
  let burdens = "Your burdens:\n";
  querySnapshot.forEach((doc) => {
    burdens += `🔸 ${doc.data().description} (Logged: ${doc.data().timestamp.toDate()})\n`;
  });
  alert(burdens);
};

window.clearBurdens = async () => {
  const snapshot = await getDocs(tasksCollection);
  snapshot.forEach(async (document) => {
    await deleteDoc(doc(tasksCollection, document.id));
  });
  alert("Burdens have been cleared, mortal.");
};

// Firebase imports (modular v9+)
import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js';
import { getFirestore, collection, doc, getDoc, setDoc, addDoc, getDocs, deleteDoc, query, where } from 'https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js';

// Your config import (missing previously!)
import { firebaseConfig } from './firebase-config.js';

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

async function addBurdens(tasks, dailyTasks) {
  alert("BULK TASK ENTRY:\n\nCATEGORIES: Urgent & Important, Not Urgent but Important, Urgent but Not Important, Not Urgent & Not Important\n\nFORMAT: DESCRIPTION, CATEGORY, DATE (YYYY-MM-DD), TIME (HH:MM AM/PM), DURATION (e.g., 2h 30m)\n\nSEPARATE WITH ';'");

  const userInput = prompt("ENTER BURDENS:").trim();
  const taskEntries = userInput.split(";");

  const validCategories = Object.keys(tasks).reduce((acc, cat) => {
    acc[cat.toLowerCase()] = cat;
    return acc;
  }, {});

  let taskAdded = false;

  for (let entry of taskEntries) {
    const parts = entry.split(",").map(p => p.trim());

    if (parts.length !== 5) {
      alert(`⚠️ INVALID FORMAT FOR: ${entry}\nREFRAME YOUR INTENT, MORTAL!`);
      continue;
    }

    let [description, category, date, time, duration] = parts;
    category = validCategories[category.toLowerCase()];

    if (!category) {
      alert(`⚠️ INVALID CATEGORY ENTRY: ${category}\nREFRAME YOUR INTENT, MORTAL!`);
      continue;
    }

    if (isNaN(Date.parse(date))) {
      alert(`⚠️ INVALID DATE FORMAT FOR: ${date}\nREFRAME YOUR INTENT, MORTAL!`);
      continue;
    }

    if (!time.match(/^\d{1,2}:\d{2} (AM|PM)$/i)) {
      alert(`⚠️ INVALID TIME FORMAT FOR: ${time}\nREFRAME YOUR INTENT, MORTAL!`);
      continue;
    }

    if (!duration.match(/\d+h|\d+m/)) {
      alert(`⚠️ INVALID DURATION FORMAT FOR: ${duration}\nREFRAME YOUR INTENT, MORTAL!`);
      continue;
    }

    const startTime24h = convertTo24h(time);
    const durationMinutes = convertDurationToMinutes(duration);

    let conflict = tasks[category].some(task => {
      const existingStart = convertTo24h(task.start_time);
      const existingEnd = existingStart + convertDurationToMinutes(task.duration);
      const newEnd = startTime24h + durationMinutes;
      return startTime24h < existingEnd && newEnd > existingStart;
    });

    if (conflict) {
      const override = confirm(`⚠️ OVERLAPPING BURDEN: '${description}' conflicts with an existing task.\nADD ANYWAY?`);
      if (!override) {
        alert(`BURDEN '${description}' NOT ADDED DUE TO CONFLICT.`);
        continue;
      }
    }

    const isRecurring = confirm(`IS '${description}' A RECURRING DAILY BURDEN?`);

    const taskData = { description, category, date, start_time: time, duration };

    if (isRecurring) {
      dailyTasks.push(taskData);
      await addDoc(collection(db, 'daily_tasks'), taskData);
      alert(`🔄 RECURRING BURDEN '${description}' ADDED.`);
    } else {
      tasks[category].push(taskData);
      await addDoc(collection(db, 'tasks'), taskData);
      alert(`📌 BURDEN '${description}' ADDED TO '${category}'.`);
    }

    taskAdded = true;
  }

  if (taskAdded) alert("✅ BURDEN LOCKED.");
}

function convertTo24h(timeStr) {
  const [time, modifier] = timeStr.split(' ');
  let [hours, minutes] = time.split(':').map(Number);

  if (modifier.toUpperCase() === 'PM' && hours < 12) hours += 12;
  if (modifier.toUpperCase() === 'AM' && hours === 12) hours = 0;

  return hours * 60 + minutes;
}

function convertDurationToMinutes(durationStr) {
  let total = 0;
  const parts = durationStr.match(/(\d+h)?\s?(\d+m)?/);
  if (parts[1]) total += parseInt(parts[1]) * 60;
  if (parts[2]) total += parseInt(parts[2]);
  return total;
}

async function viewBurdens(tasks, daily_tasks) {
  const tasksSnapshot = await getDocs(collection(db, "tasks"));
  const dailyTasksSnapshot = await getDocs(collection(db, "daily_tasks"));

  const loadedTasks = {}; // <-- renamed here
  tasksSnapshot.forEach((doc) => {
    const data = doc.data();
    const category = data.category;
    if (!loadedTasks[category]) loadedTasks[category] = [];
    loadedTasks[category].push(data);
  });

  const loadedDailyTasks = [];
  dailyTasksSnapshot.forEach((doc) => loadedDailyTasks.push(doc.data()));

  const categorizedRecurringTasks = {};
  Object.keys(loadedTasks).forEach((category) => categorizedRecurringTasks[category] = []);

  loadedDailyTasks.forEach(task => {
    const category = task.category || 'Not Urgent but Important';
    if (!categorizedRecurringTasks[category]) categorizedRecurringTasks[category] = [];
    categorizedRecurringTasks[category].push(task);
  });

  let displayMessage = "YOUR BURDENS:\n" + "=".repeat(40);

  Object.keys(loadedTasks).forEach(category => {
    const totalTasks = loadedTasks[category].length + (categorizedRecurringTasks[category]?.length || 0);

    displayMessage += `\n\n🔹 ${category} (${totalTasks} BURDENS):\n`;

    if (totalTasks === 0) {
      displayMessage += "(PITY, AN EMPTY VESSEL)\n";
      return;
    }

    loadedTasks[category].forEach((task, index) => {
      const { description, start_time, date } = task;
      displayMessage += `${index + 1}. ${description} | ⏰ ${start_time} | 📅 ${date}\n`;
    });

    categorizedRecurringTasks[category]?.forEach((task, index) => {
      const { description, start_time, date } = task;
      displayMessage += `${loadedTasks[category].length + index + 1}. ${description} | ⏰ ${start_time || "TBD"} | 📅 ${date || "Unknown"} | (RECURRING)\n`;
    });
  });

  alert(displayMessage);
}

async function shedBurdens(tasks, daily_tasks) {
    await viewBurdens(tasks, daily_tasks); // ✅ Show current burdens before removal

    const categoryInput = prompt("\nENTER THE CATEGORY OF THE BURDEN TO REMOVE:\n\nCATEGORY:").trim().toLowerCase();

    const validCategories = [
        'urgent & important',
        'not urgent but important',
        'urgent but not important',
        'not urgent & not important'
    ];

    if (!validCategories.includes(categoryInput)) {
        alert("⚠️ INVALID CATEGORY. REFRAME YOUR INTENT!");
        return;
    }

    const burdensRef = collection(db, "tasks");
    const q = query(burdensRef, where("category", "==", categoryInput));
    const snapshot = await getDocs(q);

    if (snapshot.empty) {
        alert("⚠️ NO BURDENS IN THIS CATEGORY.");
        return;
    }

    let taskMapping = [];
    let message = `📌 BURDENS IN '${categoryInput}':\n`;

    snapshot.forEach((doc, index) => {
        const task = doc.data();
        taskMapping.push({ id: doc.id, ...task });
        message += `${index + 1}. ${task.description} | ⏰ ${task.start_time} | 📅 ${task.date}\n`;
    });

    const taskNumInput = prompt(`${message}\nENTER BURDEN NUMBER TO REMOVE:`).trim();
    const taskNum = parseInt(taskNumInput) - 1;

    if (taskMapping[taskNum]) {
        await deleteDoc(doc(db, "tasks", taskMapping[taskNum].id));
        alert(`✅ BURDEN '${taskMapping[taskNum].description}' LIFTED.`);
    } else {
        alert("⚠️ INVALID NUMBER. REFRAME YOUR INTENT!");
    }
}

async function progressReport(tasks, dailyTasks) {
  alert("📜 PROGRESS REPORT: REVIEW YOUR BURDENS.\n");

  let allTasks = [];
  let taskMapping = {};
  let index = 1;

  // Load tasks from Firebase
  const tasksSnapshot = await getDocs(collection(db, "tasks"));
  const dailyTasksSnapshot = await getDocs(collection(db, "daily_tasks"));

  // Regular tasks
  tasksSnapshot.forEach((doc) => {
    const data = doc.data();
    taskMapping[index] = { id: doc.id, category: data.category, task: data };
    allTasks.push(`${index}. ${data.description} | ⏰ ${data.start_time} | 📅 ${data.date} (${data.category})`);
    index++;
  });

  // Recurring tasks
  dailyTasksSnapshot.forEach((doc) => {
    const data = doc.data();
    taskMapping[index] = { id: doc.id, category: "Recurring", task: data };
    let taskTime = data.start_time ? data.start_time : "TBD";
    allTasks.push(`${index}. ${data.description} | ⏰ ${taskTime} (RECURRING)`);
    index++;
  });

  if (allTasks.length === 0) {
    alert("⚠️ NO BURDENS TO UPDATE.");
    return;
  }

  // Show all tasks
  let taskList = allTasks.join("\n");
  let choice = prompt(`📌 YOUR BURDENS:\n${taskList}\n\nENTER THE NUMBER OF THE BURDEN TO UPDATE:`);

  if (!taskMapping[choice]) {
    alert("⚠️ INVALID CHOICE.");
    return;
  }

  let selectedTask = taskMapping[choice];
  let task = selectedTask.task;

  // Options for the user
  let action = prompt(`\nWHAT SHALL BE DONE?\n1. MARK AS COMPLETED ✅\n2. POSTPONE 🔄\n3. CANCEL ❌\n\nSPEAK A NUMERAL:`);

  if (action === "1") {
    // Remove completed task from Firebase
    await deleteDoc(doc(db, selectedTask.category === "Recurring" ? "daily_tasks" : "tasks", selectedTask.id));
    alert(`✅ BURDEN '${task.description}' LIFTED.`);

  } else if (action === "2") {
    // Postpone task
    let newDate = prompt("ENTER NEW DATE (YYYY-MM-DD):").trim();
    if (!newDate.match(/^\d{4}-\d{2}-\d{2}$/)) {
      alert("⚠️ INVALID DATE FORMAT. UPDATE FAILED.");
      return;
    }

    let taskRef = doc(db, selectedTask.category === "Recurring" ? "daily_tasks" : "tasks", selectedTask.id);
    await setDoc(taskRef, { ...task, date: newDate }, { merge: true });

    alert(`🔄 BURDEN '${task.description}' MOVED TO ${newDate}.`);

  } else if (action === "3") {
    alert("❌ UPDATE CANCELED.");

  } else {
    alert("⚠️ INVALID CHOICE.");
  }
}

// Save tasks to Firebase Firestore
async function saveTasks(tasks, dailyTasks) {
  const tasksRef = doc(db, 'vetra', 'burdens');
  await setDoc(tasksRef, { tasks, daily_tasks: dailyTasks, timestamp: new Date() });
  alert("✅ BURDENS LOCKED, UNTIL WE MEET AGAIN, MORTAL.");
}

// Load tasks from Firebase Firestore
async function loadTasks() {
  const tasksRef = doc(db, 'vetra', 'burdens');
  const docSnap = await getDoc(tasksRef);
  
  if (docSnap.exists()) {
    const data = docSnap.data();
    return [data.tasks, data.daily_tasks];
  } else {
    return [{
      "Urgent & Important": [],
      "Not Urgent but Important": [],
      "Urgent but Not Important": [],
      "Not Urgent & Not Important": []
    }, []];
  }
}

// Main program function
async function main() {
  let [tasks, dailyTasks] = await loadTasks();

  while (true) {
    let choice = prompt(
      "THE INQUISITOR HAS DELIVERED YOU TO ME.\n" +
      "I AM VETRA, DAUGHTER OF THE INQUISITOR.\n" +
      "STATE YOUR BURDENS, MORTAL.\n\n" +
      "1: ADD BURDEN.\n" +
      "2: VIEW BURDENS.\n" +
      "3: SHED BURDENS.\n" +
      "4: PROGRESS REPORT.\n" +
      "5: SAVE AND EXIT.\n\n" +
      "SPEAK A NUMERAL:"
    );

    if (choice === "1") {
      await addBurdens(tasks, dailyTasks);
    } else if (choice === "2") {
      await viewBurdens(tasks, dailyTasks);
    } else if (choice === "3") {
      await shedBurdens(tasks, dailyTasks);
    } else if (choice === "4") {
      await progressReport(tasks, dailyTasks);
    } else if (choice === "5") {
      await saveTasks(tasks, dailyTasks);
      break;
    } else {
      alert("⚠️ INVALID, REFRAME YOUR INTENT!");
    }
  }
}

// Initialize the program on page load
document.addEventListener('DOMContentLoaded', () => {
  const vetraBtn = document.getElementById('vetra-start-btn');
  if (vetraBtn) vetraBtn.addEventListener('click', main);
}); // initialize main loop
  
  // attach button listener after DOM loads
  const submitBtn = document.getElementById('submit-btn');
if (submitBtn) {
  submitBtn.addEventListener('click', async () => {
    let [tasks, dailyTasks] = await loadTasks();
    await addBurdens(tasks, dailyTasks);
    await saveTasks(tasks, dailyTasks);
  });
}





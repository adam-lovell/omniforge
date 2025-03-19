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

// SUBMIT DESIRE BUTTON ON MAIN PAGE
function submitDesire() {
  window.location.href = 'manifest.html';
}

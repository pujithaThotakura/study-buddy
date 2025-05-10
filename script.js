const goalForm = document.getElementById("goalForm");
const goalList = document.getElementById("goalList");
const progressText = document.getElementById("progressText");

async function fetchGoals() {
  const res = await fetch("/api/goals");
  const goals = await res.json();
  goalList.innerHTML = "";
  goals.forEach((goal, i) => {
    const li = document.createElement("li");
    li.textContent = `${goal.title} (${goal.type}) - ${goal.status}`;
    if (goal.status !== "completed") {
      const btn = document.createElement("button");
      btn.textContent = "Mark Complete";
      btn.onclick = () => markComplete(i);
      li.appendChild(btn);
    }
    goalList.appendChild(li);
  });
}

async function fetchProgress() {
  const res = await fetch("/api/progress");
  const data = await res.json();
  progressText.textContent = `✅ ${data.completed}/${data.total} goals completed (${data.percent.toFixed(2)}%)`;
}

goalForm.onsubmit = async (e) => {
  e.preventDefault();
  const title = document.getElementById("title").value;
  const type = document.getElementById("type").value;
  await fetch("/api/goals", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, type })
  });
  goalForm.reset();
  fetchGoals();
  fetchProgress();
};

async function markComplete(index) {
  await fetch(`/api/goals/${index}`, { method: "PUT" });
  fetchGoals();
  fetchProgress();
}

fetchGoals();
fetchProgress();

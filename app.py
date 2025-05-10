from flask import Flask, jsonify, request, render_template
import json
from datetime import datetime

app = Flask(__name__)

GOALS_FILE = "goals.json"

def load_goals():
    try:
        with open(GOALS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_goals(goals):
    with open(GOALS_FILE, "w") as f:
        json.dump(goals, f, indent=4)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/goals", methods=["GET"])
def get_goals():
    return jsonify(load_goals())

@app.route("/api/goals", methods=["POST"])
def add_goal():
    data = request.json
    goal = {
        "title": data["title"],
        "type": data["type"],
        "status": "pending",
        "created": datetime.now().isoformat()
    }
    goals = load_goals()
    goals.append(goal)
    save_goals(goals)
    return jsonify({"message": "Goal added!"}), 201

@app.route("/api/goals/<int:goal_index>", methods=["PUT"])
def complete_goal(goal_index):
    goals = load_goals()
    if 0 <= goal_index < len(goals):
        goals[goal_index]["status"] = "completed"
        save_goals(goals)
        return jsonify({"message": "Goal marked as complete!"})
    return jsonify({"error": "Invalid goal index"}), 400

@app.route("/api/progress", methods=["GET"])
def get_progress():
    goals = load_goals()
    total = len(goals)
    completed = sum(1 for g in goals if g["status"] == "completed")
    percent = (completed / total) * 100 if total else 0
    return jsonify({"completed": completed, "total": total, "percent": percent})

if __name__ == "__main__":
    app.run(debug=True)

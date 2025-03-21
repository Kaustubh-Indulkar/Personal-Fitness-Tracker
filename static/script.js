const API_URL = "http://127.0.0.1:5000";

// Log Workout
function logWorkout() {
    const exercise = document.getElementById("exercise").value;
    const duration = document.getElementById("duration").value;
    const calories = document.getElementById("workout_calories").value;

    fetch(`${API_URL}/log_workout`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ exercise, duration, calories })
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error("Error:", error));
}

// Log Meal
function logMeal() {
    const food = document.getElementById("food").value;
    const calories = document.getElementById("meal_calories").value;

    fetch(`${API_URL}/log_meal`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ food, calories })
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error("Error:", error));
}

// Log Weight
function logWeight() {
    const weight = document.getElementById("weight").value;
    const goal_weight = document.getElementById("goal_weight").value;

    fetch(`${API_URL}/log_weight`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ weight, goal_weight })
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error("Error:", error));
}

// View Log
function viewLog() {
    fetch(`${API_URL}/view_log`)
    .then(response => response.json())
    .then(data => {
        document.getElementById("logOutput").textContent = JSON.stringify(data, null, 2);
    })
    .catch(error => console.error("Error:", error));
}

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from flask import Flask, render_template, request, jsonify
import csv
import datetime

app = Flask(__name__)
FILE_NAME = "fitness_tracker.csv"

# Initialize CSV if not exists
def initialize_csv():
    try:
        with open(FILE_NAME, "x", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Type", "Detail", "Duration (mins)", "Calories", "Weight (kg)", "Goal Weight (kg)"])
    except FileExistsError:
        pass

initialize_csv()  # Initialize on startup

# Load and preprocess data
def load_data():
    try:
        df = pd.read_csv(FILE_NAME)
        df = df.dropna(subset=["Calories", "Weight (kg)"])
        df["Calories"] = pd.to_numeric(df["Calories"], errors='coerce')
        df["Weight (kg)"] = pd.to_numeric(df["Weight (kg)"], errors='coerce')
        return df
    except FileNotFoundError:
        return None

# Train ML model
def train_model():
    df = load_data()
    if df is None or df.shape[0] < 5:
        return None
    
    X = df[["Calories"]]
    y = df["Weight (kg)"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

model = train_model()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/log_workout", methods=["POST"])
def log_workout():
    data = request.json
    date = datetime.datetime.today().strftime("%Y-%m-%d")
    with open(FILE_NAME, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([date, "Workout", data["exercise"], data["duration"], data["calories"], "", ""])
    return jsonify({"message": "Workout logged successfully!"})

@app.route("/log_meal", methods=["POST"])
def log_meal():
    data = request.json
    date = datetime.datetime.today().strftime("%Y-%m-%d")
    with open(FILE_NAME, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([date, "Meal", data["food"], "", data["calories"], "", ""])
    return jsonify({"message": "Meal logged successfully!"})

@app.route("/log_weight", methods=["POST"])
def log_weight():
    data = request.json
    date = datetime.datetime.today().strftime("%Y-%m-%d")
    with open(FILE_NAME, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([date, "Weight", "", "", "", data["weight"], data["goal_weight"]])
    return jsonify({"message": "Weight recorded successfully!"})

@app.route("/view_log", methods=["GET"])
def view_log():
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            log_data = [row for row in reader]
        return jsonify(log_data)
    except FileNotFoundError:
        return jsonify({"error": "No fitness records found."}), 404

@app.route("/recommend", methods=["POST"])
def recommend_calories():
    global model
    if model is None:
        return jsonify({"error": "Not enough data to generate recommendations."}), 400
    
    data = request.json
    current_weight = float(data["current_weight"])
    goal_weight = float(data["goal_weight"])
    avg_calories = np.mean(load_data()["Calories"])
    
    predicted_weight = model.predict([[avg_calories]])[0]
    adjustment = (goal_weight - predicted_weight) * 100
    recommended_calories = avg_calories + adjustment
    
    return jsonify({"recommended_calories": round(recommended_calories, 2)})

if __name__ == "__main__":
    app.run(debug=True)

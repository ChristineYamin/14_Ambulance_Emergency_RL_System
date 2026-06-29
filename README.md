"# 14_Ambulance_Emergency_RL_System" 
# 🚑 Emergency Medical Supply Distribution Optimization

An AI-powered route optimization system for emergency medical supply distribution.

This project predicts travel time between medical locations using an **XGBoost Regressor** and optimizes the delivery sequence using a **Genetic Algorithm**. The final result is visualized through a professional **Streamlit dashboard** that shows the optimized route, model performance, travel-time improvement, and delivery sequence.

---

## 📌 Project Overview

Emergency medical supply distribution is a time-sensitive logistics problem. Hospitals and healthcare organizations need to deliver critical supplies to multiple clinics as efficiently as possible.

This project simulates a medical supply delivery system where a vehicle starts from a **Central Hospital**, visits multiple clinics, and returns to the hospital after completing all deliveries.

The system answers one main question:

> What is the most efficient delivery route for distributing emergency medical supplies to multiple clinics?

---

## 🎯 Project Objective

The objective of this project is to build an AI-powered optimization system that can:

* Predict travel time between medical locations
* Optimize the clinic delivery sequence
* Reduce total predicted delivery time
* Visualize the optimized route on an interactive map
* Present the results in a clear dashboard for decision-making

---

## 🧠 AI Pipeline

The project uses a two-stage AI pipeline:

### 1. Travel Time Prediction

An **XGBoost Regressor** is trained to predict travel time between two locations using trip-related features such as:

* Pickup latitude and longitude
* Dropoff latitude and longitude
* Trip distance
* Pickup hour
* Pickup weekday
* Weekend indicator
* Rush hour indicator

The trained model is saved as:

```text
model.pkl
```

### 2. Route Optimization

A **Genetic Algorithm** is used to search for the best delivery sequence.

The algorithm:

1. Creates multiple possible delivery routes
2. Calculates the predicted travel time for each route
3. Selects the best-performing routes
4. Generates new route combinations
5. Repeats the process across multiple generations
6. Returns the best route found

The route is constrained to:

```text
Central_Hospital → Clinic Stops → Central_Hospital
```

---

## 📊 Current Results

For the current optimized route:

| Metric                |     Value |
| --------------------- | --------: |
| Hospital              |         1 |
| Clinics Served        |        11 |
| Initial GA Route Time | 27.91 min |
| Optimized Route Time  | 26.83 min |
| Improvement           |     3.85% |
| Generations           |       100 |

The optimized route successfully starts and ends at **Central_Hospital**.

---

## 🗺️ Dashboard Features

The Streamlit dashboard includes:

* Professional dark navy command-center design
* KPI summary cards
* Optimized route map
* AI recommendation panel
* Before vs after optimization comparison
* Route sequence display
* Genetic Algorithm performance chart
* Clean optimized delivery route table
* Downloadable optimized route CSV

---

## 🖥️ Dashboard Preview

The dashboard visualizes the optimized medical supply delivery route and summarizes the AI recommendation.

> Note: The map line represents the optimized stop sequence. It does not represent turn-by-turn road navigation.

---

## 📁 Project Structure

```text
Emergency-Medical-Supply-Optimization/
│
├── app.py
├── model.pkl
├── requirements.txt
├── README.md
│
├── notebooks/
│   ├── train_XGBoost.ipynb
│   ├── route_optimization.ipynb
│   ├── optimized_supply_route.csv
│   ├── fitness_history.csv
│   └── locations.csv
│
└── images/
    └── dashboard_preview.png
```

---

## 📂 Important Files

### `train_XGBoost.ipynb`

This notebook trains the XGBoost travel-time prediction model and saves it as `model.pkl`.

### `route_optimization.ipynb`

This notebook uses the trained model and Genetic Algorithm to find the optimized medical supply delivery route.

It generates:

```text
optimized_supply_route.csv
fitness_history.csv
locations.csv
```

### `app.py`

This file runs the Streamlit dashboard and visualizes the final optimization results.

---

## 🛠️ Technologies Used

* Python
* Pandas
* NumPy
* XGBoost
* Scikit-learn
* Joblib
* Matplotlib
* Folium
* Streamlit
* Streamlit-Folium

---

## 🚀 How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/your-username/emergency-medical-supply-optimization.git
cd emergency-medical-supply-optimization
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit dashboard

```bash
streamlit run app.py
```

---

## 📦 Requirements

Example `requirements.txt`:

```text
streamlit
pandas
numpy
matplotlib
folium
streamlit-folium
xgboost
scikit-learn
joblib
```

---

## 🧬 Genetic Algorithm Logic

The Genetic Algorithm optimizes the delivery route using the following process:

1. Generate a population of random delivery routes
2. Evaluate each route using predicted travel time
3. Select the best routes as parent routes
4. Create new child routes from selected parents
5. Repeat the optimization process over multiple generations
6. Save the best route found

The final optimized route always follows this structure:

```text
Central_Hospital → Clinic_... → Clinic_... → Central_Hospital
```

---

## 🧪 Model Output Files

### `optimized_supply_route.csv`

Contains the final optimized route sequence.

Example:

```text
Visit Order,Location
1,Central_Hospital
2,Clinic_G
3,Clinic_F
...
13,Central_Hospital
```

### `fitness_history.csv`

Contains the Genetic Algorithm score across generations.

Example:

```text
Generation,Score
0,27.91
1,27.65
...
99,26.83
```

### `locations.csv`

Contains location names and coordinates used for visualization.

Example:

```text
Location,Latitude,Longitude
Central_Hospital,40.7580,-73.9855
Clinic_A,40.7610,-73.9770
```

---

## 📈 Key Insights

* The optimized route reduced predicted travel time compared with the initial GA route.
* The system successfully produced a valid route starting and ending at the central hospital.
* The dashboard makes the optimization result easy to understand through KPIs, map visualization, and route sequence display.
* This project demonstrates how machine learning and optimization can support emergency healthcare logistics.

---

## ⚠️ Limitation

The map currently visualizes the optimized stop sequence using coordinate connections. It does not generate real road-based navigation or turn-by-turn routing.

Future improvements could include:

* Road-based routing using OSRM or OpenRouteService
* Real-time traffic data integration
* Multiple delivery vehicles
* Supply priority levels
* Emergency demand forecasting
* Dynamic route re-optimization

---

## ✅ Final Outcome

This project demonstrates an end-to-end AI decision-support system for emergency medical supply delivery.

It combines:

* Machine learning prediction
* Genetic Algorithm optimization
* Interactive geospatial visualization
* Professional dashboard design

The final dashboard provides a clear and practical view of the recommended delivery route for emergency medical supply distribution.

---

## 👩‍💻 Author

Created by **Yamin**

Project 14 of the **23 Projects at 23** data science portfolio journey.

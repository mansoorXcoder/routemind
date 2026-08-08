# 🚚 RouteMind

> **AI-Powered Adaptive Route Optimization for Modern Supply Chains**

RouteMind is an AI-based adaptive route optimization platform designed to create efficient delivery routes and dynamically re-plan them when real-world situations change, such as **new pickups, failed deliveries, vehicle breakdowns, or other operational events**.

The goal is to make delivery routing **smarter, faster, flexible, and more practical for real-world logistics operations**.

---

## 👥 Team Members

* **Sravani G**
* **Keerthi Ch**
* **P. SSS Aswini Reddy**
*  **P. Mansoor Ali Khan**

---

## 🎯 Problem Statement

Traditional route planning usually creates a route based on the information available at the beginning of the delivery journey.

However, real-world delivery operations can change continuously.

For example:

* A customer may be unavailable.
* A new pickup request may arrive.
* A vehicle may break down.
* Delivery time windows may change.
* Vehicle capacity may become a constraint.

RouteMind addresses this problem by enabling **dynamic route re-planning** instead of relying only on a fixed route.

---

## 💡 Our Solution

RouteMind first creates an optimized route for multiple delivery stops.

When a new event occurs, the system evaluates the remaining deliveries and generates an updated route while considering operational constraints.

### Simple Flow

```text
Delivery Data
      ↓
Initial Route Planning
      ↓
Optimized Route
      ↓
Real-World Event
      ↓
AI-Based Re-planning
      ↓
Updated Route
      ↓
Final Dispatch
```

---

## ✨ Key Features

* 🤖 AI-assisted route planning
* 🚚 Multi-stop vehicle routing
* ⚡ Dynamic route re-planning
* 🗺️ OpenStreetMap road-network integration
* 📦 New pickup handling
* ❌ Failed delivery handling
* 🛡️ Constraint validation
* 📊 Route comparison and analytics
* 👨‍💼 Supervisor decision support
* 💡 Explainable routing decisions

---

## 🚨 Dynamic Re-planning

One of RouteMind's main features is its ability to react to changes during delivery operations.

### Example

```text
Original Route

Depot → A → B → C → D
```

Suppose delivery at **B fails**.

Instead of continuing with the original plan, RouteMind evaluates the remaining stops and creates a new feasible route.

```text
Updated Route

Depot → A → C → D
             ↓
        Re-plan if needed
```

This makes the system adaptive rather than static.

---

## 🧠 Real-World Constraints

RouteMind can consider practical logistics constraints such as:

* Delivery windows
* Zone timings
* Vehicle capacity
* Driver constraints
* Vehicle constraints
* COD cash-carry limits
* Failed deliveries
* New pickups

These constraints help make the generated routes more realistic.

---

## 🗺️ OpenStreetMap Integration

RouteMind can use **OpenStreetMap** road-network data for realistic routing.

Instead of downloading a huge country-wide road dataset, the required road network for a selected Indian city can be obtained on demand using **Overpass Turbo**.

### Flow

```text
OpenStreetMap
      ↓
Overpass Turbo
      ↓
Selected Indian City
      ↓
Road Network
      ↓
RouteMind
```

The road-network data can be exported as GeoJSON and used as supporting geographic data for routing.

---

## 🧮 Route Optimization

RouteMind uses **Google OR-Tools** as a classical optimization baseline for Vehicle Routing Problems (VRP).

### Optimization Flow

```text
Delivery Stops
      ↓
Distance / Travel Information
      ↓
OR-Tools VRP
      ↓
Constraint Validation
      ↓
Optimized Route
```

OR-Tools provides a strong classical baseline, while RouteMind focuses on adding adaptive re-planning capabilities.

---

## 🤖 AI Architecture

The project is designed around AI-assisted decision making for dynamic logistics operations.

### Main Components

* **Coordinator** — coordinates the routing workflow.
* **Planner** — creates the initial route plan.
* **Constraint Handler** — checks operational constraints.
* **Event Handler** — detects events such as failed deliveries or new pickups.
* **Re-planning Module** — updates the route after an event.
* **Validation Module** — checks whether the new route is feasible.
* **Explainability Module** — provides the reason for route changes.
* **Analytics Module** — evaluates route performance.

### AI Flow

```text
Event
  ↓
Event Detection
  ↓
Route Re-planning
  ↓
Constraint Validation
  ↓
Route Evaluation
  ↓
Supervisor Review
  ↓
Updated Route
```

---

## 🏗️ System Architecture

```text
                    ┌────────────────────┐
                    │   Delivery Data    │
                    └─────────┬──────────┘
                              ↓
                    ┌────────────────────┐
                    │ Route Optimization │
                    │     OR-Tools       │
                    └─────────┬──────────┘
                              ↓
                    ┌────────────────────┐
                    │ Constraint         │
                    │ Validation         │
                    └─────────┬──────────┘
                              ↓
                    ┌────────────────────┐
                    │ Optimized Route    │
                    └─────────┬──────────┘
                              ↓
                       Real-world Event
                              ↓
                    ┌────────────────────┐
                    │ AI Re-planning     │
                    └─────────┬──────────┘
                              ↓
                    ┌────────────────────┐
                    │ Updated Route      │
                    └────────────────────┘
```

---

## 📊 Route Optimization Pipeline

```text
Amazon Last Mile Dataset
          ↓
Delivery Stops & Packages
          ↓
Road / Distance Information
          ↓
Google OR-Tools
          ↓
Constraint Validation
          ↓
AI Evaluation
          ↓
Supervisor Approval
          ↓
Dispatch
          ↓
Analytics
```

---

## 🛠️ Technology Stack

| Layer        | Technology                 |
| ------------ | -------------------------- |
| Frontend     | Next.js, React, TypeScript |
| Backend      | FastAPI, Python            |
| AI           | Google Gemini / OpenRouter |
| Optimization | Google OR-Tools            |
| Maps         | OpenStreetMap / OSRM       |
| Database     | PostgreSQL                 |
| Cache        | Redis                      |
| Storage      | MinIO                      |
| Deployment   | Docker / NGINX             |

---

## 📂 Project Structure

```text
RouteMind/
│
├── backend/
├── frontend/
├── scripts/
├── docs/
├── tests/
├── datasets/
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

> Large datasets and secret API keys should not be committed to the repository.

---

## 📦 Dataset

The project uses the **Amazon Last Mile Routing Research Challenge dataset** as the primary routing-data source.

The dataset provides information related to historical delivery routes, stops, and packages that can be used for route optimization experiments.

For large datasets, download them separately and place them in the appropriate `datasets/` directory instead of committing large files directly to GitHub.

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/mansoorXcoder/routemind.git
cd routemind
```

### 2. Create a Python virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

**Windows:**

```bash
.venv\Scripts\activate
```

**Linux / macOS:**

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

```bash
cp .env.example .env
```

For Windows, you can also create `.env` manually from `.env.example`.

### 6. Start the backend

```bash
uvicorn backend.app.main:app --reload
```

---

## 🧪 Testing

The project includes a demo/testing script:

```bash
python scripts/run_demo.py
```

Use testing to verify the available API, routing, AI pipeline, and other implemented components.

---

## 📈 Evaluation Metrics

The solution can be evaluated using:

* Total route distance
* Total delivery time
* Number of completed deliveries
* Constraint violations
* Re-planning latency
* Route feasibility
* Route improvement compared with the baseline

The main objective is to demonstrate that adaptive re-planning can provide additional value over a fixed/classical routing approach.

---

## 🏆 Hackathon Value

RouteMind is designed around the following areas:

| Dimension              | Focus                                         |
| ---------------------- | --------------------------------------------- |
| Business Impact        | Reduce unnecessary travel and delivery delays |
| AI Innovation          | Adaptive AI-based re-planning                 |
| Technical Excellence   | VRP optimization and constraint handling      |
| Enterprise Integration | Logistics and fleet workflow integration      |
| User Experience        | Clear route updates and explanations          |
| Scalability & Cost     | Efficient routing and practical deployment    |
| Presentation           | Simple visualization of route changes         |

---

## 🔮 Future Scope

* Real-time traffic integration
* Advanced live vehicle tracking
* Mobile application
* Larger-scale fleet optimization
* More sophisticated AI agents
* Cloud deployment
* Kubernetes-based deployment
* Advanced predictive analytics

---

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Commit your changes.
5. Push the branch.
6. Open a Pull Request.

---

## 🏁 Built For

**Google AI Build 2026 Hackathon**

**Track:** Adaptive Route Optimization for the Supply Chain

---

## 👥 Team

**Sravani G • Keerthi Ch • P. SSS Aswini Reddy** **P. Mansoor Ali Khan**
> **RouteMind — Plan smarter. Adapt faster. Deliver better.**

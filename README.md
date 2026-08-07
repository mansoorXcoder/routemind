# RouteMind - AI-Powered Logistics Route Optimization Platform

RouteMind is an enterprise-grade route optimization and real-time fleet dispatch platform. By integrating **Google OR-Tools** classical constraints engines with a **Multi-Agent AI Coordination layer** (powered by Google Gemini/OpenRouter), RouteMind generates efficient, compliant routes and handles real-time events like traffic jams or vehicle breakdowns dynamically with human-in-the-loop supervisor approvals.

---

## 🏗️ System Architecture & Data Flow

RouteMind is structured as a Python FastAPI REST service integrated with a sleek, responsive Single Page Application (SPA) dispatcher dashboard.

```mermaid
graph TD
    A[Amazon ALMRRC Dataset] -->|Parsed by seed.py| B[(Local Database SQLite/Postgres)]
    B -->|FastAPI Endpoints| C[REST API Services]
    C -->|route_id| D[Coordinator Agent]
    D -->|Step 1: Classical VRP Solver| E[Google OR-Tools Solver]
    E -->|Optimized Route Stops Sequence| F[Multi-Agent Verification Pipeline]
    
    %% Multi-Agent Pipeline
    F -->|Step 2: AI Soft Constraints| G[ConstraintAgent]
    F -->|Step 3: Verification Auditing| H[ValidationAgent]
    F -->|Step 4: LLM Explanation| I[ExplainabilityAgent]
    
    G & H & I -->|Step 5: Consolidate Output| D
    D -->|Step 6: Optimization Record (Pending)| B
    C -->|Read Comparison Stats| J[Supervisor Dispatch UI]
    J -->|Action: Approve / Reject| C
    C -->|Commit sequence changes to DB| B
```

### Core Execution Pipeline
1. **Dispatcher Request**: The supervisor views a route on the frontend dashboard and clicks **"Run AI Planner"**.
2. **Batch Optimization (Planner)**: The `CoordinatorAgent` fetches stops and packages from the database, feeding them into the **OR-Tools Solver** to calculate the math-optimal sequence.
3. **Multi-Agent Evaluation**: 
   - **Constraint Agent** checks compliance rules (driver limits, Indian COD cash thresholds).
   - **Validation Agent** confirms the safety of the route loop and ensures it returns to the hub depot.
   - **Explainability Agent** uses LLMs to compare the proposed optimization vs. the original route, explaining cost and time benefits.
4. **Human-in-the-Loop Approval**: The results are stored in the database as a `Pending` optimization. The supervisor reviews the comparison in the UI and selects **"Approve & Dispatch"** to commit the new stops sequence to the database.

---

## ⚙️ Optimization Algorithms

### 1. Classical Vehicle Routing Problem (VRP)
We use **Google OR-Tools** (`ortools.constraint_solver`) to model and solve the routing sequence. It handles:
- **Capacity Constraints**: Ensures the total weight of packages assigned to stops does not exceed the vehicle load limit.
- **Time Windows**: Stop sequences are ordered to satisfy target package delivery start/end times.
- **Driver Hours Limit**: Prevents route durations from exceeding the driver's maximum shift length.

### 2. Distance & Travel Time Matrix
- **OSM Route fallback**: In production environments, OSRM can be plugged in to retrieve driving routes.
- **Haversine Speed Matrix (Fallback)**: When OSM services are offline, the engine utilizes a mathematical Haversine distance model (assuming average speeds of 40 km/h) to generate transition cost matrices between stop coordinates.

### 3. Dynamic Replanning Algorithm
When an event (traffic, breakdown, or road closure) occurs:
- The system splits the stops: past completed stops remain unchanged.
- The last completed stop is designated as a temporary starting depot.
- The OR-Tools VRP Solver executes optimization **only on the remaining unvisited stops** starting from that new location, minimizing schedule disruptions.

---

## 🤖 Multi-Agent AI Architecture

The system coordinates **8 specialized agents** constructed using prompt engineering templates and async JSON parsing adapters:
- **CoordinatorAgent**: Orchestrates pipeline stages and manages state.
- **PlannerAgent**: Combines OR-Tools logic and coordinates solver runs.
- **ConstraintAgent**: Evaluates soft constraints such as regulatory compliance and cash collection limits.
- **EventAgent**: Analyzes real-time telemetry updates to assess severity and traffic detours.
- **ReplanningAgent**: Isolates unvisited stops and recomputes partial VRP sequences.
- **ExplainabilityAgent**: Compares routes, calculates carbon offsets, and outputs readable explanations.
- **ValidationAgent**: Audits the route integrity for loops, hub returns, and sequence completeness.
- **AnalyticsAgent**: Aggregates savings data over time to render historical charts.

---

## 📂 Project Structure

```text
route-mind/
├── backend/
│   └── app/
│       ├── agents/             # Multi-Agent AI system components
│       ├── api/                # FastAPI routers (auth, tracking, optimization, etc.)
│       ├── core/               # Security, configurations, and Gemini adapters
│       ├── database/           # SQLite/Postgres sessions, seeds, and migrations
│       ├── models/             # SQLAlchemy schemas
│       ├── optimization/       # OR-Tools classical routing solver
│       └── main.py             # App entrypoint and static file handlers
├── frontend/
│   ├── index.html              # Sleek glassmorphic dark-theme SPA template
│   └── app.js                  # Frontend state, charts, and Leaflet map rendering
├── scripts/
│   └── run_demo.py             # End-to-end integration test runner
├── routemind.db                # SQLite database (auto-generated)
├── requirements.txt            # System dependency lock
└── README.md                   # Documentation index
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10+ (specifically configured for standard compilation on Windows/OS)
- Access to the internet (for Leaflet maps, Lucide icons, and Google Gemini API calls)

### 1. Create Virtual Environment
```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Setup Environment Variables
Copy `.env.example` to `.env` and fill in your details:
```powershell
copy .env.example .env
```
Ensure `GOOGLE_API_KEY` is set to your Gemini API token (if left as `dummy-gemini-key`, the system automatically defaults to robust local mock explanations without failing).

### 4. Seed the Database
Initialize and seed the database with login users and 10 Amazon Last Mile Routing Challenge routes:
```powershell
.\.venv\Scripts\python -m backend.app.database.seed
```

### 5. Run the Server
Launch the FastAPI uvicorn server:
```powershell
.\.venv\Scripts\uvicorn backend.app.main:app --reload
```

Open your browser and navigate to **`http://localhost:8000/`**. The dashboard will load immediately and log you in automatically using default supervisor credentials (`admin@routemind.ai`).

---

## 🧪 Running Verification Tests

To verify every REST endpoint, database transaction, WebSocket event, OR-Tools sequence, and AI agent pipeline, run the end-to-end automated script:
```powershell
.\.venv\Scripts\python scripts/run_demo.py
```
This spawns the uvicorn server, makes authentication requests, executes optimization runs, performs supervisor approvals, triggers traffic events, and prints a final validation report automatically.

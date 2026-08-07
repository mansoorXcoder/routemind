import time
import requests
import subprocess
import os
import signal
import sys

def main():
    print("==================================================")
    print("     ROUTEMIND SYSTEM END-TO-END DEMO TEST        ")
    print("==================================================")
    
    # 1. Start FastAPI server in the background
    print("\n[Step 1] Starting FastAPI uvicorn server...")
    cmd = [r".\.venv\Scripts\python", "-m", "uvicorn", "backend.app.main:app", "--port", "8000", "--host", "127.0.0.1"]
    
    # Start process and pipe to uvicorn.log
    log_file = open("uvicorn.log", "w", encoding="utf-8")
    proc = subprocess.Popen(
        cmd,
        cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
        stdout=log_file,
        stderr=log_file
    )
    
    # Wait for server to initialize
    print("Waiting 3 seconds for server to start...")
    time.sleep(3.0)
    
    # Verify if server is running
    try:
        health_res = requests.get("http://localhost:8000/api/v1/health", timeout=2.0)
        if health_res.status_code == 200:
            print("FastAPI Server is UP and healthy!")
            print(health_res.json())
        else:
            print(f"Server health check failed: {health_res.status_code}")
            proc.terminate()
            sys.exit(1)
    except Exception as e:
        print(f"Failed to connect to local server: {e}")
        proc.terminate()
        sys.exit(1)
        
    base_url = "http://localhost:8000/api/v1"
    token = None
    
    try:
        # 2. Login to receive JWT Token
        print("\n[Step 2] Logging in as Supervisor...")
        login_payload = {
            "email": "admin@routemind.ai",
            "password": "admin123"
        }
        res = requests.post(f"{base_url}/auth/login", json=login_payload)
        res_data = res.json()
        token = res_data["access_token"]
        print(f"Login successful! JWT Token: {token[:20]}...")
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # 3. Retrieve Dashboard summary KPIs
        print("\n[Step 3] Loading Dashboard KPI Summary...")
        res = requests.get(f"{base_url}/dashboard/summary", headers=headers)
        try:
            print("Summary KPIs:", res.json())
        except Exception as json_err:
            print(f"Failed to parse JSON. Status code: {res.status_code}")
            print(f"Response text: {res.text}")
            raise json_err
        
        # 4. Get active routes list
        print("\n[Step 4] Querying active routes list...")
        res = requests.get(f"{base_url}/routes", headers=headers)
        routes = res.json()
        print(f"Found {len(routes)} active routes.")
        for r in routes[:2]:
            print(f"- Route Code: {r['route_code']}, Status: {r['status']}, Distance: {r['planned_distance']:.1f} km")
            
        target_route = routes[0]
        route_id = target_route["id"]
        
        # 5. Run AI Planner Optimization
        print(f"\n[Step 5] Running AI Planner for route {target_route['route_code']}...")
        res = requests.post(f"{base_url}/optimization/run", json={"route_id": route_id}, headers=headers)
        opt_data = res.json()
        print("Planner results received!")
        print(f"AI Confidence: {opt_data['explanation']['confidence_score']}%")
        print(f"Explanation Rationale: {opt_data['explanation']['explanation']}")
        print(f"Time saved: {opt_data['explanation']['benefits']['time_saved_min']:.1f} minutes")
        print(f"Distance saved: {opt_data['explanation']['benefits']['distance_saved_km']:.1f} km")
        print(f"Optimization ID: {opt_data['optimization_id']}")
        
        # 6. Approve the plan
        print("\n[Step 6] Supervisor Approving the route changes...")
        res = requests.post(
            f"{base_url}/optimization/approve", 
            json={"optimization_id": opt_data["optimization_id"]}, 
            headers=headers
        )
        print("Approval response:", res.json())
        
        # 7. Check updated stops sequence
        print("\n[Step 7] Verifying stops sequences are updated in database...")
        res = requests.get(f"{base_url}/routes/{route_id}/stops", headers=headers)
        stops = res.json()
        print(f"Stops sequence list after approval:")
        for s in stops[:5]:
            print(f"- Stop: {s['customer_name']}, Sequence Order: {s['sequence']}")
            
        # 8. Simulate Event & Replan
        print("\n[Step 8] Triggering dynamic replan due to simulated Traffic congestion...")
        replan_payload = {
            "route_id": route_id,
            "event_type": "traffic",
            "event_details": {
                "location": "Route Corridor Links",
                "severity": "high",
                "speed_limit_kmh": 4.5
            },
            "current_stop_index": 2
        }
        res = requests.post(f"{base_url}/optimization/replan", json=replan_payload, headers=headers)
        replan_data = res.json()
        print("Replanning results received!")
        print(f"Event Priority: {replan_data['event_analysis']['priority']}")
        print(f"AI Explanation on Traffic Replan: {replan_data['explanation']['explanation']}")
        print(f"Replan Optimization ID: {replan_data['optimization_id']}")
        
        # 9. Approve the replanned route
        print("\n[Step 9] Supervisor Approving the traffic replanned route...")
        res = requests.post(
            f"{base_url}/optimization/approve", 
            json={"optimization_id": replan_data["optimization_id"]}, 
            headers=headers
        )
        print("Replan approval response:", res.json())
        
    except Exception as e:
        print(f"Error during API demo execution: {e}")
        
    finally:
        # 10. Terminate background server process cleanly
        print("\n[Step 10] Terminating background server...")
        proc.terminate()
        try:
            proc.wait(timeout=3.0)
            print("FastAPI Server terminated cleanly.")
        except subprocess.TimeoutExpired:
            print("Forcing server termination...")
            proc.kill()
            print("Server process killed.")
            
    print("\nDemo verification tests completed successfully.")

if __name__ == "__main__":
    main()

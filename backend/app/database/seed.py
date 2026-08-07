import json
import os
import asyncio
import logging
import random
from datetime import datetime, date, timezone
from sqlalchemy.future import select
from backend.app.database.session import SessionLocal, engine
from backend.app.models import User, Hub, Driver, Vehicle, Route, Stop, Package
from backend.app.core.security import hash_password

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("seed")

DATA_DIR = r"p:\Documents\Git\route-mind\almrrc2021\almrrc2021-data-training\model_build_inputs"

async def seed_data():
    logger.info("Starting database seeding...")
    
    # Ensure tables are created
    from backend.app.database.base import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    async with SessionLocal() as db:
        # 1. Create Default Users
        logger.info("Creating default users...")
        users = [
            User(
                name="System Administrator",
                email="admin@routemind.ai",
                password_hash=hash_password("admin123"),
                role="Admin",
                phone="+919876543210",
                status="active"
            ),
            User(
                name="Supervisor Mansoor",
                email="supervisor@routemind.ai",
                password_hash=hash_password("supervisor123"),
                role="Supervisor",
                phone="+919876543211",
                status="active"
            ),
            User(
                name="Dispatcher Rahul",
                email="dispatcher@routemind.ai",
                password_hash=hash_password("dispatcher123"),
                role="Dispatcher",
                phone="+919876543212",
                status="active"
            ),
            User(
                name="Driver Kumar",
                email="driver@routemind.ai",
                password_hash=hash_password("driver123"),
                role="Driver",
                phone="+919876543213",
                status="active"
            )
        ]
        
        for u in users:
            # Check if user already exists
            result = await db.execute(select(User).filter_by(email=u.email))
            if not result.scalars().first():
                db.add(u)
        
        # 2. Parse Amazon Dataset
        logger.info("Reading Amazon dataset files...")
        route_data_path = os.path.join(DATA_DIR, "route_data.json")
        package_data_path = os.path.join(DATA_DIR, "package_data.json")
        travel_times_path = os.path.join(DATA_DIR, "travel_times.json")
        actual_sequences_path = os.path.join(DATA_DIR, "actual_sequences.json")
        
        if not all(os.path.exists(p) for p in [route_data_path, package_data_path, travel_times_path, actual_sequences_path]):
            logger.error("Amazon Last Mile dataset files not found. Please verify the dataset path.")
            return

        with open(route_data_path, 'r') as f:
            route_data = json.load(f)
        with open(package_data_path, 'r') as f:
            package_data = json.load(f)
        with open(actual_sequences_path, 'r') as f:
            actual_sequences = json.load(f)
            
        logger.info("Dataset files loaded successfully. Seeding hubs, vehicles, drivers, routes, stops, and packages...")
        
        # Select first 10 routes to seed
        route_ids = list(route_data.keys())[:10]
        
        # Keep track of inserted packages to avoid duplicate key errors
        inserted_package_ids = set()
        
        for idx, r_id in enumerate(route_ids):
            r_info = route_data[r_id]
            p_info = package_data.get(r_id, {})
            seq_info = actual_sequences.get(r_id, {}).get("actual", {})
            
            # Hub creation or retrieval
            station_code = r_info["station_code"]
            # Find the Station stop in this route
            station_stop_id = None
            station_lat, station_lng = 0.0, 0.0
            for stop_id, stop_info in r_info["stops"].items():
                if stop_info["type"] == "Station":
                    station_stop_id = stop_id
                    station_lat = stop_info["lat"]
                    station_lng = stop_info["lng"]
                    break
            
            if not station_stop_id:
                # If no explicit station, use first stop as dummy station
                first_stop_id = list(r_info["stops"].keys())[0]
                station_lat = r_info["stops"][first_stop_id]["lat"]
                station_lng = r_info["stops"][first_stop_id]["lng"]
                station_stop_id = first_stop_id
                
            # Create Hub if not exists
            result = await db.execute(select(Hub).filter_by(name=station_code))
            hub = result.scalars().first()
            if not hub:
                hub = Hub(
                    name=station_code,
                    city="Hub City",
                    latitude=station_lat,
                    longitude=station_lng,
                    address=f"Hub Depot {station_code}",
                    capacity=100
                )
                db.add(hub)
                await db.flush()
                
            # Create Vehicle
            v_num = f"KA-01-E-{random.randint(1000, 9999)}"
            result = await db.execute(select(Vehicle).filter_by(vehicle_number=v_num))
            vehicle = result.scalars().first()
            if not vehicle:
                # Convert capacity in cm3 to kg (approx factor, e.g., 1000 cm3 = 1 liter, 1 liter capacity = 0.25 kg load limit or similar)
                cap_cm3 = r_info.get("executor_capacity_cm3", 3000000.0)
                capacity_kg = float(cap_cm3) / 10000.0  # e.g., 3,000,000 cm3 = 300 kg capacity
                vehicle = Vehicle(
                    vehicle_number=v_num,
                    vehicle_type="Truck" if capacity_kg > 200 else "Van",
                    capacity=capacity_kg,
                    fuel_type="CNG" if idx % 2 == 0 else "Diesel",
                    status="idle",
                    current_latitude=station_lat,
                    current_longitude=station_lng,
                    hub_id=hub.id
                )
                db.add(vehicle)
                await db.flush()
                
            # Create Driver
            d_emp_id = f"EMP-{random.randint(10000, 99999)}"
            result = await db.execute(select(Driver).filter_by(employee_id=d_emp_id))
            driver = result.scalars().first()
            if not driver:
                driver = Driver(
                    employee_id=d_emp_id,
                    name=f"Driver Name {idx}",
                    phone=f"+9199999{random.randint(10000, 99999)}",
                    license_number=f"DL-{random.randint(1000000, 9999999)}",
                    experience=random.randint(2, 15),
                    rating=round(random.uniform(4.0, 5.0), 1),
                    status="idle",
                    hub_id=hub.id,
                    current_vehicle=vehicle.vehicle_number
                )
                db.add(driver)
                await db.flush()
                
            # Create Route
            route_code = f"ROUTE-{r_id.split('_')[1][:8]}"
            result = await db.execute(select(Route).filter_by(route_code=route_code))
            route_obj = result.scalars().first()
            if not route_obj:
                route_obj = Route(
                    route_code=route_code,
                    vehicle_id=vehicle.id,
                    driver_id=driver.id,
                    hub_id=hub.id,
                    date=date.today(),
                    status="planned",
                    planned_distance=random.uniform(20.0, 80.0),
                    planned_duration=random.uniform(120.0, 360.0),
                    optimization_score=95.0
                )
                db.add(route_obj)
                await db.flush()
                
            # Create Stops and Packages
            logger.info(f"Adding stops and packages for route: {route_code}...")
            
            # Sort stops based on actual sequences (if available) or randomly
            stops_to_create = list(r_info["stops"].items())
            if seq_info:
                # Sort stops based on sequence number
                # Map stop_id to sequence order, default to high value if not present
                stops_to_create.sort(key=lambda item: seq_info.get(item[0], 9999))
                
            for seq_num, (stop_id, stop_details) in enumerate(stops_to_create):
                is_hub = stop_details["type"] == "Station"
                stop_obj = Stop(
                    route_id=route_obj.id,
                    sequence=seq_num,
                    customer_name=f"Hub Depot" if is_hub else f"Customer Stop {stop_id}",
                    address=f"Depot Station {stop_id}" if is_hub else f"Delivery Street, Zone {stop_details.get('zone_id', 'N/A')}",
                    latitude=stop_details["lat"],
                    longitude=stop_details["lng"],
                    stop_type="hub" if is_hub else "delivery",
                    status="pending",
                )
                db.add(stop_obj)
                await db.flush()
                
                # Add packages for this stop
                stop_packages = p_info.get(stop_id, {})
                for pkg_id, pkg_details in stop_packages.items():
                    if pkg_id in inserted_package_ids:
                        continue
                    inserted_package_ids.add(pkg_id)
                    
                    # Calculate weight & volume
                    dims = pkg_details.get("dimensions", {})
                    d = dims.get("depth_cm", 10.0)
                    h = dims.get("height_cm", 10.0)
                    w = dims.get("width_cm", 10.0)
                    volume_m3 = (d * h * w) / 1000000.0  # cm3 to m3
                    weight_kg = volume_m3 * 150.0  # approx density 150kg/m3
                    
                    package_obj = Package(
                        tracking_number=pkg_id,
                        route_id=route_obj.id,
                        stop_id=stop_obj.id,
                        weight=max(round(weight_kg, 2), 0.1),
                        volume=max(round(volume_m3, 4), 0.001),
                        cod_amount=float(random.choice([0, 0, 0, 500, 1500, 2500])),  # Random COD
                        status="pending",
                        delivery_type=random.choice(["standard", "standard", "express"])
                    )
                    db.add(package_obj)
            
            # Commit after each route
            await db.commit()
            
    logger.info("Database seeding completed successfully.")

if __name__ == "__main__":
    asyncio.run(seed_data())

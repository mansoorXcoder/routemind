# RouteMind Database Design

Version: 1.0

Status: Draft

Database

PostgreSQL 17

Cache

Redis

Storage

Amazon S3 / MinIO

ORM

SQLAlchemy

Migration

Alembic

---

# Database Overview

The RouteMind database stores

• Users
• Drivers
• Vehicles
• Routes
• Stops
• Packages
• AI Optimizations
• Notifications
• Analytics
• Route History

The database is designed for

- High Read Performance
- Fast Route Queries
- AI Explainability
- Route Versioning
- Scalability

---

# Database Architecture

Frontend

↓

FastAPI Backend

↓

SQLAlchemy ORM

↓

PostgreSQL

↓

Redis Cache

↓

Object Storage

---

# Entity Relationship

Users

↓

Drivers

↓

Vehicles

↓

Routes

↓

Stops

↓

Packages

↓

Optimizations

↓

Notifications

↓

Analytics

---

# Tables

## users

Purpose

Store authenticated users.

Columns

id UUID PK

name

email

password_hash

role

phone

status

created_at

updated_at

Indexes

email

role

---

## drivers

Columns

id UUID PK

employee_id

name

phone

license_number

experience

rating

current_vehicle

status

hub_id

created_at

updated_at

Indexes

status

employee_id

---

## vehicles

Columns

id UUID PK

vehicle_number

vehicle_type

capacity

fuel_type

current_driver

status

current_location

hub_id

created_at

Indexes

status

vehicle_number

---

## hubs

Columns

id UUID PK

name

city

latitude

longitude

address

capacity

---

## routes

Columns

id UUID PK

route_code

vehicle_id

driver_id

hub_id

date

status

planned_distance

actual_distance

planned_duration

actual_duration

optimization_score

created_at

updated_at

Indexes

driver_id

vehicle_id

status

date

---

## stops

Columns

id UUID PK

route_id

sequence

customer_name

address

latitude

longitude

stop_type

delivery_window_start

delivery_window_end

status

arrival_time

departure_time

Indexes

route_id

sequence

---

## packages

Columns

id UUID PK

tracking_number

route_id

stop_id

weight

volume

cod_amount

status

delivery_type

created_at

Indexes

tracking_number

status

---

## optimizations

Purpose

Store every optimization.

Columns

id UUID PK

route_id

optimization_type

algorithm

old_route

new_route

distance_saved

time_saved

fuel_saved

carbon_saved

confidence

reason

created_at

Indexes

route_id

algorithm

---

## route_history

Purpose

Track every change.

Columns

id UUID PK

route_id

version

modified_by

change_reason

old_data

new_data

created_at

---

## notifications

Columns

id UUID PK

user_id

title

message

type

priority

is_read

created_at

Indexes

user_id

---

## analytics

Columns

id UUID PK

date

routes_completed

packages_delivered

fuel_used

fuel_saved

distance

delay

optimization_score

---

## ai_decisions

Columns

id UUID PK

route_id

decision

confidence

reason

llm_model

execution_time

cost

approved

created_at

---

## traffic_events

Columns

id UUID PK

location

severity

description

start_time

end_time

source

---

## weather_events

Columns

id UUID PK

city

temperature

condition

risk_level

timestamp

---

# Relationships

User

1:N Notifications

Driver

1:N Routes

Vehicle

1:N Routes

Route

1:N Stops

Route

1:N Packages

Route

1:N Optimizations

Route

1:N Route History

Stop

1:N Packages

Hub

1:N Vehicles

Hub

1:N Drivers

Hub

1:N Routes

---

# Constraints

Vehicle Capacity

Must not exceed capacity.

COD Limit

Cannot exceed configured amount.

Delivery Window

Arrival must be within time window.

Driver Hours

Maximum legal driving hours.

Hub Assignment

Vehicle must belong to hub.

---

# Redis Cache

Cache

Dashboard Summary

Vehicle Locations

Traffic Data

Weather

Recent Routes

AI Suggestions

TTL

30 seconds

Live Tracking

5 seconds

---

# Object Storage

Store

Exported Reports

CSV Files

Images

Driver Photos

Logs

Optimization Reports

Architecture Diagrams

---

# Audit Logging

Track

Login

Logout

Optimization

Route Approval

Driver Assignment

Vehicle Assignment

Settings Update

---

# Index Strategy

Unique

email

tracking_number

vehicle_number

employee_id

Composite

route_id + sequence

driver_id + status

vehicle_id + date

status + created_at

---

# Backup Strategy

Daily Backup

Incremental Backup

Point-In-Time Recovery

30 Days Retention

---

# Security

Encrypted Passwords

JWT

Role Based Access

Audit Logs

Row Level Permissions

HTTPS Only

---

# Roles

Admin

Supervisor

Dispatcher

Driver

Viewer

---

# Database Performance

Connection Pooling

Query Optimization

Indexes

Partition Analytics

Read Replicas

Redis Cache

---

# Estimated Scale

Drivers

100,000+

Vehicles

50,000+

Routes

5 Million+

Stops

100 Million+

Packages

500 Million+

Optimizations

50 Million+

---

# Future Tables

customer_feedback

maintenance

fuel_logs

driver_attendance

route_templates

traffic_predictions

weather_predictions

digital_twin

iot_devices

telemetry

carbon_reports

fleet_health

---

# Database Flow

Amazon Dataset

↓

Data Import Service

↓

PostgreSQL

↓

Route Optimizer

↓

AI Decision Engine

↓

Supervisor Approval

↓

Route History

↓

Analytics

↓

Dashboard

---

# Technology

PostgreSQL

Redis

SQLAlchemy

Alembic

MinIO

FastAPI

Pydantic

Docker

---

# Future Enhancements

PostGIS

TimescaleDB

Kafka

MongoDB

Neo4j

Vector Database

Event Sourcing

CQRS
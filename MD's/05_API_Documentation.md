# RouteMind API Documentation

Version: 1.0

Status: Draft

Base URL

/api/v1

Protocol

HTTPS

Authentication

JWT Bearer Token

Content-Type

application/json

---

# API Categories

Authentication

Dashboard

Routes

Optimization

Vehicles

Drivers

Live Tracking

Analytics

Notifications

Settings

AI

Health

---

# Authentication APIs

## Login

POST /auth/login

Purpose

Authenticate user.

Request

{
  "email": "",
  "password": ""
}

Response

{
  "access_token": "",
  "refresh_token": "",
  "user": {}
}

---

## Refresh Token

POST /auth/refresh

---

## Logout

POST /auth/logout

---

## Current User

GET /auth/me

---

# Dashboard APIs

## Dashboard Summary

GET /dashboard/summary

Returns

- Total Routes
- Active Vehicles
- Drivers
- Deliveries
- Fuel Saved
- Optimization Score

---

## Recent Activity

GET /dashboard/activity

---

## KPI Statistics

GET /dashboard/kpi

---

## Alerts

GET /dashboard/alerts

---

# Route APIs

## Get All Routes

GET /routes

Filters

status

city

driver

vehicle

date

---

## Get Route

GET /routes/{route_id}

---

## Create Route

POST /routes

---

## Update Route

PUT /routes/{route_id}

---

## Delete Route

DELETE /routes/{route_id}

---

## Route Stops

GET /routes/{route_id}/stops

---

## Route Timeline

GET /routes/{route_id}/timeline

---

## Route History

GET /routes/{route_id}/history

---

# Route Optimization APIs

## Optimize Route

POST /optimization/run

Request

{
   "route_id":"",
   "constraints":[]
}

Response

{
   "optimized_route":{},
   "score":96
}

---

## Replan Route

POST /optimization/replan

Triggered By

Traffic

New Pickup

Failed Delivery

Vehicle Breakdown

Weather

---

## Compare Routes

GET /optimization/compare/{route_id}

Returns

Old Route

New Route

Time Saved

Fuel Saved

Distance Saved

---

# AI APIs

## Explain Optimization

GET /ai/explain/{route_id}

Returns

Reason

Confidence

Affected Stops

Expected Savings

---

## AI Suggestions

GET /ai/suggestions

---

## AI Decision History

GET /ai/history

---

## AI Confidence Score

GET /ai/confidence/{route_id}

---

# Live Tracking APIs

## Live Vehicles

GET /tracking/vehicles

---

## Vehicle Position

GET /tracking/vehicle/{vehicle_id}

---

## Vehicle History

GET /tracking/history/{vehicle_id}

---

## Route Progress

GET /tracking/progress/{route_id}

---

# Vehicle APIs

## Get Vehicles

GET /vehicles

---

## Vehicle Details

GET /vehicles/{vehicle_id}

---

## Create Vehicle

POST /vehicles

---

## Update Vehicle

PUT /vehicles/{vehicle_id}

---

## Delete Vehicle

DELETE /vehicles/{vehicle_id}

---

## Assign Route

POST /vehicles/{vehicle_id}/assign

---

# Driver APIs

## Get Drivers

GET /drivers

---

## Driver Details

GET /drivers/{driver_id}

---

## Create Driver

POST /drivers

---

## Update Driver

PUT /drivers/{driver_id}

---

## Driver Performance

GET /drivers/{driver_id}/performance

---

## Driver History

GET /drivers/{driver_id}/history

---

# Analytics APIs

## Delivery Analytics

GET /analytics/deliveries

---

## Driver Analytics

GET /analytics/drivers

---

## Route Analytics

GET /analytics/routes

---

## Fuel Analytics

GET /analytics/fuel

---

## Vehicle Analytics

GET /analytics/vehicles

---

## Optimization Analytics

GET /analytics/optimization

---

# Notification APIs

GET /notifications

PUT /notifications/read

DELETE /notifications/{id}

POST /notifications/send

---

# Settings APIs

GET /settings

PUT /settings

---

# Health APIs

GET /health

Returns

Status

Version

Database

Redis

AI

OR-Tools

OSM

---

# WebSocket APIs

/ws/live

Events

vehicle.updated

route.updated

driver.updated

notification.new

optimization.finished

traffic.updated

weather.updated

---

# Standard Response

Success

{
   "success":true,
   "data":{}
}

---

Failure

{
   "success":false,
   "message":"",
   "error":""
}

---

# HTTP Status Codes

200 OK

201 Created

204 Deleted

400 Bad Request

401 Unauthorized

403 Forbidden

404 Not Found

409 Conflict

422 Validation Error

429 Rate Limited

500 Internal Server Error

503 Service Unavailable

---

# Security

JWT Authentication

HTTPS Only

Rate Limiting

Request Validation

Input Sanitization

Role-Based Access Control

Audit Logging

---

# API Versioning

/api/v1

Future

/api/v2

---

# Rate Limits

Authenticated

1000 requests/hour

Guest

100 requests/hour

Optimization APIs

30 requests/hour

AI APIs

100 requests/hour

---

# API Documentation

Swagger/OpenAPI

ReDoc

Postman Collection

OpenAPI 3.1 Specification

---

# Future APIs

Traffic Service

Weather Service

SMS

Email

Push Notifications

IoT Devices

Fleet Sensors

Digital Twin

External TMS Integration

Amazon Logistics Integration

Google Maps Integration
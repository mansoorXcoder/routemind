# RouteMind System Architecture

Version: 1.0

Status

Production Ready Architecture

---

# Purpose

This document defines the complete architecture of RouteMind.

It explains

• System Components
• Data Flow
• Backend Services
• AI Architecture
• Database
• External Services
• Deployment
• Security
• Communication

---

# Architecture Goals

Scalable

Modular

Cloud Native

AI First

Fast

Explainable

Fault Tolerant

Easy Deployment

---

# High Level Architecture

                    ┌──────────────────────────────┐
                    │        Web Dashboard          │
                    │      Next.js + React          │
                    └──────────────┬───────────────┘
                                   │
                          HTTPS / REST API
                                   │
                    ┌──────────────▼───────────────┐
                    │         FastAPI API          │
                    │      Authentication          │
                    │      Business Logic          │
                    └──────────────┬───────────────┘
                                   │
         ┌─────────────────────────┼───────────────────────────┐
         │                         │                           │
         ▼                         ▼                           ▼
  Route Service            AI Service                 Tracking Service
         │                         │                           │
         ▼                         ▼                           ▼
 OR-Tools Engine         Multi-Agent AI              Live Updates
         │                         │                           │
         └──────────────┬──────────┴───────────────┐
                        ▼                          ▼
                  PostgreSQL                  Redis Cache
                        │                          │
                        └──────────────┬───────────┘
                                       ▼
                              Object Storage
                                  (Reports)

---

# Layer Architecture

Presentation Layer

↓

API Layer

↓

Business Layer

↓

AI Layer

↓

Optimization Layer

↓

Data Layer

↓

Infrastructure Layer

---

# Frontend Layer

Technology

Next.js

React

TypeScript

TailwindCSS

Shadcn UI

MapLibre

Responsibilities

Dashboard

Maps

Analytics

Supervisor Panel

Driver Panel

Notifications

Settings

---

# API Layer

Technology

FastAPI

Responsibilities

Authentication

Routing

Validation

API Versioning

Rate Limiting

Response Formatting

Swagger

---

# Business Layer

Modules

Route Management

Vehicle Management

Driver Management

Package Management

Notification Management

Analytics

Approval Workflow

---

# AI Layer

Coordinator Agent

Planner Agent

Constraint Agent

Event Agent

Replanning Agent

Validation Agent

Explainability Agent

Analytics Agent

---

# Optimization Layer

OR-Tools

Distance Matrix

Constraint Solver

Route Sequencing

Cost Optimization

Vehicle Assignment

---

# Data Layer

PostgreSQL

Redis

Object Storage

Logs

Analytics

Route History

---

# Infrastructure Layer

Docker

Docker Compose

NGINX

Ubuntu

GitHub Actions

AWS EC2

Future

Kubernetes

---

# Request Flow

User

↓

Frontend

↓

REST API

↓

Business Service

↓

OR-Tools

↓

AI Agents

↓

Validation

↓

Database

↓

Frontend

---

# Route Optimization Flow

Import Stops

↓

Validate Data

↓

Generate Distance Matrix

↓

OR-Tools Optimization

↓

Constraint Checking

↓

AI Analysis

↓

Explanation

↓

Supervisor Approval

↓

Driver Dispatch

---

# Replanning Flow

Traffic

OR

New Pickup

OR

Failed Delivery

↓

Event Agent

↓

Planner

↓

Constraint Agent

↓

Validation

↓

Explainability

↓

Approval

↓

Notification

---

# Authentication Flow

Login

↓

JWT

↓

Refresh Token

↓

Protected API

↓

Role Validation

↓

Response

---

# Data Flow

Amazon Dataset

↓

Importer

↓

Database

↓

Route Service

↓

OR-Tools

↓

AI Layer

↓

Dashboard

---

# Communication

Frontend

↓

REST

↓

Backend

↓

Internal Services

↓

Database

↓

Redis

↓

Response

---

# Live Tracking Flow

Driver

↓

GPS

↓

Tracking API

↓

Redis

↓

WebSocket

↓

Dashboard

---

# Notification Flow

Event

↓

Notification Service

↓

Database

↓

WebSocket

↓

Frontend

---

# AI Workflow

Planner

↓

Constraint

↓

Validation

↓

Explainability

↓

Supervisor

↓

Analytics

---

# Component Diagram

Frontend

Dashboard

Maps

Analytics

Settings

↓

Backend

Authentication

Routes

Drivers

Vehicles

Optimization

AI

↓

Database

Users

Routes

Stops

Drivers

Vehicles

Optimizations

Notifications

Analytics

---

# Sequence Diagram

Supervisor

↓

Dashboard

↓

API

↓

Optimization Service

↓

OR-Tools

↓

AI

↓

Validation

↓

Database

↓

Dashboard

---

# External Integrations

Amazon Dataset

OpenStreetMap

Overpass API

Gemini API

Future

Weather API

Traffic API

Fleet Management

---

# Caching Strategy

Redis

Vehicle Locations

Traffic

Dashboard

Analytics

Recent Routes

AI Results

TTL

5 seconds

30 seconds

5 minutes

---

# Logging

API Logs

AI Logs

Optimization Logs

Security Logs

Audit Logs

Performance Logs

---

# Monitoring

Health Endpoint

CPU

RAM

Latency

Database

Redis

AI

OR-Tools

---

# Error Handling

Retry

Fallback

Cached Routes

Graceful Failure

Logging

Notification

---

# Security

HTTPS

JWT

RBAC

Input Validation

Output Validation

Audit Logging

Rate Limiting

Encryption

---

# Scalability

Horizontal API Scaling

Redis

Database Indexing

Worker Queue

Async Processing

Future

Kubernetes

Auto Scaling

---

# Deployment Architecture

                 Internet
                     │
               NGINX Reverse Proxy
                     │
          ┌──────────┴──────────┐
          │                     │
      Frontend             FastAPI Backend
                                  │
          ┌──────────────┬────────┴──────────────┐
          │              │                       │
     OR-Tools        AI Services           WebSocket
          │              │                       │
          └──────────────┼───────────────────────┘
                         ▼
                    PostgreSQL
                         │
                    Redis Cache
                         │
                    Object Storage

---

# Folder Communication

Frontend

↓

API

↓

Services

↓

Repositories

↓

Database

---

# Performance Targets

Dashboard

<2 seconds

Route Optimization

<10 seconds

Replanning

<5 seconds

AI Explanation

<2 seconds

Notification

<1 second

API Response

<300ms

---

# Availability

99.9%

---

# Technology Stack

Frontend

Next.js

React

TailwindCSS

Shadcn UI

MapLibre

Backend

FastAPI

Python

Pydantic

SQLAlchemy

AI

Gemini

OR-Tools

LangGraph (Future)

CrewAI (Optional)

Database

PostgreSQL

Redis

Storage

MinIO

Deployment

Docker

NGINX

GitHub Actions

AWS EC2

---

# Future Architecture

Microservices

Kafka

Kubernetes

PostGIS

TimescaleDB

Digital Twin

IoT Sensors

Traffic Prediction

Weather Prediction

Carbon Optimization

---

# Final System Pipeline

Amazon Dataset
      │
      ▼
Data Import Service
      │
      ▼
PostgreSQL
      │
      ▼
Route Service
      │
      ▼
OR-Tools Optimizer
      │
      ▼
Multi-Agent AI Layer
      │
      ▼
Validation
      │
      ▼
Supervisor Dashboard
      │
      ▼
Driver Notification
      │
      ▼
Analytics Dashboard

---

# Architecture Principles

✔ Modular

✔ Explainable

✔ AI Assisted

✔ Cloud Ready

✔ Enterprise Grade

✔ Highly Scalable

✔ Fault Tolerant

✔ Easy to Maintain
# RouteMind AI Agent Architecture

Version: 1.0

Status

Draft

---

# Purpose

RouteMind uses a Multi-Agent AI Architecture.

Instead of one large LLM handling everything,
multiple specialized AI agents cooperate to
produce intelligent, explainable and cost-efficient
route optimization.

Each agent owns exactly one responsibility.

---

# AI Principles

Small Specialized Agents

Fast Decision Making

Explainable Outputs

Low Cost

Human Approval

Self Verification

OR-Tools First

AI Only When Needed

---

# High-Level Workflow

Amazon Dataset

↓

Data Loader

↓

Constraint Engine

↓

OR-Tools Optimizer

↓

AI Decision Layer

↓

Specialized AI Agents

↓

Supervisor Approval

↓

Driver Notification

↓

Analytics

---

# Agent Architecture

                    Coordinator Agent
                           │
      ┌───────────┬─────────┴──────────┬────────────┐
      │           │                    │            │
Planner      Constraint Agent     Event Agent   Explain Agent
      │                │                │            │
      └───────────┬────┴───────┬────────┘
                  │
          Replanning Agent
                  │
         Validation Agent
                  │
        Supervisor Approval
                  │
          Driver Notification

---

# 1 Coordinator Agent

Purpose

Acts as the brain.

Responsibilities

Receive optimization request

Assign work

Collect outputs

Merge decisions

Generate workflow

Return final response

Input

Optimization request

Output

Agent execution plan

---

# 2 Planner Agent

Purpose

Generate initial optimized route.

Uses

OR-Tools

OpenStreetMap

Distance Matrix

Vehicle Capacity

Objectives

Shortest Distance

Lowest Time

Minimum Fuel

Balanced Load

Output

Optimized Route

Estimated Time

Estimated Cost

Optimization Score

---

# 3 Constraint Agent

Purpose

Validate business rules.

Checks

Vehicle Capacity

Delivery Windows

COD Limits

Working Hours

Hub Assignment

Indian Zone Rules

Low Bridge Restrictions

Restricted Roads

Output

Constraint Report

Violations

Recommendations

---

# 4 Event Detection Agent

Purpose

Monitor changes.

Events

Traffic

Failed Delivery

New Pickup

Road Closure

Vehicle Breakdown

Weather

Delayed Driver

Output

Detected Event

Priority

Impact Score

---

# 5 Replanning Agent

Purpose

Recalculate only affected route sections.

Input

Current Route

Detected Event

Constraints

Output

Updated Route

Changed Stops

New ETA

Savings

---

# 6 Explainability Agent

Purpose

Explain every optimization.

Questions

Why changed?

Why skipped stop?

Why new sequence?

Why delay?

Output

Natural Language Explanation

Confidence Score

Affected Stops

Benefits

---

# 7 Validation Agent

Purpose

Self-check system output.

Verifies

Constraints

Duplicate Stops

Distance

ETA

Packages

Capacity

Optimization Quality

Output

PASS

WARNING

FAIL

---

# 8 Supervisor Agent

Purpose

Human approval layer.

Responsibilities

Review explanation

Approve

Reject

Request changes

Add comments

Output

Approval Status

---

# 9 Driver Notification Agent

Purpose

Notify drivers.

Sends

Updated Route

ETA

New Stops

Warnings

Navigation Link

Offline Route Cache

---

# 10 Analytics Agent

Purpose

Collect metrics.

Measures

Optimization Score

Fuel Saved

Time Saved

Distance Saved

Rejected Plans

Approval Rate

Driver Performance

---

# Agent Communication

Coordinator

↓

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

Driver

↓

Analytics

---

# Agent Inputs

Planner

Route

Vehicle

Packages

OSM

Constraint

Business Rules

Planner Output

Vehicle

Driver

Event

Traffic

Weather

Pickup

Failure

Explain

Old Route

New Route

Savings

Validation

Everything

---

# Agent Outputs

Planner

Optimized Route

Constraint

Validation Report

Event

Event Object

Replanning

Updated Route

Explain

Natural Language Summary

Validation

PASS

Supervisor

Approved Route

Analytics

Performance Metrics

---

# AI Models

Routine Decisions

Gemini Flash Lite

Reasoning

Gemini Flash

Future

Gemma

Llama

Qwen

---

# AI Cost Strategy

Normal Routes

OR-Tools Only

Minor Changes

Small Model

Major Changes

LLM

Explanation

Small Model

Validation

Small Model

---

# Memory

Session Memory

Recent Optimizations

Recent Traffic

Route History

Constraint Cache

---

# Prompt Templates

Planner Prompt

Explain Prompt

Validation Prompt

Traffic Prompt

Weather Prompt

Replanning Prompt

Supervisor Prompt

---

# Confidence Scores

95-100

Automatic Suggestion

80-95

Supervisor Review

Below 80

Manual Review

---

# Failure Handling

LLM Failure

Fallback

OR-Tools

Traffic Failure

Cached Route

OSM Failure

Previous Graph

Weather Failure

Ignore

Database Failure

Retry

---

# Explainability

Every optimization must answer

Why?

What changed?

Expected benefit?

Affected stops?

Time saved?

Fuel saved?

Risk?

Confidence?

---

# Human in the Loop

Planner

↓

AI

↓

Supervisor

↓

Approve

↓

Dispatch

---

# Performance Targets

Initial Route

<10 seconds

Replanning

<5 seconds

Explanation

<2 seconds

Validation

<1 second

Notification

<1 second

---

# Logging

Every Agent

Input

Output

Latency

Token Usage

Cost

Errors

Retry Count

---

# Monitoring

Agent Health

Latency

Failures

Cost

Requests

Approval Rate

Optimization Accuracy

---

# Security

No Prompt Injection

Input Validation

Output Validation

Audit Logs

Role Permissions

Encrypted Communication

---

# Future Agents

Traffic Prediction Agent

Weather Prediction Agent

Demand Forecast Agent

Carbon Optimization Agent

Cost Optimization Agent

Fleet Health Agent

Digital Twin Agent

Customer Satisfaction Agent

IoT Telemetry Agent

Voice Assistant Agent

---

# Complete AI Pipeline

Amazon Dataset
        │
        ▼
Data Loader
        │
        ▼
Planner Agent
        │
        ▼
Constraint Agent
        │
        ▼
Validation Agent
        │
        ▼
Explainability Agent
        │
        ▼
Supervisor Approval
        │
        ▼
Driver Notification
        │
        ▼
Analytics Dashboard

---

# Technologies

FastAPI

CrewAI (Optional)

LangGraph (Optional)

Google ADK (Future)

Gemini API

OR-Tools

OpenStreetMap

Redis

PostgreSQL

Docker

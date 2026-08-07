# RouteMind Deployment Guide

Version: 1.0

Status

Production Ready

---

# Purpose

This document explains how RouteMind is deployed,
configured, monitored and maintained across
development and production environments.

---

# Deployment Goals

Simple

Repeatable

Scalable

Secure

Automated

Cloud Ready

Low Cost

---

# Environments

Development

Local Machine

Testing

CI/CD

Staging

Cloud Test Environment

Production

AWS Cloud

---

# Technology Stack

Frontend

Next.js

Backend

FastAPI

AI

Gemini API

Optimization

Google OR-Tools

Database

PostgreSQL

Cache

Redis

Storage

MinIO / Amazon S3

Reverse Proxy

NGINX

Containerization

Docker

Orchestration

Docker Compose

CI/CD

GitHub Actions

Hosting

AWS EC2

Monitoring

Prometheus (Future)

Grafana (Future)

---

# Development Environment

Requirements

Python 3.12+

Node.js 22+

Docker

Docker Compose

Git

VS Code

---

# Local Architecture

Developer

↓

Frontend

↓

Backend

↓

PostgreSQL

↓

Redis

↓

MinIO

---

# Docker Architecture

                   Docker Compose

        ┌──────────────────────────────────┐
        │                                  │
        │ Frontend Container               │
        │ Backend Container                │
        │ PostgreSQL Container             │
        │ Redis Container                  │
        │ MinIO Container                  │
        │ NGINX Container                  │
        │                                  │
        └──────────────────────────────────┘

---

# Containers

Frontend

Port

3000

Backend

8000

PostgreSQL

5432

Redis

6379

MinIO

9000

NGINX

80

HTTPS

443

---

# Production Architecture

                Internet

                    │

               HTTPS (443)

                    │

              NGINX Reverse Proxy

                    │

        ┌───────────┴────────────┐

        │                        │

    Next.js                 FastAPI

        │                        │

        └───────────┬────────────┘

                    │

        PostgreSQL      Redis

                    │

                MinIO Storage

                    │

              Gemini API

                    │

              OR-Tools Solver

---

# Environment Variables

Frontend

NEXT_PUBLIC_API_URL

NEXT_PUBLIC_MAP_URL

NEXT_PUBLIC_APP_NAME

Backend

DATABASE_URL

REDIS_URL

JWT_SECRET

JWT_EXPIRE

GOOGLE_API_KEY

MINIO_ENDPOINT

MINIO_ACCESS_KEY

MINIO_SECRET_KEY

LOG_LEVEL

APP_ENV

---

# Secrets

Never Commit

.env

.env.production

API Keys

JWT Secret

Database Password

Redis Password

AWS Keys

---

# NGINX

Responsibilities

HTTPS

Compression

Caching

Reverse Proxy

Load Balancing

Static Assets

Security Headers

---

# HTTPS

Let's Encrypt

TLS 1.3

Automatic Renewal

HTTP Redirect

---

# Database

PostgreSQL

Daily Backup

Point-In-Time Recovery

Indexes

Connection Pool

---

# Redis

Cache

Sessions

Live Tracking

AI Results

Dashboard

TTL

5 Seconds

30 Seconds

5 Minutes

---

# Storage

MinIO

Stores

Reports

CSV

PDF

Images

Driver Photos

Optimization Results

Logs

---

# Logging

API Logs

Error Logs

Optimization Logs

AI Logs

System Logs

Security Logs

---

# Log Levels

DEBUG

INFO

WARNING

ERROR

CRITICAL

---

# Monitoring

CPU

Memory

Disk

Database

Redis

API

AI

OR-Tools

---

# Health Check

GET

/health

Checks

Database

Redis

Gemini

OR-Tools

Storage

API

---

# Security

HTTPS

JWT

RBAC

Input Validation

Rate Limiting

Audit Logs

Encrypted Passwords

Security Headers

CORS

---

# Rate Limits

Login

10/minute

Optimization

30/hour

AI

100/hour

General API

1000/hour

---

# CI/CD

GitHub Push

↓

GitHub Actions

↓

Run Tests

↓

Lint

↓

Build

↓

Docker Image

↓

Deploy

↓

Health Check

↓

Production

---

# GitHub Actions

frontend.yml

backend.yml

tests.yml

docker.yml

release.yml

security.yml

---

# Deployment Workflow

Developer

↓

Git Push

↓

GitHub

↓

CI Pipeline

↓

Tests

↓

Docker Build

↓

Deploy

↓

Health Check

↓

Production

---

# Backup Strategy

Database

Daily

Redis

Optional

Storage

Weekly

Configuration

Git

---

# Restore Strategy

Restore Database

↓

Restore Storage

↓

Restart Services

↓

Verify Health

---

# Scaling

Current

Single Server

Future

Multiple API Servers

Load Balancer

Database Replica

Redis Cluster

Kubernetes

---

# Performance Targets

Dashboard

<2 seconds

Optimization

<10 seconds

Replanning

<5 seconds

API

<300ms

AI Explanation

<2 seconds

---

# Error Recovery

Retry

Fallback Cache

Graceful Shutdown

Circuit Breaker (Future)

---

# Maintenance

Weekly Updates

Monthly Backup Validation

Dependency Updates

Security Patches

Database Optimization

---

# Deployment Checklist

Python Installed

Node Installed

Docker Installed

Docker Compose Installed

Environment Variables Configured

Database Running

Redis Running

MinIO Running

Frontend Running

Backend Running

NGINX Running

HTTPS Enabled

Health Check Passing

Logs Working

Monitoring Enabled

Backup Configured

---

# Production Checklist

HTTPS

JWT

Backups

Rate Limiting

Compression

Caching

Health Checks

Monitoring

Logging

Secrets

Firewall

---

# Future Deployment

AWS ECS

Kubernetes

Terraform

CloudFront

AWS RDS

AWS ElastiCache

AWS S3

AWS EKS

Auto Scaling

Multi Region

Disaster Recovery

---

# Deployment Principles

✔ Infrastructure as Code

✔ Container First

✔ Cloud Native

✔ Secure by Default

✔ Zero Downtime Ready

✔ Automated CI/CD

✔ Scalable

✔ Observable

✔ Easy Rollback
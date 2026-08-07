# RouteMind Project Structure

Version: 1.0

Status

Production Ready

---

# Repository Overview

RouteMind follows a Monorepo Architecture.

Advantages

- Easy Development
- Shared Types
- Shared Config
- Single Deployment
- Better Collaboration
- Easier CI/CD

---

# Root Structure

RouteMind/

│

├── frontend/

├── backend/

├── ai/

├── datasets/

├── docs/

├── scripts/

├── infrastructure/

├── docker/

├── tests/

├── .github/

├── README.md

├── docker-compose.yml

├── .env.example

├── LICENSE

└── .gitignore

---

# Frontend

frontend/

│

├── src/

│   ├── app/

│   ├── components/

│   ├── features/

│   ├── hooks/

│   ├── services/

│   ├── store/

│   ├── lib/

│   ├── utils/

│   ├── types/

│   ├── assets/

│   └── styles/

│

├── public/

├── tests/

├── package.json

├── next.config.ts

└── tsconfig.json

---

# App Router

app/

dashboard/

map/

routes/

drivers/

vehicles/

analytics/

notifications/

settings/

login/

layout.tsx

page.tsx

loading.tsx

error.tsx

not-found.tsx

---

# Components

components/

ui/

cards/

charts/

tables/

forms/

dialogs/

sidebar/

navbar/

footer/

maps/

notifications/

common/

---

# Features

features/

dashboard/

optimization/

tracking/

drivers/

vehicles/

analytics/

authentication/

settings/

---

# Services

services/

api.ts

auth.ts

dashboard.ts

routes.ts

vehicles.ts

drivers.ts

tracking.ts

analytics.ts

notifications.ts

optimization.ts

ai.ts

---

# Store

store/

auth.store.ts

dashboard.store.ts

route.store.ts

vehicle.store.ts

driver.store.ts

notification.store.ts

theme.store.ts

---

# Backend

backend/

│

├── app/

├── alembic/

├── tests/

├── scripts/

├── requirements/

├── Dockerfile

├── pyproject.toml

└── README.md

---

# Backend App

app/

api/

core/

models/

schemas/

services/

repositories/

agents/

optimization/

tracking/

database/

middleware/

utils/

config/

workers/

---

# API

api/

auth.py

dashboard.py

routes.py

optimization.py

tracking.py

drivers.py

vehicles.py

analytics.py

notifications.py

settings.py

health.py

---

# Core

core/

security.py

jwt.py

permissions.py

exceptions.py

logging.py

config.py

constants.py

---

# Models

models/

user.py

driver.py

vehicle.py

hub.py

route.py

stop.py

package.py

optimization.py

notification.py

analytics.py

---

# Schemas

schemas/

user.py

driver.py

vehicle.py

route.py

optimization.py

notification.py

analytics.py

common.py

---

# Services

services/

dashboard_service.py

route_service.py

driver_service.py

vehicle_service.py

tracking_service.py

optimization_service.py

analytics_service.py

notification_service.py

ai_service.py

---

# Repositories

repositories/

user_repository.py

driver_repository.py

vehicle_repository.py

route_repository.py

optimization_repository.py

analytics_repository.py

---

# AI

agents/

coordinator.py

planner.py

constraint.py

event.py

replanner.py

validator.py

explainer.py

analytics.py

prompts/

memory/

tools/

---

# Prompts

prompts/

planner.md

constraint.md

explainer.md

validator.md

replanner.md

supervisor.md

---

# Optimization

optimization/

or_tools/

distance_matrix/

constraints/

solver/

simulation/

utils/

---

# Tracking

tracking/

gps/

live/

cache/

events/

---

# Database

database/

session.py

connection.py

base.py

seed.py

migrations.py

---

# Workers

workers/

notification_worker.py

optimization_worker.py

analytics_worker.py

scheduler.py

---

# AI Folder

ai/

research/

benchmarks/

prompt_tests/

evaluation/

experiments/

datasets/

---

# Datasets

datasets/

amazon/

osm/

processed/

raw/

cache/

exports/

sample/

---

# Infrastructure

infrastructure/

terraform/

nginx/

monitoring/

logging/

---

# Docker

docker/

frontend/

backend/

postgres/

redis/

minio/

---

# Documentation

docs/

01_Master_PRD.md

02_Backend_PRD.md

03_Frontend_PRD.md

04_UI_UX.md

05_API_Documentation.md

06_Database_Design.md

07_AI_Agent_Architecture.md

08_System_Architecture.md

09_Project_Structure.md

10_Deployment.md

Architecture_Diagrams/

API/

Images/

Meeting_Notes/

---

# Tests

tests/

frontend/

backend/

integration/

performance/

load/

security/

ai/

---

# GitHub

.github/

workflows/

issue_templates/

pull_request_template.md

---

# CI/CD

workflows/

frontend.yml

backend.yml

tests.yml

docker.yml

release.yml

---

# Scripts

scripts/

setup.sh

setup.ps1

seed.py

download_osm.py

download_dataset.py

build_distance_matrix.py

run_demo.py

cleanup.py

---

# Configuration

config/

development.env

testing.env

production.env

---

# Environment Variables

.env

.env.local

.env.production

.env.example

---

# Assets

assets/

icons/

logos/

images/

animations/

---

# Logs

logs/

api/

optimization/

ai/

system/

---

# Reports

reports/

daily/

weekly/

monthly/

optimization/

benchmark/

---

# Exports

exports/

csv/

excel/

pdf/

json/

---

# Shared Coding Standards

Python

Black

isort

Ruff

MyPy

TypeScript

ESLint

Prettier

Husky

Commitlint

---

# Git Branch Strategy

main

develop

feature/*

bugfix/*

hotfix/*

release/*

---

# Commit Convention

feat:

fix:

docs:

refactor:

test:

style:

chore:

ci:

perf:

---

# Development Workflow

Create Feature Branch

↓

Develop Feature

↓

Write Tests

↓

Run Lint

↓

Create Pull Request

↓

Code Review

↓

Merge to Develop

↓

Deploy

---

# Future Expansion

mobile/

desktop/

sdk/

plugins/

microservices/

kubernetes/

event-bus/

digital-twin/

iot/

---

# Repository Principles

✔ Clean Architecture

✔ Domain Driven Design

✔ Feature Based Structure

✔ Modular Components

✔ Reusable Services

✔ AI First

✔ Testable

✔ Maintainable

✔ Scalable

✔ Enterprise Ready
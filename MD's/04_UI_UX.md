# RouteMind UI/UX Design Specification

Version: 1.0

---

# Purpose

Design a modern enterprise dashboard for logistics route optimization.

The interface should feel like:

• Google Maps
• Uber Fleet
• Amazon Logistics
• Azure Dashboard

Focus on

- Simplicity
- Speed
- Explainability
- Real-time Monitoring

---

# Design Philosophy

Minimal

Enterprise

Clean

Professional

Data First

Responsive

AI Assisted

---

# Theme

Primary
#2563EB

Success
#16A34A

Warning
#F59E0B

Danger
#DC2626

Info
#0EA5E9

Background
#F8FAFC

Card
#FFFFFF

Border
#E5E7EB

Text
#111827

Dark Mode Supported

---

# Typography

Font

Inter

Weights

400

500

600

700

Heading Sizes

H1

36px

H2

30px

H3

24px

H4

20px

Body

16px

Caption

14px

---

# Border Radius

Cards

16px

Buttons

12px

Inputs

12px

Dialogs

20px

---

# Shadows

Small

Medium

Large

Glass Effect

Only on Dialogs

---

# Grid System

12 Column Grid

Maximum Width

1600px

Spacing

8px System

8

16

24

32

40

48

64

---

# Navigation

Desktop

----------------------------------------

Sidebar

Logo

Dashboard

Live Map

Routes

Drivers

Vehicles

Analytics

Notifications

Settings

----------------------------------------

Top Bar

Search

Notification Bell

Theme Toggle

Profile

----------------------------------------

Content Area

Dynamic

---

# Mobile Navigation

Bottom Navigation

Dashboard

Map

Routes

Analytics

Profile

Sidebar becomes Drawer

---

# Dashboard Layout

------------------------------------------------------------

Top

Welcome Message

Date

Quick Search

------------------------------------------------------------

Row 1

Stat Cards

Total Routes

Active Drivers

Completed Deliveries

Fuel Saved

Optimization Score

------------------------------------------------------------

Row 2

Map Preview

AI Insights

------------------------------------------------------------

Row 3

Charts

Daily Deliveries

Route Success

Vehicle Usage

------------------------------------------------------------

Bottom

Activity Timeline

Alerts

Notifications

---

# Live Map Screen

Left Sidebar

Vehicle Filters

Search

Status

City

Vehicle Type

------------------------------------------------

Center

Interactive OpenStreetMap

Animated Vehicles

Routes

Traffic

Hub

Customers

------------------------------------------------

Right Panel

Vehicle Details

Driver

ETA

Stops

Fuel

Packages

AI Suggestions

---

# Route Details Page

Header

Route ID

Driver

Vehicle

Status

------------------------------------------------

Cards

Distance

ETA

Fuel

Packages

Stops

Optimization Score

------------------------------------------------

Tabs

Overview

Stops

Timeline

AI Decisions

History

---

# AI Explanation Screen

Header

Route Comparison

------------------------------------------------

Old Route

↓

New Route

------------------------------------------------

Reason Cards

Traffic

Weather

COD Limit

Time Window

Vehicle Capacity

------------------------------------------------

Impact Cards

Minutes Saved

Fuel Saved

Distance Saved

Cost Saved

Carbon Saved

------------------------------------------------

Bottom

Approve

Reject

Comment

---

# Drivers Screen

Driver Cards

Photo

Name

Rating

Status

Today's Deliveries

Working Hours

Location

Buttons

View

Assign

History

---

# Vehicles Screen

Table

Vehicle

Driver

Fuel

Capacity

Speed

Location

Status

Action

---

# Analytics Screen

Cards

KPIs

Charts

Heatmaps

Performance

Filters

Day

Week

Month

Year

Export Button

---

# Notifications

Grouped

Today

Yesterday

Older

Notification Types

Traffic

Weather

Pickup

Failure

Maintenance

AI

System

---

# Settings

Profile

Organization

Map

Notifications

Theme

Language

API

Security

---

# Components

Buttons

Primary

Secondary

Danger

Ghost

Outline

Cards

Tables

Charts

Progress

Timeline

Accordion

Tabs

Badge

Avatar

Dialogs

Tooltips

Toast

Drawer

Dropdown

Date Picker

Command Menu

Search

Loading Skeleton

Pagination

Breadcrumb

---

# Map Components

Vehicle Marker

Hub Marker

Customer Marker

Traffic Layer

Weather Layer

Route Polyline

Current Position

ETA Popup

Distance Labels

Cluster Marker

---

# Charts

Area Chart

Bar Chart

Line Chart

Pie Chart

Donut Chart

Radar

Heatmap

Timeline

---

# Status Colors

Online

Green

Idle

Yellow

Offline

Gray

Emergency

Red

Optimized

Blue

---

# Icons

Lucide Icons

Navigation

Map

Truck

Route

Clock

Fuel

Alert

User

Settings

Bell

Analytics

Robot

---

# Loading States

Dashboard Skeleton

Map Loader

Card Skeleton

Table Skeleton

Chart Skeleton

Button Spinner

---

# Empty States

No Routes

No Drivers

No Vehicles

No Alerts

No Notifications

No Analytics

---

# Error States

500

404

No Internet

API Error

Permission Denied

Retry

---

# Animations

Fade

Slide

Scale

Map Marker Pulse

Vehicle Movement

Toast Slide

Sidebar Collapse

Card Hover

Chart Animation

---

# Responsive Breakpoints

Desktop

1600+

Laptop

1440

Small Laptop

1280

Tablet

768

Mobile

480

---

# Accessibility

Keyboard Navigation

Focus Ring

High Contrast

Screen Reader

ARIA Labels

Large Touch Targets

---

# User Flow

Login

↓

Dashboard

↓

Live Map

↓

Select Route

↓

View AI Recommendation

↓

Approve

↓

Dispatch Driver

↓

Monitor Progress

↓

Receive Alerts

↓

Analytics

---

# Design Inspiration

Google Maps Fleet

Uber Fleet

Amazon Logistics

Azure Portal

Linear

Vercel Dashboard

---

# UI Principles

Every screen should answer three questions immediately:

1. What is happening?

2. Why is it happening?

3. What action should the supervisor take?

No screen should feel cluttered.

Maps should always remain the primary visual element.

AI explanations must always accompany route changes.

Important actions should require at most two clicks.

Critical alerts must always remain visible.

---

# Deliverables

Responsive Dashboard

Desktop Layout

Tablet Layout

Mobile Layout

Component Library

Design Tokens

Color System

Typography System

Spacing System

Animation Guidelines

Accessibility Checklist

Ready for Figma

Ready for Google AI Studio

Ready for Frontend Development
# Implementation and Test Deliverable (ITD)

# Best Bike Paths (BBP) Road Application

---

## Front Page

| **Document Information** | |
|--------------------------|-----|
| **Project Name** | Best Bike Paths (BBP) |
| **Document Type** | Implementation and Test Deliverable (ITD) |
| **Version** | 1.0 |
| **Date** | January 30, 2026 |
| **Course** | Software Engineering 2 |

### Team Members

| Name | Student ID | Email |
|------|------------|-------|
| [Hu Xu Yan] | [Student ID] | [email@polimi.it] |
| [Team Member 2] | [Student ID] | [email@polimi.it] |
| [Team Member 3] | [Student ID] | [email@polimi.it] |

### Software Links

| Resource | Location |
|----------|----------|
| **Source Code** | `DeliveryFolder/bbp-road-app/` |
| **Backend Source** | `DeliveryFolder/bbp-road-app/backend/main.py` |
| **Frontend Source** | `DeliveryFolder/bbp-road-app/frontend/src/` |
| **Installation Files** | `DeliveryFolder/bbp-road-app/` |
| **Node.js Runtime** | `DeliveryFolder/bbp-road-app/node-v20.19.0-win-x64/` |

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Scope of the Document](#2-scope-of-the-document)
3. [Implemented Requirements and Functions](#3-implemented-requirements-and-functions)
4. [Adopted Development Frameworks](#4-adopted-development-frameworks)
5. [Structure of the Source Code](#5-structure-of-the-source-code)
6. [Testing](#6-testing)
7. [Installation Instructions](#7-installation-instructions)
8. [Effort Spent](#8-effort-spent)
9. [References](#9-references)

---

## 1. Introduction

The Best Bike Paths (BBP) application is a comprehensive road condition monitoring and route planning system designed specifically for cyclists. The system enables users to:

- Report and track road conditions (potholes, surface quality, obstacles)
- Plan optimal cycling routes based on road quality data
- Contribute to a community-driven road quality database
- Receive intelligent route recommendations with safety scoring

This document describes the implementation details of the BBP prototype, including the architectural decisions, implemented features, testing procedures, and installation instructions.

### 1.1 Purpose

This ITD document serves as the technical reference for the BBP implementation, providing:

- Documentation of all implemented functionalities
- Justification for technology choices
- Comprehensive testing results
- Step-by-step installation guide for deployment

### 1.2 Definitions, Acronyms, and Abbreviations

| Term | Definition |
|------|------------|
| BBP | Best Bike Paths |
| OSRM | Open Source Routing Machine |
| API | Application Programming Interface |
| REST | Representational State Transfer |
| CRUD | Create, Read, Update, Delete |
| i18n | Internationalization |
| SPA | Single Page Application |

---

## 2. Scope of the Document

This document covers the complete implementation of the BBP road application prototype, including:

1. **Backend Implementation**: FastAPI-based REST API server with in-memory data storage
2. **Frontend Implementation**: React-based Single Page Application with interactive maps
3. **Integration**: OSRM routing service integration for real road geometry
4. **Testing**: Unit tests and system-level test cases
5. **Deployment**: Installation and configuration instructions

### 2.1 Document Boundaries

This document focuses on:
- ✅ Implemented prototype features
- ✅ Technical architecture and code structure
- ✅ Testing methodology and results
- ✅ Installation procedures

This document does NOT cover:
- ❌ Production deployment configurations
- ❌ Performance optimization strategies
- ❌ Future enhancement roadmap

---

## 3. Implemented Requirements and Functions

### 3.1 Implemented Features Overview

| Feature Category | Feature | Status | Priority |
|------------------|---------|--------|----------|
| **User Management** | User Registration | ✅ Implemented | High |
| | User Settings | ✅ Implemented | Medium |
| | Multi-language Support | ✅ Implemented | Medium |
| **Segment Management** | Create Road Segments | ✅ Implemented | High |
| | View Segments on Map | ✅ Implemented | High |
| | Segment Status Tracking | ✅ Implemented | High |
| **Report System** | Submit Condition Reports | ✅ Implemented | High |
| | Report Confirmation | ✅ Implemented | High |
| | Weighted Voting Aggregation | ✅ Implemented | High |
| | Batch Confirmation | ✅ Implemented | Medium |
| **Route Planning** | OSRM Route Integration | ✅ Implemented | High |
| | Generate & Evaluate Algorithm | ✅ Implemented | High |
| | Route Quality Scoring | ✅ Implemented | High |
| | Multiple Route Alternatives | ✅ Implemented | Medium |
| **Trip Management** | Create Trips | ✅ Implemented | High |
| | Trip History | ✅ Implemented | Medium |
| | Privacy Protection | ✅ Implemented | High |
| **Auto Detection** | Sensor-based Detection | ✅ Implemented | Medium |
| | Auto-confirm Reports | ✅ Implemented | Low |
| **Weather Service** | Weather Information | ✅ Implemented | Low |
| | Cycling Recommendations | ✅ Implemented | Low |
| **Internationalization** | English (en) | ✅ Implemented | Medium |
| | Chinese (zh) | ✅ Implemented | Medium |
| | Italian (it) | ✅ Implemented | Medium |

### 3.2 Detailed Feature Descriptions

#### 3.2.1 User Management

**Implementation**: Users can register with a username. The system stores user preferences including language, dark mode, notification settings, and default map configurations.

```
API Endpoints:
- POST /api/users - Create or get user
- GET /api/users - List all users
- GET /api/users/{user_id}/settings - Get user settings
- PUT /api/users/{user_id}/settings - Update user settings
- PATCH /api/users/{user_id}/settings - Partial update settings
```

**Motivation**: User management is essential for personalized experience and tracking individual contributions to the road condition database.

#### 3.2.2 Road Segment Management

**Implementation**: Road segments are defined by start and end GPS coordinates with associated status (optimal, medium, suboptimal, maintenance) and optional obstacle information.

```
API Endpoints:
- GET /api/segments - List all segments (with localized status)
- POST /api/segments - Create new segment
```

**Status Classification**:
| Status | Description | Color Code |
|--------|-------------|------------|
| Optimal | Excellent road condition | Green |
| Medium | Fair condition, minor issues | Yellow |
| Suboptimal | Poor condition, caution advised | Orange |
| Maintenance | Under repair, avoid if possible | Red |

#### 3.2.3 Report System with Weighted Voting

**Implementation**: Users submit reports for road segments. The system uses a weighted voting algorithm to aggregate reports and automatically update segment status.

**Weighting Algorithm**:
```python
Weight Calculation:
- Base weight: 1.0
- Fresh report (< 30 days): ×2.0 multiplier
- Confirmed report: ×1.5 multiplier

Status Determination:
- negative_score >= 0.6 → "maintenance"
- negative_score >= 0.3 → "medium"  
- positive_score > 0.7 → "optimal"
- Otherwise → "medium"
```

**Motivation**: Weighted voting ensures that recent and verified reports have greater influence on road status, improving data accuracy over time.

#### 3.2.4 Route Planning with Quality Scoring

**Implementation**: The "Generate & Evaluate" algorithm provides intelligent route recommendations:

**Phase 1: Candidate Generation**
1. Direct route from OSRM
2. Routes via perpendicular waypoints (15% offset)
3. Deduplication of similar routes (>80% overlap)

**Phase 2: Scoring**
```
Score = Distance + Penalty

Penalty Calculation by Preference:
┌─────────────┬──────────────┬──────────────┬────────────┐
│ Factor      │ safety_first │ balanced     │ shortest   │
├─────────────┼──────────────┼──────────────┼────────────┤
│ Pothole     │ 1200         │ 500          │ 100        │
│ Maintenance │ 10.0×length  │ 4.0×length   │ 0.8×length │
│ Bad Road    │ 5.0×length   │ 2.0×length   │ 0.3×length │
│ Medium Road │ 1.5×length   │ 0.5×length   │ 0.1×length │
└─────────────┴──────────────┴──────────────┴────────────┘
```

**Phase 3: Tagging**
- "Recommended" - Top-ranked route
- "Alternative" - Other viable routes
- "Best Surface" - Quality score > 90
- "Fastest" - Shortest distance
- "Bumpy", "Road Work", "Poor Surface" - Warning tags

#### 3.2.5 Privacy By Design

**Implementation**: Location privacy protection following GDPR principles:

1. **Location Obfuscation**: Start/end points fuzzed by ~150m
2. **Coordinate Truncation**: Public coordinates rounded to 3 decimal places (~100m precision)
3. **Trip Geometry Sanitization**: First and last 150m of trip routes obfuscated
4. **Private Data Separation**: Raw coordinates stored separately, only accessible by owner

```python
Privacy Methods:
- "noise": Random offset within 150m radius
- "grid": Snap to 200m grid
- "truncate": Round to 3 decimal places
```

### 3.3 Excluded Features and Justification

| Feature | Reason for Exclusion |
|---------|---------------------|
| User Authentication (JWT) | Simplified for prototype; username-based identification sufficient for demo |
| Persistent Database | In-memory storage suitable for prototype; reduces deployment complexity |
| Real-time Notifications | Would require WebSocket infrastructure; deferred to future iteration |
| Mobile App | Web-based SPA provides cross-platform access; native app not required for prototype |
| Social Features | Core functionality prioritized; social features are enhancement, not essential |
| Payment Integration | Out of scope for academic prototype |

---

## 4. Adopted Development Frameworks

### 4.1 Programming Languages

#### 4.1.1 Backend: Python 3.10+

| Aspect | Details |
|--------|---------|
| **Version** | Python 3.10 or higher |
| **Paradigm** | Multi-paradigm (OOP, Functional) |

**Advantages**:
- ✅ Rapid development with clean, readable syntax
- ✅ Excellent library ecosystem (FastAPI, Pydantic, httpx)
- ✅ Strong type hints support for better code quality
- ✅ Easy integration with scientific computing libraries
- ✅ Large community and extensive documentation

**Disadvantages**:
- ❌ Slower execution compared to compiled languages
- ❌ Global Interpreter Lock (GIL) limits true parallelism
- ❌ Memory consumption higher than C/C++

**Justification**: Python's rapid development capabilities and the excellent FastAPI framework make it ideal for building REST APIs quickly while maintaining code quality through type hints.

#### 4.1.2 Frontend: TypeScript 5.9

| Aspect | Details |
|--------|---------|
| **Version** | TypeScript ~5.9.3 |
| **Paradigm** | Object-oriented, Functional |

**Advantages**:
- ✅ Static type checking catches errors at compile time
- ✅ Enhanced IDE support with autocompletion
- ✅ Better code maintainability and refactoring
- ✅ Seamless integration with React ecosystem
- ✅ Industry standard for modern web development

**Disadvantages**:
- ❌ Additional compilation step required
- ❌ Learning curve for developers new to static typing
- ❌ Type definitions may lag behind JavaScript libraries

**Justification**: TypeScript provides the type safety necessary for maintaining a complex React application while leveraging the vast JavaScript ecosystem.

### 4.2 Frameworks

#### 4.2.1 Backend Framework: FastAPI

| Aspect | Details |
|--------|---------|
| **Version** | Latest stable |
| **Type** | Async Web Framework |

**Advantages**:
- ✅ Automatic OpenAPI (Swagger) documentation generation
- ✅ Built-in request validation via Pydantic
- ✅ Native async/await support for high performance
- ✅ Dependency injection system
- ✅ Excellent developer experience

**Disadvantages**:
- ❌ Relatively new compared to Django/Flask
- ❌ Smaller plugin ecosystem
- ❌ Async programming complexity for beginners

#### 4.2.2 Frontend Framework: React 19

| Aspect | Details |
|--------|---------|
| **Version** | React 19.2.0 |
| **Type** | UI Component Library |

**Advantages**:
- ✅ Component-based architecture promotes reusability
- ✅ Virtual DOM for efficient rendering
- ✅ Hooks API for state management
- ✅ Large ecosystem and community support
- ✅ Excellent developer tools

**Disadvantages**:
- ❌ Steep learning curve for beginners
- ❌ Frequent updates may require migration effort
- ❌ JSX syntax unconventional for some developers

#### 4.2.3 Build Tool: Vite

| Aspect | Details |
|--------|---------|
| **Version** | rolldown-vite 7.2.5 |
| **Type** | Frontend Build Tool |

**Advantages**:
- ✅ Extremely fast hot module replacement (HMR)
- ✅ Native ES modules support
- ✅ Optimized production builds
- ✅ Simple configuration

**Disadvantages**:
- ❌ Less mature than Webpack
- ❌ Some plugins may not be compatible

### 4.3 Libraries and Middleware

#### 4.3.1 Backend Libraries

| Library | Purpose | Version |
|---------|---------|---------|
| **uvicorn** | ASGI server for FastAPI | Latest |
| **pydantic** | Data validation and serialization | Latest |
| **httpx** | HTTP client for OSRM API calls | Latest |
| **python-multipart** | Form data parsing | Latest |

#### 4.3.2 Frontend Libraries

| Library | Purpose | Version |
|---------|---------|---------|
| **react-leaflet** | React components for Leaflet maps | 5.0.0 |
| **leaflet** | Interactive map library | 1.9.4 |

### 4.4 External APIs

#### 4.4.1 OSRM (Open Source Routing Machine)

| Aspect | Details |
|--------|---------|
| **Base URL** | `http://router.project-osrm.org` |
| **Profile** | Bicycle routing |
| **Timeout** | 10 seconds |

**Endpoints Used**:
```
GET /route/v1/bike/{coordinates}
Parameters:
- overview=full
- geometries=geojson
- alternatives=true/false
- steps=true
```

**Advantages**:
- ✅ Free public API for bicycle routing
- ✅ Real road geometry data
- ✅ Support for alternative routes
- ✅ Turn-by-turn navigation data

**Disadvantages**:
- ❌ Rate limits on public server
- ❌ No guaranteed uptime
- ❌ Limited to road network coverage

**Fallback Strategy**: When OSRM is unavailable, the system falls back to geometric interpolation using Haversine distance calculations.

### 4.5 CORS Configuration

```python
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 5. Structure of the Source Code

### 5.1 Project Directory Structure

```
bbp-road-app/
├── README.md                    # Project documentation
├── backend/                     # Python FastAPI backend
│   ├── main.py                  # Main application file (2144 lines)
│   ├── requirements.txt         # Python dependencies
│   └── test_routing.py          # Routing algorithm tests
├── frontend/                    # React TypeScript frontend
│   ├── index.html               # HTML entry point
│   ├── package.json             # Node.js dependencies
│   ├── tsconfig.json            # TypeScript configuration
│   ├── tsconfig.app.json        # App-specific TS config
│   ├── tsconfig.node.json       # Node-specific TS config
│   ├── vite.config.ts           # Vite build configuration
│   └── src/                     # Source code
│       ├── main.tsx             # React entry point
│       ├── App.tsx              # Main application component
│       ├── AppContext.tsx       # Global state management
│       ├── api.ts               # API client functions
│       ├── index.css            # Global styles
│       ├── Layout.tsx           # Page layout component
│       ├── LoginPage.tsx        # User login page
│       ├── DashboardPage.tsx    # Dashboard with statistics
│       ├── SegmentsPage.tsx     # Segment management
│       ├── ReportsPage.tsx      # Report submission
│       ├── RoutePlanningPage.tsx # Route planning interface
│       ├── TripsPage.tsx        # Trip creation
│       ├── TripHistoryPage.tsx  # Trip history view
│       ├── AutoDetectionPage.tsx # Auto-detection feature
│       ├── SettingsPage.tsx     # User settings
│       └── MapView.tsx          # Leaflet map component
└── node-v20.19.0-win-x64/       # Bundled Node.js runtime
    └── node-v20.19.0-win-x64/
        ├── node.exe
        ├── npm.cmd
        └── npx.cmd
```

### 5.2 Backend Architecture (main.py)

The backend follows a **layered service architecture**:

```
┌─────────────────────────────────────────────────────────────┐
│                    API Layer (FastAPI)                       │
│  Endpoints: /api/users, /api/segments, /api/trips, etc.     │
├─────────────────────────────────────────────────────────────┤
│                    Service Layer                             │
│  ┌─────────────────┐ ┌─────────────────┐ ┌────────────────┐ │
│  │ WeatherService  │ │ RoutingService  │ │ AggregationSvc │ │
│  │ - get_weather() │ │ - fetch_osrm()  │ │ - aggregate()  │ │
│  │ - get_recommend │ │ - score_route() │ │ - vote()       │ │
│  └─────────────────┘ └─────────────────┘ └────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                    Data Models (Pydantic)                    │
│  UserCreate, SegmentCreate, ReportCreate, TripCreate, etc.  │
├─────────────────────────────────────────────────────────────┤
│                    Data Storage Layer                        │
│  USERS: Dict, SEGMENTS: Dict, REPORTS: Dict, TRIPS: Dict    │
└─────────────────────────────────────────────────────────────┘
```

#### 5.2.1 Module Organization (main.py sections)

| Lines | Section | Description |
|-------|---------|-------------|
| 1-130 | Internationalization (i18n) | Translation dictionaries and helper functions |
| 131-230 | Weather Service | Mock weather data generation |
| 231-300 | OSRM Integration | Route fetching from OSRM API |
| 300-400 | Route Utilities | Perpendicular waypoint calculation, route similarity detection |
| 400-500 | Geo Utilities | Haversine distance, path generation, duration estimation |
| 500-650 | Privacy Helpers | Location obfuscation, trip geometry sanitization |
| 650-720 | Aggregation Service | Weighted voting algorithm for report aggregation |
| 720-800 | Data Storage & Schemas | In-memory stores and Pydantic models |
| 800-900 | Demo Data Seeding | Sample data initialization |
| 900-1200 | CRUD Endpoints | Users, Segments, Reports, Trips |
| 1200-1350 | Auto-Detection | Sensor-based pothole detection logic |
| 1350-1500 | Settings & Weather API | User settings, weather endpoints |
| 1500-1600 | Route Preview | Multi-route preview endpoint |
| 1600-1700 | i18n API | Translation endpoints |
| 1700-2144 | Path Search | Generate & Evaluate algorithm implementation |

### 5.3 Frontend Architecture

The frontend follows a **component-based architecture** with centralized state management:

```
┌────────────────────────────────────────────────────────────┐
│                      App.tsx                                │
│                    (Root Component)                         │
├────────────────────────────────────────────────────────────┤
│                    AppContext.tsx                           │
│              (Global State: darkMode, language, t())        │
├────────────────────────────────────────────────────────────┤
│                     Layout.tsx                              │
│              (Navigation, Header, Sidebar)                  │
├──────────────┬──────────────┬──────────────┬───────────────┤
│ DashboardPage│ SegmentsPage │ ReportsPage  │RoutePlanning  │
│              │              │              │    Page       │
├──────────────┼──────────────┼──────────────┼───────────────┤
│  TripsPage   │TripHistory   │AutoDetection │ SettingsPage  │
│              │    Page      │    Page      │               │
├──────────────┴──────────────┴──────────────┴───────────────┤
│                      MapView.tsx                            │
│               (Leaflet Map Component)                       │
├────────────────────────────────────────────────────────────┤
│                        api.ts                               │
│              (API Client Functions)                         │
└────────────────────────────────────────────────────────────┘
```

#### 5.3.1 Component Descriptions

| Component | Responsibility | Lines |
|-----------|---------------|-------|
| **App.tsx** | Root component, routing logic, user state | ~70 |
| **AppContext.tsx** | Global state provider (dark mode, i18n) | ~330 |
| **Layout.tsx** | Navigation sidebar, header, page structure | ~200 |
| **DashboardPage.tsx** | Statistics cards, segment map, aggregation trigger | ~314 |
| **SegmentsPage.tsx** | Segment CRUD, map visualization | ~241 |
| **ReportsPage.tsx** | Report submission, confirmation workflow | ~281 |
| **RoutePlanningPage.tsx** | Route search, multi-route display, weather | ~618 |
| **TripsPage.tsx** | Trip creation with OSRM integration | ~200 |
| **TripHistoryPage.tsx** | Historical trip listing | ~150 |
| **AutoDetectionPage.tsx** | Sensor-based detection interface | ~200 |
| **SettingsPage.tsx** | User preferences configuration | ~250 |
| **MapView.tsx** | Reusable Leaflet map wrapper | ~150 |
| **api.ts** | HTTP client, type definitions | ~337 |

### 5.4 Data Flow Diagram

```
┌──────────┐    HTTP/JSON    ┌──────────┐    Internal    ┌──────────┐
│  React   │ ◄────────────► │  FastAPI │ ◄────────────► │ In-Memory│
│ Frontend │                 │  Backend │                │   Store  │
└──────────┘                 └──────────┘                └──────────┘
     │                            │
     │                            │ HTTP/JSON
     │                            ▼
     │                       ┌──────────┐
     │                       │   OSRM   │
     │                       │  Server  │
     │                       └──────────┘
     │
     │ WebSocket (Leaflet tiles)
     ▼
┌──────────┐
│OpenStreet│
│   Map    │
└──────────┘
```

---

## 6. Testing

### 6.1 Testing Strategy

The testing strategy follows the Test Plan outlined in the Design Document (DD), with focus on:

1. **Unit Testing**: Individual function testing
2. **Integration Testing**: API endpoint testing
3. **System Testing**: End-to-end user scenario testing

### 6.2 Test Environment

| Component | Configuration |
|-----------|---------------|
| Backend | Python 3.10+, FastAPI TestClient |
| Frontend | Manual testing in Chrome/Firefox |
| OSRM | Public server (router.project-osrm.org) |
| Map Tiles | OpenStreetMap |

### 6.3 System Test Cases

#### Test Case 1: User Registration and Login

| Field | Value |
|-------|-------|
| **Test ID** | STC-001 |
| **Objective** | Verify user can register and login successfully |
| **Preconditions** | Backend server running, Frontend accessible |
| **Input** | Username: "testuser" |
| **Steps** | 1. Navigate to login page<br>2. Enter username "testuser"<br>3. Click "Login" button |
| **Expected Output** | User redirected to dashboard, username displayed in header |
| **Actual Result** | ✅ PASSED - User successfully logged in |

#### Test Case 2: Create Road Segment

| Field | Value |
|-------|-------|
| **Test ID** | STC-002 |
| **Objective** | Verify user can create a new road segment |
| **Preconditions** | User logged in |
| **Input** | Start: (1.3521, 103.8198), End: (1.3621, 103.8298), Status: "optimal" |
| **Steps** | 1. Navigate to Segments page<br>2. Enter coordinates<br>3. Select status<br>4. Click "Create" |
| **Expected Output** | New segment appears in list and on map |
| **Actual Result** | ✅ PASSED - Segment created with correct coordinates |

#### Test Case 3: Submit Condition Report

| Field | Value |
|-------|-------|
| **Test ID** | STC-003 |
| **Objective** | Verify user can submit a condition report |
| **Preconditions** | User logged in, at least one segment exists |
| **Input** | Segment ID: 1, Note: "Pothole near intersection" |
| **Steps** | 1. Select segment from list<br>2. Navigate to Reports<br>3. Enter note<br>4. Click "Submit" |
| **Expected Output** | Report appears in list, aggregation updated |
| **Actual Result** | ✅ PASSED - Report submitted successfully |

#### Test Case 4: Report Confirmation

| Field | Value |
|-------|-------|
| **Test ID** | STC-004 |
| **Objective** | Verify report confirmation updates aggregation |
| **Preconditions** | At least one unconfirmed report exists |
| **Input** | Report ID to confirm |
| **Steps** | 1. Find unconfirmed report<br>2. Click "Confirm" button |
| **Expected Output** | Report marked as confirmed, weighted score updated |
| **Actual Result** | ✅ PASSED - Confirmation status updated |

#### Test Case 5: Route Planning with OSRM

| Field | Value |
|-------|-------|
| **Test ID** | STC-005 |
| **Objective** | Verify route planning returns multiple alternatives |
| **Preconditions** | OSRM server accessible |
| **Input** | Origin: (1.3521, 103.8198), Destination: (1.332, 103.903), Preference: "balanced" |
| **Steps** | 1. Navigate to Route Planning<br>2. Enter coordinates<br>3. Select preference<br>4. Click "Search Routes" |
| **Expected Output** | 1-3 routes displayed with quality scores and tags |
| **Actual Result** | ✅ PASSED - Multiple routes returned with scoring |

#### Test Case 6: Route Quality Scoring (Safety First)

| Field | Value |
|-------|-------|
| **Test ID** | STC-006 |
| **Objective** | Verify safety_first preference prioritizes road quality |
| **Preconditions** | Segments with maintenance status exist near route |
| **Input** | Preference: "safety_first" |
| **Steps** | 1. Search routes with safety_first preference<br>2. Compare route rankings |
| **Expected Output** | Route avoiding maintenance segments ranked first |
| **Actual Result** | ✅ PASSED - Higher quality route recommended |

#### Test Case 7: Weather Information Display

| Field | Value |
|-------|-------|
| **Test ID** | STC-007 |
| **Objective** | Verify weather information shown with route |
| **Preconditions** | Route search completed |
| **Input** | Any route search |
| **Steps** | 1. Complete route search<br>2. Observe weather panel |
| **Expected Output** | Weather conditions, temperature, cycling recommendation displayed |
| **Actual Result** | ✅ PASSED - Weather data shown correctly |

#### Test Case 8: Language Switching

| Field | Value |
|-------|-------|
| **Test ID** | STC-008 |
| **Objective** | Verify UI language can be changed |
| **Preconditions** | User logged in |
| **Input** | Language selection: "中文" (Chinese) |
| **Steps** | 1. Navigate to Settings<br>2. Change language to Chinese<br>3. Save settings |
| **Expected Output** | All UI labels displayed in Chinese |
| **Actual Result** | ✅ PASSED - Language switched successfully |

#### Test Case 9: Data Aggregation Trigger

| Field | Value |
|-------|-------|
| **Test ID** | STC-009 |
| **Objective** | Verify bulk aggregation updates segment statuses |
| **Preconditions** | Multiple segments with reports exist |
| **Input** | Click "Trigger Aggregation" on Dashboard |
| **Steps** | 1. Navigate to Dashboard<br>2. Click "Trigger Aggregation" button |
| **Expected Output** | Summary shows segments processed and status changes |
| **Actual Result** | ✅ PASSED - Aggregation completed, status changes applied |

#### Test Case 10: Auto-Detection Simulation

| Field | Value |
|-------|-------|
| **Test ID** | STC-010 |
| **Objective** | Verify accelerometer-based detection logic |
| **Preconditions** | Segment selected |
| **Input** | z_axis_peak: 20.0 m/s², speed: 5.0 m/s |
| **Steps** | 1. Navigate to Auto Detection<br>2. Run detection on segment |
| **Expected Output** | Detection result shows "suboptimal" status with confidence score |
| **Actual Result** | ✅ PASSED - Correct status detected |

### 6.4 API Testing Results

| Endpoint | Method | Test Result |
|----------|--------|-------------|
| `/api/users` | POST | ✅ PASSED |
| `/api/users` | GET | ✅ PASSED |
| `/api/segments` | GET | ✅ PASSED |
| `/api/segments` | POST | ✅ PASSED |
| `/api/segments/{id}/reports` | POST | ✅ PASSED |
| `/api/segments/{id}/reports` | GET | ✅ PASSED |
| `/api/reports/{id}/confirm` | POST | ✅ PASSED |
| `/api/segments/{id}/aggregate` | GET | ✅ PASSED |
| `/api/aggregation/trigger` | POST | ✅ PASSED |
| `/api/trips` | POST | ✅ PASSED |
| `/api/trips` | GET | ✅ PASSED |
| `/api/path/search` | POST | ✅ PASSED |
| `/api/weather` | GET | ✅ PASSED |
| `/api/users/{id}/settings` | GET/PUT/PATCH | ✅ PASSED |
| `/api/i18n/translations` | GET | ✅ PASSED |

### 6.5 Routing Algorithm Test Script

A dedicated test script (`test_routing.py`) validates the routing algorithm:

```python
# Test execution command:
python test_routing.py

# Test output example:
============================================================
ROUTE SEARCH TEST RESULTS
============================================================
Route Source: osrm
Algorithm: generate_and_evaluate
Candidates Generated: 3
Candidates Returned: 3

Route A (Rank 1):
  Distance: 4523m
  Duration: 7 min
  Quality Score: 92.5
  Tags: ['Recommended', 'Best Surface', 'Fastest']
  Source: osrm_direct

Route B (Rank 2):
  Distance: 4891m
  Duration: 8 min
  Quality Score: 85.3
  Tags: ['Alternative', 'Slightly Longer']
  Source: osrm_via_waypoint
============================================================
```

---

## 7. Installation Instructions

### 7.1 Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| **Python** | 3.10 or higher | Required for backend |
| **Node.js** | 20.x (included) | Bundled in package |
| **npm** | 9.x+ | Comes with Node.js |
| **Web Browser** | Chrome/Firefox/Edge | For frontend access |
| **Internet Connection** | Required | For OSRM API and map tiles |

### 7.2 Quick Start (Windows)

#### Step 1: Extract the Package

```powershell
# Navigate to the delivery folder
cd C:\path\to\DeliveryFolder\bbp-road-app
```

#### Step 2: Start Backend Server

```powershell
# Open PowerShell in backend directory
cd backend

# Create virtual environment (first time only)
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate

# Install dependencies (first time only)
pip install -r requirements.txt

# Start the server
uvicorn main:app --host 127.0.0.1 --port 8000
```

The backend will be running at: `http://127.0.0.1:8000`

API documentation available at: `http://127.0.0.1:8000/docs`

#### Step 3: Start Frontend Development Server

```powershell
# Open a NEW PowerShell window
cd C:\path\to\DeliveryFolder\bbp-road-app\frontend

# Use bundled Node.js (optional, if Node.js not installed globally)
$env:PATH = "..\node-v20.19.0-win-x64\node-v20.19.0-win-x64;" + $env:PATH

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

The frontend will be running at: `http://localhost:5173`

#### Step 4: Access the Application

1. Open a web browser
2. Navigate to `http://localhost:5173`
3. Enter any username to login (e.g., "alice" for demo data)

### 7.3 Detailed Installation (Linux/macOS)

#### Backend Setup

```bash
# Navigate to backend
cd bbp-road-app/backend

# Create virtual environment
python3 -m venv .venv

# Activate (Linux/macOS)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn main:app --host 127.0.0.1 --port 8000
```

#### Frontend Setup

```bash
# Navigate to frontend
cd bbp-road-app/frontend

# Install Node.js dependencies
npm install

# Run development server
npm run dev
```

### 7.4 Production Build

#### Build Frontend for Production

```powershell
cd frontend
npm run build
```

This creates optimized files in `frontend/dist/` that can be served by any static file server.

### 7.5 Configuration

#### Backend Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `--host` | 127.0.0.1 | Server bind address |
| `--port` | 8000 | Server port |
| `OSRM_BASE_URL` | router.project-osrm.org | OSRM server URL |
| `OSRM_TIMEOUT` | 10.0 | OSRM request timeout (seconds) |

#### Frontend Configuration

Edit `frontend/.env` or `frontend/.env.local`:

```env
VITE_API_BASE=http://127.0.0.1:8000/api
```

### 7.6 Troubleshooting

| Issue | Solution |
|-------|----------|
| **Port 8000 in use** | Change port: `uvicorn main:app --port 8001` |
| **CORS errors** | Ensure backend is running on 127.0.0.1:8000 |
| **npm install fails** | Delete `node_modules` and `package-lock.json`, retry |
| **Map not loading** | Check internet connection (requires OpenStreetMap tiles) |
| **OSRM timeout** | Increase timeout in code or use fallback routes |
| **Python not found** | Install Python 3.10+ and add to PATH |

### 7.7 Verification Steps

After installation, verify the system is working:

1. **Backend Health Check**:
   ```
   curl http://127.0.0.1:8000/
   # Expected: {"ok": true, "message": "BBP backend ready"}
   ```

2. **API Documentation**:
   - Open `http://127.0.0.1:8000/docs` in browser
   - Should display Swagger UI

3. **Frontend**:
   - Open `http://localhost:5173`
   - Login with username "alice"
   - Dashboard should show demo data

---

## 8. Effort Spent

### 8.1 Individual Effort

| Team Member | Task | Hours |
|-------------|------|-------|
| [Hu Xu Yan] | Backend API Development | XX |
| [Hu Xu Yan] | Frontend Development | XX |
| [Hu Xu Yan] | OSRM Integration | XX |
| [Hu Xu Yan] | Testing | XX |
| [Hu Xu Yan] | Documentation | XX |
| **[Hu Xu Yan] Total** | | **XX** |
| | | |
| [Team Member 2] | [Tasks] | XX |
| **[Team Member 2] Total** | | **XX** |
| | | |
| [Team Member 3] | [Tasks] | XX |
| **[Team Member 3] Total** | | **XX** |

### 8.2 Effort Summary

| Phase | Hours | Percentage |
|-------|-------|------------|
| Requirements Analysis | X | X% |
| Design | X | X% |
| Implementation | X | X% |
| Testing | X | X% |
| Documentation | X | X% |
| **Total** | **XX** | **100%** |

### 8.3 Generative AI Usage Declaration

In accordance with course requirements, we declare the use of Generative AI (GitHub Copilot / Claude) in the following capacities:

| Task | AI Tool | Input (Prompt) | Output | Verification Method |
|------|---------|----------------|--------|---------------------|
| Code Documentation | GitHub Copilot | "Add docstrings to routing functions" | Function documentation | Manual review, accuracy check |
| ITD Document Drafting | Claude | Project code + ITD requirements | Document structure and content | Manual review, fact verification |
| Test Case Generation | Claude | "Generate system test cases for route planning" | Test case templates | Execution and validation |
| Code Review | GitHub Copilot | Code snippets for review | Improvement suggestions | Manual assessment |

**Verification Process**:
1. All AI-generated code was reviewed for correctness
2. AI-generated documentation was verified against actual implementation
3. Test cases were executed to confirm validity
4. No AI output was used without human verification

---

## 9. References

### 9.1 Technical Documentation

1. **FastAPI Documentation** - https://fastapi.tiangolo.com/
2. **React Documentation** - https://react.dev/
3. **TypeScript Documentation** - https://www.typescriptlang.org/docs/
4. **Vite Documentation** - https://vitejs.dev/
5. **Leaflet Documentation** - https://leafletjs.com/reference.html
6. **React-Leaflet Documentation** - https://react-leaflet.js.org/
7. **OSRM API Documentation** - http://project-osrm.org/docs/v5.24.0/api/
8. **Pydantic Documentation** - https://docs.pydantic.dev/

### 9.2 Course Materials

1. **RASD Document** - Requirements Analysis and Specification Document (BBP Project)
2. **DD Document** - Design Document (BBP Project)
3. **Course Slides** - Software Engineering 2, Politecnico di Milano

### 9.3 Standards

1. **REST API Design Guidelines** - https://restfulapi.net/
2. **GeoJSON Specification** - RFC 7946
3. **Polyline Encoding** - Google Polyline Algorithm

### 9.4 Tools

1. **Visual Studio Code** - IDE
2. **Git** - Version Control
3. **Postman** - API Testing
4. **Chrome DevTools** - Frontend Debugging

---

## Appendix A: API Endpoint Reference

### A.1 User Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/users` | Create or get user |
| GET | `/api/users` | List all users |
| GET | `/api/users/{id}/settings` | Get user settings |
| PUT | `/api/users/{id}/settings` | Update all settings |
| PATCH | `/api/users/{id}/settings` | Partial update settings |

### A.2 Segment Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/segments` | List all segments |
| POST | `/api/segments` | Create segment |
| GET | `/api/segments/{id}/aggregate` | Get aggregation result |
| POST | `/api/segments/{id}/auto-detect` | Run auto-detection |
| POST | `/api/segments/{id}/apply-detection` | Apply detection result |

### A.3 Report Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/segments/{id}/reports` | List reports for segment |
| POST | `/api/segments/{id}/reports` | Create report |
| POST | `/api/reports/{id}/confirm` | Confirm report |
| POST | `/api/reports/batch-confirm` | Batch confirm |

### A.4 Trip Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/trips` | List trips |
| POST | `/api/trips` | Create trip |
| GET | `/api/trips/{id}` | Get trip details |
| DELETE | `/api/trips/{id}` | Delete trip |

### A.5 Route Planning Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/routes` | Preview routes |
| POST | `/api/path/search` | Search routes with scoring |

### A.6 Utility Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/stats` | Get statistics |
| GET | `/api/weather` | Get weather data |
| GET | `/api/i18n/translations` | Get translations |
| GET | `/api/i18n/languages` | Get available languages |
| POST | `/api/aggregation/trigger` | Trigger bulk aggregation |

---

*Document generated: January 30, 2026*

*End of Document*

# BBP Road Application

A comprehensive road condition monitoring and route planning system built with FastAPI (Python) backend and React/TypeScript frontend. This application enables cyclists to report road conditions, plan safe routes, and contribute to a community-driven road quality database.

## System Architecture

- **Backend**: FastAPI with in-memory data storage
- **Frontend**: React + TypeScript + Vite
- **External Services**: OSRM (Open Source Routing Machine) for real road geometry

## Prerequisites

- Python 3.10+
- Node.js 20.x+
- npm 9.x+

## Installation

### Backend Setup

```bash
cd bbp-road-app/backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8000
```

### Frontend Setup

```bash
cd bbp-road-app/frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173` and communicates with the backend at `http://127.0.0.1:8000`.

## Core Features

### User Management
- User registration and authentication via username
- Persistent user settings and preferences
- Multi-language support (English, Chinese, Italian)

### Road Segment Management
- Create and manage road segments with status indicators
- Status classification: Optimal, Medium, Suboptimal, Maintenance
- Obstacle reporting and tracking

### Report System
- Submit condition reports for road segments
- Report confirmation workflow
- Weighted voting algorithm for status aggregation

### Trip Planning
- Create and track cycling trips
- Real-time route geometry from OSRM
- Trip history with distance and duration tracking

## Advanced Features

### OSRM Routing Integration
The system integrates with OSRM public API for accurate road geometry:
- Bicycle-optimized routing profile
- Multiple alternative route generation
- Automatic fallback to geometric interpolation when OSRM is unavailable

### Route Planning with Quality Scoring
Implements a "Generate & Evaluate" algorithm for optimal route selection:

**Candidate Generation**
1. Direct route via OSRM
2. Alternative routes via perpendicular waypoints
3. Deduplication of similar routes (>80% coordinate overlap)

**Scoring Criteria**
- `safety_first`: Prioritizes road quality, penalizes maintenance zones
- `shortest`: Optimizes for minimum distance
- `balanced`: Weighted combination of distance and quality

**Route Tags**
- Recommended, Alternative, Fastest, Best Surface, Bumpy, Road Work

### Weather Service
Mock weather service with deterministic generation:
- Location and time-based weather conditions
- Cycling-friendly recommendations
- Temperature, wind speed, humidity, and rain probability

### Internationalization (i18n)
Complete localization support:
- English (en), Chinese (zh), Italian (it)
- Localized UI labels, error messages, and route tags
- User language preference persistence

### Privacy By Design
Location obfuscation for user privacy:
- Configurable obfuscation radius (~150m)
- Three methods: noise injection, grid snapping, coordinate truncation
- Separation of private and public location data

### Data Aggregation
Automated segment status updates:
- Weighted voting based on report freshness and confirmation status
- Keyword-based sentiment analysis
- Configurable aggregation thresholds

### Auto-Detection System
Sensor-based road condition detection:
- Accelerometer data analysis
- Severity classification: Severe (>25 m/s²), Pothole (>15 m/s²), Bump (>8 m/s²)
- Speed validation for false positive prevention
- Confidence scoring with GPS accuracy adjustment

## API Reference

### User Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/users` | Create new user |
| GET | `/api/users/{id}` | Get user by ID |
| GET | `/api/users/{id}/settings` | Get user settings |
| PUT | `/api/users/{id}/settings` | Update user settings |

### Segment Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/segments` | Create segment |
| GET | `/api/segments` | List all segments |
| GET | `/api/segments/{id}` | Get segment by ID |
| PATCH | `/api/segments/{id}` | Update segment |
| POST | `/api/segments/{id}/auto-detect` | Auto-detect segment status |
| GET | `/api/segments/{id}/aggregate` | Aggregate segment reports |

### Report Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/segments/{id}/reports` | Create report |
| GET | `/api/segments/{id}/reports` | List segment reports |
| POST | `/api/reports/{id}/confirm` | Confirm report |

### Trip Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/trips` | Create trip |
| GET | `/api/trips` | List all trips |
| GET | `/api/trips/{id}` | Get trip by ID |

### Route Planning Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/routes` | Preview route alternatives |
| POST | `/api/path/search` | Route planning with scoring |

### Utility Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/weather` | Get weather for location |
| GET | `/api/stats` | Dashboard statistics |
| GET | `/api/i18n/translations` | Get translations |
| GET | `/api/i18n/languages` | Get supported languages |
| POST | `/api/aggregation/trigger` | Trigger data aggregation |

## Data Persistence

This application uses in-memory storage. All data is reset when the backend service restarts. For production deployment, integrate a persistent database solution.

## Configuration

### Backend Configuration
- `OSRM_BASE_URL`: OSRM service endpoint (default: public OSRM)
- `OSRM_TIMEOUT`: Request timeout in seconds (default: 10.0)
- `PRIVACY_FUZZ_METERS`: Location obfuscation radius (default: 150)

### Frontend Configuration
- API endpoint configured in Vite proxy settings
- Dark mode and language preferences stored in user settings

## License

This project is developed for educational purposes as part of the Software Engineering 2 course.

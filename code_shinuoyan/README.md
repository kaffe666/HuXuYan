# BBP Prototype (Route B)

An interactive GIS-based path planning and traffic reporting system prototype.

---

## 📖 Project Overview

This project is a web-based prototype designed to demonstrate **crowdsourced traffic reporting** and **dynamic path planning**. It simulates a scenario where users can report road obstacles, and the system calculates routes based on road conditions.

The application features a **FastAPI** backend for data processing and a **Leaflet.js** frontend for map visualization.

---

## ✨ Key Features

* **🗺️ Interactive Map**
    * Real-time map visualization using OpenStreetMap & Leaflet.
    * Dynamic rendering of routes and markers.

* **🚧 Segment Management**
    * Define road segments with statuses (e.g., `optimal`, `suboptimal`).
    * Mark obstacles on specific coordinates.

* **📢 Traffic Reporting System**
    * Submit user reports (Notes) for specific road segments.
    * **Verification Logic**: Confirm reports to validate road conditions.
    * **Data Aggregation**: View statistics on total vs. confirmed reports.

* **📍 Route Planning (Route B Algorithm)**
    * **Trip Calculation**: Calculates distance (Haversine formula) and estimated duration.
    * **Multi-Route Preview**: Automatically generates alternative routes (GeoJSON) alongside the direct path for user selection.

---

## 🛠️ Technology Stack

| Component | Technology |
| :--- | :--- |
| **Backend** | Python 3.9+, FastAPI, Pydantic |
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla), Leaflet.js |
| **Database** | SQLite / In-memory storage (for prototyping) |
| **Server** | Uvicorn (ASGI Server) |

---

## 🚀 Quick Start Guide

Follow these instructions to set up and run the project locally.

### 1. Prerequisites
* Python 3.8 or higher installed.
* Git (optional, for cloning).

### 2. Installation
Navigate to the project root directory (where `requirements.txt` is located) and install dependencies:

```bash
pip install -r requirements.txt
3. Running the Server
Start the FastAPI server using Uvicorn. Make sure you are in the folder containing the app directory:

Bash
uvicorn app.main:app --reload
4. Access the Application
Once the server is running, open your browser:

Main Interface: http://127.0.0.1:8000

API Documentation: http://127.0.0.1:8000/docs

📂 Project Structure
Plaintext
.
├── app/
│   ├── main.py          # Core Backend Logic (FastAPI)
│   └── static/          # Frontend Assets
│       ├── index.html   # User Interface
│       └── app.js       # Map Logic & API Integration
├── bbp.db               # Database File
├── requirements.txt     # Python Dependencies
└── README.md            # Project Documentation
👥 Team Members
[Member Name 1]: Backend Development & Algorithms

[Member Name 2]: Frontend UI & Map Integration

[Member Name 3]: Database Design & Documentation

📄 License
This project is for educational purposes only.

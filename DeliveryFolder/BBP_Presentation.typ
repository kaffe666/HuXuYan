// BBP Project Presentation - University Theme (Touying)
// Best Bike Paths (BBP) - Project Demo Slides

#import "@preview/touying:0.5.5": *
#import themes.university: *

#let vemp = none

#show: university-theme.with(
  aspect-ratio: "16-9",
  config-info(
    title: [Best Bike Paths (BBP)],
    subtitle: [Road Condition Monitoring & Route Planning System],
    author: [Kaifei Xu · Shinuo Yan · Yanglin Hu],
    date: [February 18, 2026],
    institution: [Politecnico di Milano - Software Engineering 2],
  ),
  config-colors(
    primary: rgb("#1e40af"),
    secondary: rgb("#3b82f6"),
    tertiary: rgb("#93c5fd"),
  ),
)

#set text(font: "New Computer Modern", size: 18pt)

// ============== TITLE SLIDE ==============
#title-slide()
// ============== SLIDE 10: DASHBOARD ==============

// ============== SLIDE 2: SYSTEM OVERVIEW ==============
== System Overview

#grid(
  columns: (1fr, 1fr),
  gutter: 30pt,
  [
    === Architecture
    
    #align(center)[
      #block(fill: rgb("#dbeafe"), radius: 6pt, inset: 12pt, width: 100%)[
        *Frontend* - Streamlit + Folium Maps
      ]
      #v(0.3em)
      #text(size: 14pt)[↕ REST API]
      #v(0.3em)
      #block(fill: rgb("#dcfce7"), radius: 6pt, inset: 12pt, width: 100%)[
        *Backend* - Python + FastAPI
      ]
      #v(0.3em)
      #text(size: 14pt)[↕]
      #v(0.3em)
      #block(fill: rgb("#fef3c7"), radius: 6pt, inset: 12pt, width: 100%)[
        *External* - OSRM Routing | OpenStreetMap
      ]
    ]
  ],
  [
    === Live Demo
    
    #block(
      fill: rgb("#ecfdf5"),
      stroke: 2pt + rgb("#10b981"),
      radius: 10pt,
      inset: 18pt,
      width: 100%,
    )[
      #text(weight: "bold", size: 16pt, fill: rgb("#059669"))[Cloud Deployment]
      #v(0.5em)
      #text(size: 13pt, fill: rgb("#1e40af"))[
        `https://huxuyan-fq8a9pdhxknpmuird65kfg.streamlit.app`
      ]
    ]
    
    #v(0.8em)
    
    === Key Features
    - Road condition monitoring & reporting
    - Intelligent route planning with quality scores
    - Community-driven weighted voting system
    - Privacy-by-design (GDPR compliant)
  ],
)
== Dashboard - Overview

#grid(
  columns: (1.4fr, 1fr),
  gutter: 20pt,
  [
    #image("images/dashboard&lightmode.png", height: 85%)
  ],
  [
    === Key Metrics
    - *Total Segments*
    - *Total Reports*  
    - *Total Trips*
    - *Active Users*
    
    === Live Weather
    - Temperature & Conditions
    - Wind Speed
    - Rain Chance
    - Cycling recommendation
  ],
)


// ============== SLIDE 7: ROUTE PLANNING ==============
== Route Planning - Input

#grid(
  columns: (1.4fr, 1fr),
  gutter: 20pt,
  [
    #image("images/route.planning.png", height: 85%)
  ],
  [
    === How to Use
    1. *Search* origin
    2. *Search* destination
    3. Select *mode*:
       - Safety First
       - Shortest
       - Balanced
    4. Click *Find Routes*
    
    === Weather
    #block(fill: rgb("#fef3c7"), radius: 6pt, inset: 8pt)[
      Sunny, 19.1°C \
      _"Great for cycling!"_
    ]
  ],
)

// ============== SLIDE 4: ROAD SEGMENTS ==============
== Road Segments - Map View

#grid(
  columns: (1.8fr, 1fr),
  gutter: 20pt,
  [
    #image("images/segment.png", height: 85%)
  ],
  [
    === Features
    - *Interactive map* with markers
    - *Create segments* via search
    - *Track obstacles*
    
    === Status Colors
    #table(
      columns: (auto, 1fr),
      stroke: 0.5pt + gray,
      inset: 6pt,
      [#text(fill: rgb("#16a34a"))[●]], [Optimal],
      [#text(fill: rgb("#eab308"))[●]], [Fair],
      [#text(fill: rgb("#dc2626"))[●]], [Poor],
      [#text(fill: rgb("#6b7280"))[●]], [Maintenance],
    )
  ],
)
// ============== SLIDE 8: ROUTE RESULTS ==============
== Route Planning - Results
#v(-0.5em)
#align(center)[
  #image("images/route.planning_detail.jpg", height: 102%)
]
#v(-3em)

#align(center)[*Route Options*: Recommended · Best Surface · Fastest · Alternative]
// ============== SLIDE 5: SEGMENT LIST ==============
== Road Segments - List View

#align(center)[
  #image("images/segments.list.png", height: 80%)
]

#align(center)[*Searchable table* - ID, Road Name, Status, Obstacle Type]

// ============== SLIDE 6: REPORTS ==============
== Condition Reports - Community Voting

#grid(
  columns: (1.5fr, 0.7fr),
  gutter: 30pt,
  [
    #image("images/report.png", height: 60%)
  ],
  [
    === Submit Reports
    1. Select segment
    2. Slide condition bar
    3. Add notes (optional)
    4. Submit
    
    === Weighted Voting
    #table(
      columns: (1fr, auto),
      stroke: 0.5pt + gray,
      inset: 6pt,
      [*< 7 days*], [1.0],
      [*7-30 days*], [0.7],
      [*> 30 days*], [0.3],
      [*+Confirm*], [+0.2],
    )
  ],
)




// ============== SLIDE 9: TRIPS & AUTO-DETECTION ==============
== Trips & Auto-Detection

#grid(
  columns: (0.5fr, 0.5fr),
  gutter: 5pt,
  [
    #align(center)[#image("images/trips.jpg", height: 80%)]
    #v(-1em)
    *Trip Management* - Create trips, track cycling journeys with privacy protection (±150m blur)
  ],
  [
    #align(center)[#image("images/aut.detection.jpg", height: 80%)]
    #v(-1em)
    *Auto-Detection* - GPS + Accelerometer detects bumps automatically
  ],
)

// ============== SLIDE 3: USER SETTINGS ==============
== User Settings - Personalization

#grid(
  columns: (1fr, 1.5fr, 1fr),
  gutter: 20pt,
  [
    #align(center)[
      #image("images/setting.png", height: 65%)
      _Light Mode_
    ]
  ],
  [
    #align(center)[
      #image("images/settings_dark.png", height: 65%)
      _Dark Mode_
    ]
  ],
  [
    === Options
    - *Language*: EN / 中文 / IT
    - *Theme*: Light & Dark
    - *Notifications*
    - *Profile* editing
    
    === Privacy
    - Location blur: ±150m
    - Coord truncation
    - GDPR compliant
  ],
)

// ============== SLIDE 11: SUMMARY ==============
== Summary & Highlights

#grid(
  columns: (1fr, 1fr, 1fr, 1fr),
  gutter: 12pt,
  block(fill: rgb("#ecfdf5"), stroke: 1pt + rgb("#10b981"), radius: 8pt, inset: 12pt)[
    #text(weight: "bold", fill: rgb("#059669"))[ Features]
    - Dashboard
    - Road Segments
    - Condition Reports
    - Route Planning
    - Trip Recording
    - Auto-Detection
    - User Settings
  ],
  block(fill: rgb("#eff6ff"), stroke: 1pt + rgb("#3b82f6"), radius: 8pt, inset: 12pt)[
    #text(weight: "bold", fill: rgb("#2563eb"))[ Tech Stack]
    - Python 3.10+
    - FastAPI
    - Streamlit
    - OSRM Routing
    - Folium/Leaflet
    - OpenStreetMap
  ],
  block(fill: rgb("#fef3c7"), stroke: 1pt + rgb("#f59e0b"), radius: 8pt, inset: 12pt)[
    #text(weight: "bold", fill: rgb("#d97706"))[ Privacy]
    - Location blur ±150m
    - Coord truncation
    - Trip sanitization
    - GDPR compliant
  ],
  block(fill: rgb("#fce7f3"), stroke: 1pt + rgb("#ec4899"), radius: 8pt, inset: 12pt)[
    #text(weight: "bold", fill: rgb("#db2777"))[ UX Design]
    - 3 Languages
    - Dark/Light Mode
    - Mobile Ready
    - Geocoding Search
  ],
)

// ============== SLIDE 12: THANK YOU ==============
== 

#v(1fr)
#align(center)[
  #text(40pt, weight: "bold", fill: rgb("#1e40af"))[
    Thank You!
  ]
  
  #v(1em)
  
  #text(22pt)[Questions & Live Demo]
  
  #v(1.5em)
  
  #block(
    fill: rgb("#1e40af"),
    radius: 12pt,
    inset: 25pt,
  )[
    #text(fill: white, size: 18pt)[
      Try it now: #text(fill: rgb("#93c5fd"))[`https://huxuyan-fq8a9pdhxknpmuird65kfg.streamlit.app`]
    ]
  ]
  
  #v(1.5em)
  
  #text(16pt, fill: gray)[
    Kaifei Xu · Shinuo Yan · Yanglin Hu \
    Politecnico di Milano | Software Engineering 2 | 2026
  ]
]
#v(1fr)

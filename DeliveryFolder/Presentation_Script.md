# BBP Presentation Script
## 演示稿 / Demo Script

---

### Slide 1: Title
**（展示封面页）**

> "Good morning/afternoon, Professor. Today we're presenting Best Bike Paths, or BBP — a road condition monitoring and route planning system designed for cyclists."

---

### Slide 2: System Overview
**（停留在架构图页面）**

> "Our system uses a three-tier architecture: a Streamlit frontend with interactive maps, a FastAPI backend handling business logic, and integration with OSRM for real bicycle routing data from OpenStreetMap."

> "The app is already deployed on Streamlit Cloud — you can try it right now at this URL."

**（可指向URL）**

---

### Slide 3: Dashboard
**（点击 Dashboard 菜单）**

> "This is the Dashboard — the main landing page. Users can see key statistics: total road segments monitored, user reports submitted, trips recorded, and active users."

> "We also integrate a weather service showing current conditions and cycling recommendations."

---

### Slide 4: Route Planning - Input
**（点击 Route Planning 菜单）**

> "Route Planning is a core feature. Users enter origin and destination — they can either search by place name using geocoding, or click directly on the map."

**（演示：在搜索框输入地名，如 "Loreto Milan"）**

> "There are three optimization modes: Safety First avoids bad roads, Shortest finds minimum distance, and Balanced provides a compromise."

---

### Slide 5: Road Segments - Map
**（点击 Segments 菜单）**

> "This is the Segments page showing an interactive map. Each marker represents a road segment with color-coded status: green for optimal, yellow for fair, red for poor, and gray for maintenance."

**（点击地图上的标记点）**

> "Users can create new segments by searching a location or clicking on the map."

---

### Slide 6: Route Planning - Results
**（返回 Route Planning，点击 Find Routes）**

> "After clicking Find Routes, our Generate & Evaluate algorithm provides multiple route options. Each route shows distance, duration, and a quality score out of 100."

> "Routes are tagged: Recommended, Best Surface, Fastest, or Alternative — helping users choose based on their priorities."

---

### Slide 7: Road Segments - List
**（点击 Segments 页面的 List 视图）**

> "The List View shows all segments in a searchable table with ID, road name, current status, and obstacle type. Users can filter and manage segment data efficiently."

---

### Slide 8: Reports
**（点击 Reports 菜单）**

> "The Reports page lets users submit road condition reports. Select a segment, slide the condition bar from Suboptimal to Optimal, add optional notes, and submit."

**（演示：选择segment，滑动条件滑块）**

> "We use a weighted voting algorithm — fresh reports within 7 days have full weight, older reports gradually decrease. Confirmed reports get a bonus."

---

### Slide 9: Trips & Auto-Detection
**（点击 Trips 菜单，再点击 Auto-Detection）**

> "Users can create and track cycling trips. For privacy, start and end points are automatically blurred by 150 meters — GDPR compliant."

**（切换到 Auto-Detection 页面）**

> "Auto-Detection uses GPS and accelerometer data to detect road bumps automatically. Severity thresholds: Severe above 25, Pothole above 15, Bump above 8 m/s²."

---

### Slide 10: Settings
**（点击 Settings 菜单）**

> "Users can personalize their experience: choose between English, Chinese, or Italian; toggle Dark or Light mode; manage notifications and profile settings."

**（演示：切换深色模式）**

> "All privacy settings are here — location blur is enabled by default."

---

### Slide 11: Summary
**（展示总结页）**

> "To summarize: we've implemented all core features — Dashboard, Segments, Reports, Route Planning, Trips, Auto-Detection, and Settings."

> "Our tech stack includes Python FastAPI, Streamlit, OSRM routing, and Folium maps. Privacy is built-in with location blur and GDPR compliance."

---

### Slide 12: Thank You
**（展示结束页）**

> "Thank you for your attention. The app is live — feel free to try it now. We're happy to answer any questions or give a live demo."

**（准备回答问题或进行现场演示）**

---

## 快速操作备忘 / Quick Action Reference

| 功能 | 操作步骤 |
|------|----------|
| Dashboard | 点击侧边栏 "Dashboard" |
| Route Planning | 点击 "Route Planning" → 输入起点终点 → Find Routes |
| Segments Map | 点击 "Segments" → 查看地图标记 |
| Segments List | 点击 "Segments" → 切换 List 视图 |
| Reports | 点击 "Reports" → 选择segment → 滑动条 → Submit |
| Trips | 点击 "Trips" → 创建行程 |
| Auto-Detection | 点击 "Auto-Detection" → 查看传感器数据 |
| Settings | 点击 "Settings" → 切换语言/深色模式 |
| 深色模式 | Settings → Dark Mode 开关 |
| 语言切换 | Settings → Language 下拉菜单 |

---

## 演示注意事项 / Demo Tips

1. **提前打开网页** - 确保 `https://huxuyan-fq8a9pdhxknpmuird65kfg.streamlit.app` 已加载
2. **用 "alice" 登录** - 有预设演示数据
3. **Route Planning 演示** - 用 "Loreto Milan" 到 "Duomo Milan" 效果最好
4. **地图加载慢** - 等几秒让Leaflet地图完全加载
5. **备用方案** - 如果云端慢，可以用本地部署版本

---

*Presentation Time: ~8-10 minutes*

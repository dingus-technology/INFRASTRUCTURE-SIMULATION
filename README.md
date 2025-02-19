<h1 align="center" style="display: flex; align-items: center; justify-content: center; gap: 10px;">
  <img src="assets/logo-dark.png" alt="Logo" width="50">
  <span>Monitoring Simulation Data with Loki, Prometheus & Grafana</span>
</h1>

<p align="center">
  <img src="assets/grafana-demo-ui.png" alt="Grafana UI" width="850">
</p>

## 🚀 Overview
This guide explains how to set up **Loki**, **Prometheus**, and **Grafana** using Docker Compose to monitor CPU load data from a Python application.

🔹 **Prometheus** - Scrapes metrics from the app  
🔹 **Loki** - Collects & indexes logs  
🔹 **Grafana** - Visualizes the data  

---

## 📌 Prerequisites
Ensure you have the following installed:
- [Docker & Docker Compose](https://docs.docker.com/get-docker/)
- [Colima](https://github.com/abiosoft/colima) (for Mac users)


---

## 🚀 Start the Monitoring Stack
Run the following command to build and start the services:

```bash
docker compose up --build
```

---

## 🔍 Verify Prometheus Scraping Data
1. Open **Prometheus UI** → [http://localhost:9090](http://localhost:9090)
2. Navigate to **"Status" > "Targets"** to check if `sanitised-data` is `UP`
3. Run a query in PromQL:

   ```promql
   cpu_load
   ```

   You should see CPU load data in real-time!

---

## 📊 Connect Grafana to Prometheus
1. Open **Grafana UI** → [http://localhost:3000](http://localhost:3000)
2. **Login** with:
   - Username: `admin`
   - Password: `admin`
3. Navigate to **"Configuration" > "Data Sources"**
4. Click **"Add Data Source"** and select **Prometheus**
5. Set the **URL**:

   ```
   http://host.docker.internal:9090
   ```

6. Click **"Save & Test"** 🎯

---

## 📈 Create a Grafana Dashboard
1. Go to **"Create" > "Dashboard"**
2. Click **"Add a new panel"**
3. In the **Metrics** section, enter:

   ```promql
   cpu_load
   ```

4. Click **"Run query"** to visualize CPU load
5. Customize the graph, then click **"Save"** ✅

---

## 📜 Configure Loki for Log Monitoring
1. Navigate to **"Logs"** in Grafana
2. Select **"Loki"** as the **"Data Source"**
3. Run a log query to filter logs:

   ```logql
   {app="sanitised-data"}
   ```

---

## 🎉 Done!  
Your **sanitised-data service** is now fully monitored with **Prometheus, Loki & Grafana**! 🚀  

✅ **Metrics →** Tracked via **Prometheus**  
✅ **Logs →** Indexed with **Loki**  
✅ **Visualization →** Displayed in **Grafana**  

---

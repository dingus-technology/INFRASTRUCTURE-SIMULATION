# **Monitoring Fake Data with Prometheus & Grafana**

This guide explains how to set up **Prometheus** and **Grafana** in Docker Compose to monitor sanitised CPU load data exposed by a Python application.


## **Start the Stack**
Run the following command to start everything:

```bash
docker compose up --build
```

---

## **Verify Prometheus is Scraping Data**
1. Open **Prometheus UI**: [http://localhost:9090](http://localhost:9090)
2. Click on **"Status" > "Targets"**, ensure `sanitised-data` is `UP`
3. Run a test query:

   ```promql
   cpu_load
   ```

---

## **Connect Grafana to Prometheus**
1. Open **Grafana**: [http://localhost:3000](http://localhost:3000)
2. **Login** with:
   - Username: `admin`
   - Password: `admin`
3. Go to **"Configuration" > "Data Sources"**.
4. Click **"Add Data Source"**.
5. Select **Prometheus**.
6. Set the URL as:

   ```
   http://prometheus:9090
   ```

7. Click **"Save & Test"**.

---

## **Create a Dashboard in Grafana**
1. Go to **"Create" > "Dashboard"**.
2. Click **"Add a new panel"**.
3. In the **Metrics** section, enter:

   ```promql
   cpu_load
   ```

4. Click **"Run query"**.
5. Customize the graph as needed.
6. Click **"Save"** and name your dashboard.

---

## **🎉 Done!**
Your **sanitised-data service** is being monitored with **Prometheus** and visualized in **Grafana**! 🚀


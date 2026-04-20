# RetroScan AI

**RetroScan AI** is a state-of-the-art, physics-first retroreflectivity measurement system designed for national highways. It simulates the integration of IR cameras, LiDAR, and Artificial Intelligence (YOLOv8) to measure the retroreflectivity (RA) of road infrastructure such as markings, signs, and studs in real-time, matching highway speeds. 

This project aims to automate highway compliance monitoring against IRC (Indian Roads Congress) standards, specifically IRC 67 and IRC 35.

---

## 🎯 Key Features

1. **Physical-Based RA Calculation**: Computes accurate Retroreflectivity (RA) values using photometry principles and inverse-square law equations.
2. **Ambient Light Elimination**: Conceptually uses IR modulated differential imaging (Lock-in Detection) to isolate the retroreflected signal from ambient sunlight.
3. **Advanced Object Detection**: Integrates with [YOLOv8](https://github.com/ultralytics/ultralytics) to precisely identify and classify road markings, sign boards, and road studs in real-time.
4. **Automated Compliance Verification**: Automatically validates RA measurements against established IRC 67 and IRC 35 safety thresholds (Safe, Warning, Danger).
5. **GIS Intelligence Dashboard**: Features a comprehensive Streamlit dashboard for real-time map visualization, tracking the precise lat/lng location of compromised highway assets.
6. **Predictive Maintenance**: Embeds an LSTM-based predictive controller stub to estimate the degradation curve and predict days-to-failure for highway infrastructure.

---

## 🏗️ System Architecture & Workflow

The simulation runs through a series of cohesive engines and processors:

- **Hardware Sensors (Telemetry)**: Assimilates real-time GPS coordinates, environmental weather conditions, and LiDAR distance measurements.
- **Vision Engine**: Runs object detection (YOLOv8) on video frames to detect targets and extracts mean pixel luminance.
- **Physics Engine**: Merges camera calibration, observation angles, luminance, and illuminance (IR intensity) to compute the RA value. Adjusts dynamically for weather (Wet, Fog).
- **Compliance & Prediction**: Evaluates RA values for IRC compliance and pushes the data to an LSTM model to predict future lifespan.
- **GIS Dashboard**: A live-updating portal visualizing safe and at-risk assets directly on a geographic map.

---

## 📂 Project Structure

```text
RetroScanAI/
├── core/
│   ├── config.py             # System thresholds and geometric configurations
│   ├── physics_engine.py     # RA value computation and IRC compliance logic 
│   └── vision_engine.py      # YOLOv8 object detection and bounding box processing
├── dashboard/
│   └── app.py                # Streamlit GIS dashboard for real-time visualization
├── data/
│   └── mock_sensors.py       # Simulates GPS, LiDAR, and weather sensor data
├── predictive/
│   └── lstm_model.py         # PyTorch LSTM predictive maintenance module
├── scripts/
│   ├── generate_dummy_video.py # Utility to generate a sample video feed
│   └── train_lstm.py         # Utility for training the LSTM model
├── db/
│   └── latest_run.json       # Generated output database from pipeline runs
├── main.py                   # Central entry point for the RetroScan AI pipeline
└── requirements.txt          # Python dependencies
```

---

## 🚀 Installation & Setup

### Prerequisites

Ensure you have **Python 3.8+** installed on your system.

### 1. Clone the repository

If you haven't already, clone the main repository to your local machine.

```bash
git clone https://github.com/992manav/RetroScan.git
cd RetroScan/RetroScanAI
```

### 2. Install Dependencies

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

*(Optional but recommended)* Use a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### 3. Generate Dummy Video Data

Before running the main pipeline, ensure you have a sample video source. The project includes a script to generate one:

```bash
python scripts/generate_dummy_video.py
```

---

## 🖥️ Usage

The project is split into two main executables: the core data pipeline and the GIS visualization dashboard.

### 1. Run the Main Pipeline

Execute the main pipeline to begin analyzing the video feed, processing sensor data, and generating RA intelligence.

```bash
python main.py
```

**What happens?**
- The pipeline processes the video frame-by-frame.
- It detects road signs, markings, and studs using YOLOv8.
- Calculates Retroreflectivity (RA) and determines IRC compliance.
- Saves the results locally into `db/latest_run.json`.
- Press `q` while focused on the video window to stop the stream safely.

### 2. Launch the GIS Dashboard

Open a new terminal session, ensure your virtual environment is active, and launch the Streamlit dashboard:

```bash
cd RetroScanAI
streamlit run dashboard/app.py
```

**Dashboard Features:**
- **KPI Metrics**: High-level overview of total scanned assets categorized by safety status.
- **Interactive Map**: Folium-based map rendering assets based on their exact GPS coordinates, color-coded by safety status (Green = Safe, Orange = Warning, Red = Danger).
- **Predictive Analytics**: A dedicated panel showing assets predicted to fail within the next 30 days based on LSTM projections.
- **Detailed Records**: Full tabular data of all processed scans for detailed review.

---

## 🛠️ Technology Stack

- **Computer Vision & AI**: PyTorch, Ultralytics YOLOv8, OpenCV
- **Physics Modeling & Math**: NumPy, internal robust formulas for Luminance vs Illuminance
- **Dashboard & Visualization**: Streamlit, Folium, Pandas
- **Data Engineering**: JSON data lakes, modular Python structure

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

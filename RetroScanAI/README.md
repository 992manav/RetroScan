# RetroScan AI

RetroScan AI is a physics-first retroreflectivity measurement system for national highways. It uses IR cameras, LiDAR, and AI (YOLOv8) to measure the retroreflectivity (RA) of road markings, signs, and studs in real-time at highway speeds.

## Features
- **Ambient Light Elimination**: Uses IR modulated differential imaging (Lock-in Detection) to isolate the retroreflected signal.
- **Object Detection**: Integrates with YOLOv8 to detect road markings, sign boards, and road studs.
- **Physics-Based RA Calculation**: Calculates RA values using photometry and inverse-square law equations.
- **IRC Compliance Check**: Automatically checks RA values against IRC 67 and IRC 35 standards.
- **GIS Dashboard Integration**: Generates data points for real-time visualization on a highway map.
- **Predictive Maintenance**: Includes a stub for an LSTM-based model to predict future degradation.

## Project Structure
- `main.py`: The main entry point for the RetroScan AI pipeline.
- `data_simulator.py`: Simulates data acquisition from hardware components.
- `image_processor.py`: Handles ambient light elimination.
- `object_detector.py`: Simulates object detection (YOLOv8 stub).
- `ra_calculator.py`: Implements the RA physics calculation engine.
- `compliance_checker.py`: Checks RA values against IRC standards.
- `data_manager.py`: Manages data storage and retrieval.
- `gis_data_generator.py`: Generates GIS-ready data for visualization.
- `predictive_model_stub.py`: Conceptual stub for predictive maintenance.

## Requirements
- Python 3.x
- pandas
- numpy

## Usage
To run the RetroScan AI simulation:
```bash
python3 main.py
```
This will simulate several cycles of data acquisition, processing, and analysis, saving the results to `retroscan_data.csv`.

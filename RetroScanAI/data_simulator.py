import random
import numpy as np
import time

class DataSimulator:
    """Simulates data acquisition from RetroScan AI hardware components."""

    def __init__(self):
        print("DataSimulator initialized.")

    def simulate_data(self):
        """Simulates IR frames, LiDAR distance, GPS, and weather data."""
        # Simulate IR frames (simple grayscale images for demonstration)
        ir_frame_on = np.random.randint(0, 256, size=(100, 100), dtype=np.uint8)
        ir_frame_off = np.random.randint(0, 256, size=(100, 100), dtype=np.uint8)

        # Simulate LiDAR distance (in meters)
        lidar_distance = round(random.uniform(5, 50), 2)

        # Simulate GPS data
        gps_data = {
            "latitude": round(random.uniform(28.0, 30.0), 6),
            "longitude": round(random.uniform(75.0, 77.0), 6),
            "highway_segment_id": f"NH-{random.randint(1, 100)}-{random.randint(10, 200)}.0"
        }

        # Simulate weather conditions
        weather_conditions = ["clear", "rainy", "foggy", "night"]
        weather_data = {
            "condition": random.choice(weather_conditions),
            "temperature": round(random.uniform(10.0, 40.0), 1),
            "visibility": round(random.uniform(100, 5000), 0) # in meters
        }

        return ir_frame_on, ir_frame_off, lidar_distance, gps_data, weather_data

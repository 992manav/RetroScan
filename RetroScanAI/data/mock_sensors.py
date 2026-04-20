import random
import time

class MockSensorData:
    def __init__(self):
        # Initial starting coordinates for the vehicle (Example: NH-48 start point)
        self.lat = 28.5355 
        self.lng = 77.3910
        
    def get_lidar_distance(self):
        """Simulates distance to the detected object in meters"""
        return round(random.uniform(5.0, 30.0), 2)
        
    def get_ir_intensity(self):
        """Simulates IR Source illuminance output (mock reference value)"""
        return round(random.uniform(800.0, 1200.0), 2)
        
    def get_weather_conditions(self):
        """Simulates fetching real-time weather/visibility sensor data"""
        weather_states = ['CLEAR', 'CLEAR', 'CLEAR', 'CLEAR', 'WET', 'FOG']
        state = random.choice(weather_states)
        visibility = 1000 if state != 'FOG' else random.randint(10, 200)
        return {
            'weather': state,
            'visibility_m': visibility
        }
        
    def update_gps(self):
        """Simulates vehicle movement down the highway"""
        self.lat += random.uniform(0.0001, 0.0003)
        self.lng += random.uniform(0.0001, 0.0003)
        return self.lat, self.lng

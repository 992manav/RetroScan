import math
from core.config import (
    H1_LED_HEIGHT, H2_CAMERA_HEIGHT, WET_SURFACE_CORRECTION_FACTOR,
    FOG_CORRECTION_FACTOR_BASE, IRC_THRESHOLDS
)

class PhysicsEngine:
    def __init__(self):
        # Camera internal calibration constant (k) measured in lab (mock value)
        self.camera_calibration_constant = 0.05 

    def calculate_observation_angle(self, distance_m):
        """
        Step 1: Fixed vehicle geometry
        """
        if distance_m <= 0:
            return 0
        diff_h = H2_CAMERA_HEIGHT - H1_LED_HEIGHT
        angle_rad = math.atan(diff_h / distance_m)
        return math.degrees(angle_rad)

    def calculate_luminance(self, mean_pixel_value):
        """
        Step 2: Luminance from Calibrated Pixels (RAW frames assumption)
        """
        return mean_pixel_value * self.camera_calibration_constant

    def calculate_illuminance(self, ir_intensity, distance_m):
        """
        Step 3: Illuminance at Surface using Inverse Square Law
        """
        if distance_m <= 0:
            return 0
        return ir_intensity / (distance_m ** 2)

    def calculate_ra(self, mean_pixel_value, ir_intensity, distance_m, weather='CLEAR', visibility_m=1000):
        """
        Step 4 & 5: Final RA Value computation and IRC threshold checks
        """
        luminance = self.calculate_luminance(mean_pixel_value)
        illuminance = self.calculate_illuminance(ir_intensity, distance_m)
        
        if illuminance == 0:
            return 0
            
        # Standard Retroreflectivity Formula
        ra_value = (luminance / illuminance) * 1000  # converted to mcd
        
        # Environmental corrections (Physics-driven)
        if weather == 'WET':
            # Simulating physical switch to 1.0 degree observation angle and specular correction
            ra_value *= WET_SURFACE_CORRECTION_FACTOR
        elif weather == 'FOG':
            # Simulating switch to 1550nm IR to bypass Mie scattering
            fog_factor = FOG_CORRECTION_FACTOR_BASE * (1000 / max(10, visibility_m))
            ra_value *= fog_factor
            
        return round(ra_value, 2)

    def determine_irc_status(self, ra_value, object_type):
        """
        Compares RA against IRC 67 / IRC 35 guidelines
        """
        obj_type_key = object_type.upper().replace(' ', '_')
        if obj_type_key not in IRC_THRESHOLDS:
            return 'UNKNOWN'
            
        thresholds = IRC_THRESHOLDS[obj_type_key]
        if ra_value < thresholds['DANGER']:
            return 'DANGER'
        elif ra_value < thresholds['WARNING']:
            return 'WARNING'
        else:
            return 'SAFE'

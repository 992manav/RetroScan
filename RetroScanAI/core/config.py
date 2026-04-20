import math

# Fixed Vehicle Geometry Defaults
H1_LED_HEIGHT = 0.65  # meters
H2_CAMERA_HEIGHT = 1.20  # meters

# Environmental Correction Factors
WET_SURFACE_CORRECTION_FACTOR = 1.3  # Example logic: rain specular switch
FOG_CORRECTION_FACTOR_BASE = 1.5     # Example logic: Mie scattering adjustment

# IRC Compliance Thresholds (mcd/m2/lux)
# Defined as (DANGER_UPPER, WARNING_UPPER)
# Values >= WARNING_UPPER are SAFE.
IRC_THRESHOLDS = {
    'ROAD_MARKING': {
        'DANGER': 100,
        'WARNING': 150
    },
    'SIGN_BOARD': {
        'DANGER': 250,
        'WARNING': 375
    },
    'ROAD_STUD': {
        'DANGER': 150,
        'WARNING': 225
    }
}

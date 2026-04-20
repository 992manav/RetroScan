import numpy as np

class ImageProcessor:
    """Handles image processing, specifically ambient light elimination using differential imaging."""

    def __init__(self):
        print("ImageProcessor initialized.")

    def process_frames(self, ir_frame_on, ir_frame_off):
        """Applies differential imaging to eliminate ambient light.

        Args:
            ir_frame_on (np.array): IR frame with LED ON (retroreflection + ambient light).
            ir_frame_off (np.array): IR frame with LED OFF (ambient light only).

        Returns:
            np.array: Pure signal frame (retroreflection only).
        """
        # Simple subtraction for demonstration. In a real scenario, this would involve
        # more sophisticated alignment and calibration.
        pure_signal_frame = np.clip(ir_frame_on.astype(np.int16) - ir_frame_off.astype(np.int16), 0, 255).astype(np.uint8)
        return pure_signal_frame

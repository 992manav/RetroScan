import random
import numpy as np

class ObjectDetector:
    """Simulates object detection using YOLOv8. In a real scenario, this would integrate with a YOLOv8 model."""

    def __init__(self):
        print("ObjectDetector initialized (YOLOv8 stub).")
        self.object_types = ["road_marking", "sign_board", "road_stud"]

    def detect_objects(self, image_frame):
        """Simulates detecting objects in an image frame.

        Args:
            image_frame (np.array): The processed image frame (pure signal).

        Returns:
            list: A list of dictionaries, each representing a detected object
                  with its type and bounding box (x, y, w, h).
        """
        detected_objects = []
        num_objects = random.randint(0, 3) # Simulate detecting 0 to 3 objects

        for _ in range(num_objects):
            obj_type = random.choice(self.object_types)
            # Simulate bounding box (x, y, width, height)
            x = random.randint(0, image_frame.shape[1] - 20)
            y = random.randint(0, image_frame.shape[0] - 20)
            w = random.randint(10, min(50, image_frame.shape[1] - x))
            h = random.randint(10, min(50, image_frame.shape[0] - y))
            bbox = (x, y, w, h)
            detected_objects.append({"type": obj_type, "bbox": bbox})

        return detected_objects

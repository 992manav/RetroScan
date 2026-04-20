import cv2
import numpy as np
from ultralytics import YOLO
import os

class VisionEngine:
    def __init__(self, model_path="yolov8n.pt", confidence_threshold=0.5):
        """
        Initializes the YOLOv8 Object Detection Engine.
        """
        self.confidence_threshold = confidence_threshold
        # Load YOLOv8 model - downloads standard weights if not present locally
        print(f"[VisionEngine] Loading YOLOv8 weights from {model_path}...")
        self.model = YOLO(model_path)
        
        # Assume these classes for our specific hackathon use case.
        # COCO standard has things like 'stop sign' (11). We'll map generic detections to our 3 modes.
        self.target_classes = {
            11: 'SIGN_BOARD',    # stop sign in COCO -> Sign Board
            0: 'ROAD_MARKING',   # Mapping person -> Road marking for testing purposes on standard yolov8n
            2: 'ROAD_STUD'       # Mapping car -> Road stud for testing purposes
        }

    def process_frame(self, frame: np.ndarray):
        """
        Runs YOLOv8 inference on a BGR numpy image frame (from OpenCV).
        Calculates pixel luminance acting as proxy for raw photon count.
        """
        # Run inference
        results = self.model(frame, verbose=False)[0]
        
        detections = []
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        for box in results.boxes:
            conf = float(box.conf[0])
            if conf < self.confidence_threshold:
                continue
                
            cls_id = int(box.cls[0])
            
            # For hackathon demo using pre-trained COCO, we force a mapping.
            # In a real deployed version, self.model would be trained strictly on NHAI datasets.
            obj_type = self.target_classes.get(cls_id, 'ROAD_MARKING')
            
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            
            # Ensure within bounds
            h, w = gray_frame.shape
            y1, y2 = max(0, y1), min(h, y2)
            x1, x2 = max(0, x1), min(w, x2)
            
            if y2 <= y1 or x2 <= x1:
                continue

            # Extract region of interest
            roi = gray_frame[y1:y2, x1:x2]
            
            # Calibrated calculation of mean pixel value (Mocking photon count linearity)
            mean_pixel_value = float(np.mean(roi))
            
            detections.append({
                'box': [x1, y1, x2, y2],
                'class': obj_type,
                'confidence': conf,
                'mean_pixel_value': mean_pixel_value
            })
            
        return detections

    def draw_detections(self, frame: np.ndarray, detections: list):
        """
        Utility module to draw bounding boxes and text on the frame.
        """
        draw_frame = frame.copy()
        for det in detections:
            x1, y1, x2, y2 = det['box']
            label = f"{det['class']} Conf:{det['confidence']:.2f} Lum:{det['mean_pixel_value']:.1f}"
            cv2.rectangle(draw_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(draw_frame, label, (x1, max(y1 - 10, 0)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        return draw_frame

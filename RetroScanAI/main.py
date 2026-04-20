import time
import json
import os
import cv2
from datetime import datetime

from core.vision_engine import VisionEngine
from core.physics_engine import PhysicsEngine
from data.mock_sensors import MockSensorData
from predictive.lstm_model import PredictiveController
from core.config import IRC_THRESHOLDS

def run_pipeline(video_source="sample_highway.mp4"):
    print("Starting Detailed RetroScan AI Production Pipeline...")
    vision = VisionEngine()
    physics = PhysicsEngine()
    sensors = MockSensorData()
    lstm = PredictiveController()

    results_db = []
    
    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print(f"Error: Could not open video feed {video_source}. Please run scripts/generate_dummy_video.py first.")
        return

    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_idx += 1
        
        # 1. Hardware Sensor telemetry assimilation
        lat, lng = sensors.update_gps()
        weather_data = sensors.get_weather_conditions()
        distance_m = sensors.get_lidar_distance()
        ir_intensity = sensors.get_ir_intensity()

        print(f"\n[Frame {frame_idx}] GPS: ({lat:.4f}, {lng:.4f}) | Weather: {weather_data['weather']} | Dist: {distance_m}m")

        # 2. Run Vision inference (YOLOv8 + BBox math)
        detections = vision.process_frame(frame)

        # Draw detections for visual feedback
        display_frame = vision.draw_detections(frame, detections)
        cv2.imshow("RetroScan AI Video Stream", display_frame)

        # To avoid OpenCV GUI locking, check for 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        for det in detections:
            obj_type = det['class']
            mean_pix = det['mean_pixel_value']
            
            # 3. Physics Engine math
            ra_val = physics.calculate_ra(
                mean_pixel_value=mean_pix,
                ir_intensity=ir_intensity,
                distance_m=distance_m,
                weather=weather_data['weather'],
                visibility_m=weather_data['visibility_m']
            )

            # 4. Check IRC Compliance status
            status = physics.determine_irc_status(ra_val, obj_type)

            # 5. Predict days to failure using PyTorch LSTM model
            obj_key = obj_type.replace(' ', '_')
            fail_thresh = IRC_THRESHOLDS.get(obj_key, {}).get('DANGER', 100)
            
            days_to_fail = lstm.predict_days_to_failure(
                current_ra=ra_val, 
                object_type=obj_type, 
                failure_threshold=fail_thresh,
                gps_segment_id=f"SEG_{int(lat*100)}_{int(lng*100)}"
            )

            # Insert into database
            data_point = {
                'timestamp': datetime.now().isoformat(),
                'lat': lat,
                'lng': lng,
                'object_type': obj_type,
                'ra_value': ra_val,
                'irc_status': status,
                'days_to_failure': days_to_fail,
                'weather_condition': weather_data['weather']
            }
            results_db.append(data_point)

            print(f"  -> {obj_type} Detected! RA: {ra_val:.2f} mcd | Status: {status} | Fail In: {days_to_fail} days")

    cap.release()
    cv2.destroyAllWindows()

    # Database Export
    os.makedirs('db', exist_ok=True)
    db_path = 'db/latest_run.json'
    with open(db_path, 'w') as f:
        json.dump(results_db, f, indent=4)
    print(f"\nPipeline Stream Complete. Processed {frame_idx} frames. DB updated.")

if __name__ == "__main__":
    run_pipeline("sample_highway.mp4")

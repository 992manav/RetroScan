import cv2
import numpy as np
import os

def generate_video(output_path="sample_highway.mp4", duration_sec=5, fps=10):
    print(f"Generating dummy video: {output_path}...")
    width, height = 640, 480
    
    # Define codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, float(fps), (width, height))

    total_frames = duration_sec * fps
    
    for i in range(total_frames):
        # Create a blank grey highway image
        frame = np.ones((height, width, 3), dtype=np.uint8) * 50
        
        # Simulate moving road lines (Road Marking proxy)
        offset = (i * 20) % height
        cv2.rectangle(frame, (300, offset), (340, offset + 60), (255, 255, 255), -1)
        
        # Simulate a sign board (Sign Board proxy) occasionally appearing
        if (i % 20) < 10:
            cv2.rectangle(frame, (500, 100), (600, 200), (0, 0, 255), -1) 
            
        out.write(frame)

    out.release()
    print("Dummy video generation complete! Run main.py now.")

if __name__ == "__main__":
    generate_video(os.path.join(os.path.dirname(__file__), "..", "sample_highway.mp4"))

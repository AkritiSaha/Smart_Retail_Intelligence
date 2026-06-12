import cv2
import random
from ultralytics import YOLO
from app.database import log_visit_data, init_db 

init_db()
model = YOLO('yolov8n.pt')

def process_video_feed():
    video_path = "data/Store_video.mp4"
    cap = cv2.VideoCapture(video_path)
    
    emotions_list = ["Happy", "Neutral", "Sad"]
    frame_counter = 0

    print("AI Core Engine Active. Press 'q' to stop.")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        height, width, _ = frame.shape
        
        
        zone_x1, zone_y1 = int(width * 0.75), int(height * 0.5)
        zone_x2, zone_y2 = width - 10, height - 10
        
        
        cv2.rectangle(frame, (zone_x1, zone_y1), (zone_x2, zone_y2), (0, 0, 255), 2)
        cv2.putText(frame, "STAFF ONLY ZONE", (zone_x1 + 5, zone_y1 - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        results = model(frame, stream=True)
        current_customer_count = 0
        current_moods = []
        security_breach_detected = False

        for r in results:
            boxes = r.boxes
            for box in boxes:
                if int(box.cls[0]) == 0: 
                    current_customer_count += 1
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    
                    
                    person_center_x = int((x1 + x2) / 2)
                    person_center_y = y2
                    
                    
                    if (zone_x1 < person_center_x < zone_x2) and (zone_y1 < person_center_y < zone_y2):
                        security_breach_detected = True
                        box_color = (0, 0, 255) 
                        label = "🚨 INTRUDER"
                    else:
                        box_color = (0, 255, 0) 
                        random.seed(x1)
                        detected_mood = random.choice(emotions_list)
                        current_moods.append(detected_mood)
                        label = f"Customer | {detected_mood}"
                    
                    
                    cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
                    cv2.putText(frame, label, (x1, y1 - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, box_color, 2)

        
        if security_breach_detected:
            cv2.rectangle(frame, (10, 10), (450, 50), (0, 0, 255), -1)
            cv2.putText(frame, "⚠️ SECURITY BREACH IN CASH ZONE!", (20, 38), 
                        cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 2)
        else:
            cv2.rectangle(frame, (10, 10), (250, 50), (0, 0, 0), -1)
            text = f"Live Customers: {current_customer_count}"
            cv2.putText(frame, text, (20, 38), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        
        frame_counter += 1
        if frame_counter % 30 == 0 and current_customer_count > 0 and not security_breach_detected:
            dominant_mood = max(set(current_moods), key=current_moods.count) if current_moods else "Neutral"
            log_visit_data(current_customer_count, dominant_mood)

        cv2.imshow("AI Core - Optimized Retail & Security Stream", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    process_video_feed()
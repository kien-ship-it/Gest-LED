
import cv2
import time
import vision_module

def run_vision_loop():
    cap = cv2.VideoCapture(0)
    detector = vision_module.initialize_detector()

    p_time = 0  # previous time

    while True:
        success, frame = cap.read()
        if not success:
            print("Failed to grab frame.")
            break

        hands, img = vision_module.process_frame(frame, detector)

        if hands:
            count = vision_module.count_fingers(hands[0])
            cv2.putText(img, f"Fingers: {count}", (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # FPS calculation
        c_time = time.time()
        fps = 1 / (c_time - p_time) if c_time != p_time else 0
        p_time = c_time
        cv2.putText(img, f"FPS: {int(fps)}", (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        cv2.imshow("Vision Module", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
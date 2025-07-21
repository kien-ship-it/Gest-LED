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
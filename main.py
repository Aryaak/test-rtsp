import cv2
import time

def connect_rtsp_with_retry(rtsp_url, max_retries=3, timeout=10):
    cap = None
    for attempt in range(max_retries):
        print(f"⌛ Attempt {attempt + 1}/{max_retries}: Connecting to RTSP...")
        cap = cv2.VideoCapture(rtsp_url)
        
        # Wait longer for RTSP negotiation
        start_time = time.time()
        while time.time() - start_time < timeout:
            if cap.isOpened():
                ret, frame = cap.read()
                if ret:  # Got a valid frame
                    print("✅ RTSP stream connected successfully!")
                    return cap
                else:  # RTSP connected, but no frame yet
                    time.sleep(0.5)
            else:
                time.sleep(1)
        
        # If we reach here, connection failed
        print("⚠️ RTSP connection attempt timed out.")
        cap.release()
    
    print("❌ Failed to connect after multiple retries.")
    return None

def display_rtsp_stream(rtsp_url):
    cap = connect_rtsp_with_retry(rtsp_url)
    if not cap:
        return
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("⚠️ Frame read error. Reconnecting...")
                cap.release()
                cap = connect_rtsp_with_retry(rtsp_url)
                if not cap:
                    break
                continue
            
            cv2.imshow('Live RTSP Stream', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        print("Stream stopped by user.")
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    # Corrected URL (single @)
    rtsp_url = "rtsp://admin:2024qwerty@203.153.114.226:554/Streaming/Channels/604"
    display_rtsp_stream(rtsp_url)

import cv2

def check_rtsp_stream(rtsp_url):
    cap = cv2.VideoCapture(rtsp_url)
    
    if not cap.isOpened():
        print("❌ Error: Could not connect to the RTSP stream.")
        print("Possible reasons:")
        print("- Incorrect URL or credentials")
        print("- Camera is offline")
        print("- Network/firewall blocking the connection")
        return
    
    print("✅ Successfully connected to the live RTSP stream!")
    
    try:
        while True:
            ret, frame = cap.read()
            
            if not ret:
                print("⚠️ Lost connection to the stream.")
                break
            
            cv2.imshow('Live Camera Feed', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        print("Stream stopped by user.")
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    # Corrected URL (only one @ after password)
    rtsp_url = "rtsp://admin:2024qwerty@203.153.114.226:554/Streaming/Channels/604"
    check_rtsp_stream(rtsp_url)
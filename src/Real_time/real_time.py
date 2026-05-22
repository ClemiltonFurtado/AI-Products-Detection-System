import cv2
from flask import render_template, Response

class RealTime:
    """
    Module responsible for handling real-time video streaming and object detection.
    """

    def __init__(self, ai_processor):
        """
        Initializes the RealTime module.
        
        Args:
            ai_processor (AI): The global AI instance injected for processing video frames.
        """
        self.ai_processor = ai_processor

    def render_page(self, template_realtime):
        """
        Renders the HTML template for the real-time detection page.
        
        Args:
            template_realtime (str): The path to the HTML template.
            
        Returns:
            str: Rendered HTML template.
        """
        return render_template(template_realtime)

    def find_available_camera(self, max_tested=5):
        """
        Tests video ports from 0 up to max_tested to find a functional camera.
        
        Args:
            max_tested (int): The maximum number of camera indices to test.
            
        Returns:
            int or None: The index of the first functional camera found, or None if none are found.
        """
        print("[INFO] Searching for available cameras...")
        for i in range(max_tested):
            camera = cv2.VideoCapture(i)
            if camera.isOpened():
                success, _ = camera.read()
                if success:
                    print(f"[INFO] Functional camera found at index: {i}")
                    camera.release()
                    return i
                camera.release()
            
        print("[ERROR] No functional camera found!")
        return None

    def generate_frames(self):
        """
        Generator function that reads frames from the camera, processes them with the AI model,
        encodes them to JPEG, and yields them for a multipart/x-mixed-replace stream.
        
        Yields:
            bytes: Formatted byte stream of the processed JPEG frames.
        """
        camera_index = self.find_available_camera()
        
        if camera_index is None:
            return
            
        camera = cv2.VideoCapture(camera_index)
        
        while True:
            success, frame = camera.read()
            if not success:
                break
            else:
                processed_frame = self.ai_processor.process_frame(frame)
                
                ret, buffer = cv2.imencode('.jpg', processed_frame)
                frame_bytes = buffer.tobytes()
                
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    def video_feed(self):
        """
        Provides the Flask Response object for the video stream.
        
        Returns:
            Response: A Flask Response configured for multipart streaming.
        """
        return Response(self.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
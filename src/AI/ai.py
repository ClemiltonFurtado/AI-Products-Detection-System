import os
import cv2
from ultralytics import YOLO

class AI:
    """
    Module responsible for loading and managing the YOLO object detection model.
    Handles inference for static images, real-time video frames, and raw JSON data generation.
    """

    def __init__(self, model_path='best.pt'):
        """
        Initializes the AI module and loads the YOLO model into memory.
        
        Args:
            model_path (str): The file path to the trained YOLO model weights.
        """
        self.model = YOLO(model_path)
        
        self.result_folder = os.path.join('static', 'results')
        os.makedirs(self.result_folder, exist_ok=True)

    def process_image(self, image_path, filename, upload_folder):
        """
        Processes a static image file, draws bounding boxes, and saves the output.
        
        Args:
            image_path (str): The absolute path to the uploaded original image.
            filename (str): The name of the file being processed.
            upload_folder (str): The base directory where the result folder will be created.
            
        Returns:
            str: The filename of the processed and saved image.
        """
        result_folder = os.path.join(upload_folder, 'results')
        os.makedirs(result_folder, exist_ok=True)
        
        results = self.model(image_path, conf=0.7)
        res_plotted = results[0].plot()
        
        result_filepath = os.path.join(result_folder, filename)
        cv2.imwrite(result_filepath, res_plotted)
        
        return filename
    
    def process_frame(self, frame):
        """
        Processes a single video frame for real-time detection.
        
        Args:
            frame (numpy.ndarray): The raw video frame captured by the camera.
            
        Returns:
            numpy.ndarray: The processed video frame containing the plotted bounding boxes.
        """
        results = self.model(frame, conf=0.7)
        
        res_plotted = results[0].plot()
        
        return res_plotted
    
    def process_json(self, image_path):
        """
        Processes an image and extracts raw detection data for the API.
        
        Args:
            image_path (str): The path to the uploaded image file.
            
        Returns:
            dict: A dictionary containing a list of detected objects and their confidence scores.
        """
        results = self.model(image_path, conf=0.7)
        
        detections = []
        
        for box in results[0].boxes:
            class_id = int(box.cls.item())
            class_name = self.model.names[class_id]
            
            confidence = round(float(box.conf.item()), 2)
            
            detections.append({
                "class": class_name,
                "confidence": confidence
            })
            
        return {
            "detections": detections
        }
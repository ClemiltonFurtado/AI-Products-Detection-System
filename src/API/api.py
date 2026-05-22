import os
from flask import request, jsonify
from werkzeug.utils import secure_filename

class API:
    """
    Module responsible for handling pure API requests and returning JSON responses.
    """

    def __init__(self, ai_processor):
        """
        Initializes the API module.
        
        Args:
            ai_processor (AI): The global AI instance injected for processing images and generating JSON data.
        """
        self.ai_processor = ai_processor

    def detect_endpoint(self, app):
        """
        Handles the POST request for the API detection endpoint.
        Receives an image, processes it using the AI model, and returns a raw JSON response.
        
        Args:
            app (Flask): The current Flask application instance.
            
        Returns:
            tuple: A JSON response containing the detections (or an error) and an HTTP status code.
        """
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"error": "No image selected"}), 400
            
        if file:
            filename = secure_filename(file.filename)
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            file.save(upload_path)
            
            json_result = self.ai_processor.process_json(upload_path)
            
            if os.path.exists(upload_path):
                os.remove(upload_path)
                
            return jsonify(json_result), 200
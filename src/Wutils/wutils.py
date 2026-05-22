import os
from flask import Flask, render_template, send_from_directory
from Configs.config import *
from AI.ai import AI  
from Upload.upload import Upload
from Real_time.real_time import RealTime
from API.api import API

class Wutils:
    """
    Central orchestrator class for the AI Products Detection System.
    
    This class is responsible for initializing the Flask application, setting up 
    the necessary directories, loading the global AI model to optimize GPU/Memory usage, 
    injecting the AI dependency into the submodules (Upload, RealTime, API), 
    and registering all the web and API routes.
    """

    def __init__(self):
        """
        Initializes the Wutils instance.
        Sets up the Flask app, configures upload directories, instantiates the AI model, 
        and maps all URL endpoints to their respective handler methods.
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))
        template_dir = os.path.join(base_dir, '../..', 'Templates')
        
        self.app = Flask(__name__, template_folder=template_dir)
        self.app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        os.makedirs(self.app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        # 1. INSTANTIATE THE AI ONCE GLOBALLY
        print("[INFO] Initializing Global AI Engine...")
        self.ai_processor = AI(model_path=MODEL_PATH)
        
        # 2. PASS THE SAME AI INSTANCE TO ALL MODULES (Dependency Injection)
        self.upload = Upload(ai_processor=self.ai_processor)
        self.realtime = RealTime(ai_processor=self.ai_processor)
        self.api = API(ai_processor=self.ai_processor)
        
        # 3. REGISTER STANDARD ROUTES
        self.app.add_url_rule('/', endpoint='index', view_func=self.handle_index, methods=['GET'])
        self.app.add_url_rule('/upload', endpoint='upload', view_func=self.handle_upload, methods=['GET', 'POST'])
        self.app.add_url_rule('/exibir-resultado/<filename>', endpoint='exibir_resultado', view_func=self.handle_exibir_resultado, methods=['GET'])
        
        # 4. REGISTER REAL-TIME ROUTES
        self.app.add_url_rule('/realtime', endpoint='realtime', view_func=self.handle_realtime, methods=['GET'])
        # NEW ROUTE: Where the browser fetches the video stream frames
        self.app.add_url_rule('/video_feed', endpoint='video_feed', view_func=self.realtime.video_feed, methods=['GET'])

        # 5. REGISTER API ROUTE (/detect) ONLY FOR POST METHODS
        self.app.add_url_rule('/detect', endpoint='detect', view_func=self.handle_api_detect, methods=['POST'])

    def handle_index(self):
        """
        Handles requests for the main index/menu page.
        
        Returns:
            Rendered HTML template for the main page.
        """
        return render_template(TEMPLATE_INDEX)

    def handle_upload(self):
        """
        Handles requests for the upload page.
        Delegates the file processing logic to the Upload module.
        
        Returns:
            Rendered HTML template for the upload page, with or without the processed image.
        """
        return self.upload.upload_file(self.app, TEMPLATE_UPLOAD, ALLOWED_EXTENSIONS)

    def handle_realtime(self):
        """
        Handles requests for the real-time detection page.
        
        Returns:
            Rendered HTML template containing the video stream interface.
        """
        return self.realtime.render_page(TEMPLATE_REALTIME)

    def handle_exibir_resultado(self, filename):
        """
        Serves the processed image files directly from the results directory.
        
        Args:
            filename (str): The name of the processed image file.
            
        Returns:
            The image file served by the Flask application.
        """
        result_dir = os.path.join(self.app.config['UPLOAD_FOLDER'], 'results')
        return send_from_directory(result_dir, filename)

    def handle_api_detect(self):
        """
        Handles POST requests for the pure API endpoint.
        Delegates the processing to the API module to return a JSON response.
        
        Returns:
            JSON response containing the detected classes and confidence levels.
        """
        return self.api.detect_endpoint(self.app)

    def initialize_system(self):
        """
        Starts the Flask development server.
        """
        self.app.run(debug=True)
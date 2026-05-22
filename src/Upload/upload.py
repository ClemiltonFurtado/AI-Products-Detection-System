import os
from flask import request, render_template, flash, redirect
from werkzeug.utils import secure_filename

class Upload:
    """
    Module responsible for handling image uploads via the web interface.
    """

    def __init__(self, ai_processor):
        """
        Initializes the Upload module.
        
        Args:
            ai_processor (AI): The global AI instance injected for processing images.
        """
        self.ai_processor = ai_processor

    def allowed_file(self, filename, allowed_extensions):
        """
        Validates if the uploaded file has an allowed extension.
        
        Args:
            filename (str): The name of the uploaded file.
            allowed_extensions (set): A set of permitted file extensions (e.g., {'png', 'jpg'}).
            
        Returns:
            bool: True if the file extension is allowed, False otherwise.
        """
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

    def upload_file(self, app, template_upload, allowed_extensions):
        """
        Handles the upload route logic for both GET and POST requests.
        
        Args:
            app (Flask): The current Flask application instance.
            template_upload (str): The path to the upload HTML template.
            allowed_extensions (set): A set of permitted file extensions.
            
        Returns:
            str: Rendered HTML template.
        """
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file uploaded.')
                return redirect(request.url)
            
            file = request.files['file']
            
            if file.filename == '':
                flash('No image selected.')
                return redirect(request.url)
            
            if file and self.allowed_file(file.filename, allowed_extensions):
                filename = secure_filename(file.filename)
                
                upload_folder = app.config['UPLOAD_FOLDER']
                upload_path = os.path.join(upload_folder, filename)
                
                file.save(upload_path)
                
                processed_filename = self.ai_processor.process_image(upload_path, filename, upload_folder)
                
                image_url = f"/exibir-resultado/{processed_filename}"
                
                return render_template(template_upload, uploaded_image=image_url)
            else:
                flash('File extension not allowed.')
                return redirect(request.url)
        
        return render_template(template_upload)
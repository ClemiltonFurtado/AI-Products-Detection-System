import os

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../../data/uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
TEMPLATE_INDEX = "index.html"
TEMPLATE_UPLOAD = "upload.html"
TEMPLATE_REALTIME = "realtime.html"
MODEL_PATH = "../data/model/best.pt"
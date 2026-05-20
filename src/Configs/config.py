import os

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../../data/uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Nomes dos arquivos HTML
TEMPLATE_INDEX = "index.html"
TEMPLATE_UPLOAD = "upload.html"
TEMPLATE_REALTIME = "realtime.html"
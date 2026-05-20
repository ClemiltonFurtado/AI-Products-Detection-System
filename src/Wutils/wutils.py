from flask import Flask, render_template
from Configs.config import *
from Upload.upload import Upload
from Real_time.real_time import RealTime

class Wutils:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        template_dir = os.path.join(base_dir, '../..', 'Templates')
        print(f"Buscando templates em: {template_dir}")
        
        self.app = Flask(__name__, template_folder=template_dir)
        self.app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        self.app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
        
        # Instanciando as classes das funcionalidades
        self.upload = Upload()
        self.realtime = RealTime()
        
        # Registrando as 3 rotas
        self.app.add_url_rule('/', endpoint='index', view_func=self.handle_index, methods=['GET'])
        self.app.add_url_rule('/upload', endpoint='upload', view_func=self.handle_upload, methods=['GET', 'POST'])
        self.app.add_url_rule('/realtime', endpoint='realtime', view_func=self.handle_realtime, methods=['GET'])


    def handle_index(self):
        # Rota principal (Menu)
        return render_template(TEMPLATE_INDEX)

    def handle_upload(self):
        # Rota de Upload
        return self.upload.upload_file(self.app, TEMPLATE_UPLOAD, ALLOWED_EXTENSIONS)

    def handle_realtime(self):
        # Rota de Tempo Real
        return self.realtime.render_page(TEMPLATE_REALTIME)

    def initialize_system(self):
        self.app.run(debug=True)
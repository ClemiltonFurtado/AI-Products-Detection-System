from flask import render_template

class RealTime:
    def __init__(self):
        pass

    def render_page(self, template):
        # Aqui no futuro você colocará a lógica da câmera/detecção
        return render_template(template)
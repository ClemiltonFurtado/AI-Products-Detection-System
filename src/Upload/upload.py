import os
from flask import flash, redirect, render_template, request
from werkzeug.utils import secure_filename

class Upload:
    def check_dir(self, upload_folder):
        os.makedirs(upload_folder, exist_ok=True)

    def allowed_file(self, filename, extensions):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in extensions
    
    def upload_file(self, app, html_template, extensions):
        if request.method == 'POST':
            # Verifica se a requisição tem a parte do arquivo
            if 'file' not in request.files:
                flash('Nenhum arquivo enviado.')
                return redirect(request.url)
            
            file = request.files['file']
            
            # Se o usuário não selecionar um arquivo, o navegador envia uma string vazia
            if file.filename == '':
                flash('Nenhuma imagem selecionada.')
                return redirect(request.url)
            
            # Verifica se o arquivo é permitido
            if file and self.allowed_file(file.filename, extensions):
                # Limpa o nome do arquivo para evitar problemas de segurança
                filename = secure_filename(file.filename)
                # Salva o arquivo na pasta de uploads
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return f"<h3>Upload feito com sucesso! Arquivo salvo como: {filename}</h3><br><a href='/'>Voltar</a>"
            else:
                flash('Extensão de arquivo não permitida. Use PNG, JPG, JPEG ou GIF.')
                return redirect(request.url)

        return render_template(html_template)
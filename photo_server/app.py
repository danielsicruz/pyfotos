from flask import Flask, render_template, request, redirect, url_for, send_from_directory, abort, Response
import os, subprocess

app = Flask(__name__)

# Definir as credenciais de login
USERNAME = "admin"
PASSWORD = "senha123"

# Caminho onde as fotos serão armazenadas
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

# Função para verificar se a extensão da imagem é permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Função para autenticar
def check_auth(username, password):
    return username == USERNAME and password == PASSWORD

# Função para pedir autenticação (Basic Authentication)
def authenticate():
    return Response(
        'Você precisa fazer login para acessar esta página.', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

# Verificar se o usuário está autenticado
def requires_auth(f):
    def auth_required_wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return auth_required_wrapper


@app.route('/tv/on', methods=['POST'])
def tv_on():
    return requires_auth(handle_tv_on)()

def handle_tv_on():
    try:
        subprocess.run(['echo', 'on 0', '|', 'cec-client', '-s', '-d', '1'], check=True)
        return redirect(url_for('index'))
    except subprocess.CalledProcessError as e:
        return f"Erro ao ligar a TV: {str(e)}"

@app.route('/tv/off', methods=['POST'])
def tv_off():
    return requires_auth(handle_tv_off)()

def handle_tv_off():
    try:
        subprocess.run(['echo', 'standby 0', '|', 'cec-client', '-s', '-d', '1'], check=True)
        return redirect(url_for('index'))
    except subprocess.CalledProcessError as e:
        return f"Erro ao desligar a TV: {str(e)}"

# Página inicial que lista as imagens
@app.route('/')
def index():
    # Aplica a autenticação na função index
    return requires_auth(render_index)()

# Função auxiliar para a rota index
def render_index():
    images = os.listdir(app.config['UPLOAD_FOLDER'])
    images = [img for img in images if allowed_file(img)]
    return render_template('index.html', images=images)

# Rota para upload de imagens
@app.route('/upload', methods=['POST'])
def upload_file():
    # Aplica a autenticação na função upload_file
    return requires_auth(handle_upload_file)()

def handle_upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    files = request.files.getlist('file')  # Pega todos os arquivos enviados
    filenames = []
    
    for file in files:
        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            filenames.append(filename)
    
    return redirect(url_for('index'))

# Rota para excluir uma imagem
@app.route('/delete/<filename>', methods=['GET'])
def delete_file(filename):
    # Aplica a autenticação na função delete_file
    return requires_auth(handle_delete_file)(filename)

def handle_delete_file(filename):
    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('index'))
    except Exception as e:
        return f"Erro ao excluir o arquivo: {str(e)}"

# Rota para acessar imagens da pasta uploads
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # Aplica a autenticação na função uploaded_file
    return requires_auth(handle_uploaded_file)(filename)

def handle_uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

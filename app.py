from flask import Flask, request, render_template, url_for
import os
import re
import subprocess

app = Flask(__name__, static_folder='static')

# Armazene os processos em execução aqui
processes = {}

# Defina o caminho para a pasta estática
static_folder = r'C:\Users\Caina\Documents\Code-note\Sofascore2\static'

@app.route('/', methods=['GET', 'POST'])
def home():
    # Defina os caminhos completos para os arquivos aqui
    filepath_sofascore = r'C:\Users\Caina\Documents\Code-note\Sofascore2\sofascore.py'
    filepath_my_matplotlib = r'C:\Users\Caina\Documents\Code-note\Sofascore2\my_matplotlib.py'
    
    if request.method == 'POST':
        if 'submit_sofascore' in request.form:
            new_code_sofascore = request.form['sofascore']
            with open(filepath_sofascore, 'r') as file:
                lines = file.readlines()
            for i, line in enumerate(lines):
                if 'match_id' in line:
                    lines[i] = re.sub(r'{match_id}', new_code_sofascore, line)
            with open(filepath_sofascore, 'w') as file:
                file.writelines(lines)
            return 'Dados recebidos para sofascore.py!'
        elif 'submit_my_matplotlib' in request.form:
            new_code_my_matplotlib = request.form['my_matplotlib']
            with open(filepath_my_matplotlib, 'r') as file:
                lines = file.readlines()
            for i, line in enumerate(lines):
                if 'db_name' in line:
                    lines[i] = re.sub(r'{db_name}', new_code_my_matplotlib, line)
            with open(filepath_my_matplotlib, 'w') as file:
                file.writelines(lines)
            return 'Dados recebidos para my_matplotlib.py!'
        elif 'run_sofascore' in request.form:
            # Inicie o script sofascore.py em um novo processo
            processes['sofascore'] = subprocess.Popen(['python', filepath_sofascore])
            return 'Script sofascore.py iniciado!'
        elif 'run_my_matplotlib' in request.form:
            # Inicie o script my_matplotlib.py em um novo processo
            processes['my_matplotlib'] = subprocess.Popen(['python', filepath_my_matplotlib])
            return 'Script my_matplotlib.py iniciado!'
        elif 'stop_sofascore' in request.form:
            # Interrompa o script sofascore.py
            if 'sofascore' in processes:
                processes['sofascore'].terminate()
                return 'Script sofascore.py interrompido!'
        elif 'stop_my_matplotlib' in request.form:
            # Interrompa o script my_matplotlib.py
            if 'my_matplotlib' in processes:
                processes['my_matplotlib'].terminate()
                return 'Script my_matplotlib.py interrompido!'

    # Liste os arquivos na pasta estática
    files = os.listdir(app.static_folder)

    # Gere URLs para os arquivos
    file_urls = [url_for('static', filename=file) for file in files]

    return render_template('index.html', file_urls=file_urls)

if __name__ == '__main__':
    app.run(debug=True)

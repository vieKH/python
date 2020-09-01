import os
import re
from os.path import join

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)  # работа со статическими папками
app.config['LAB_DIR'] = 'lab3'
app.config['UPLOAD_DIR'] = 'upload'  # работа со словарями
app.config['ALLOWED_EXTENSION'] = '.png'  # потенциальное место для разных вариантов - .jpeg, .tiff, .bmp и т.д.


@app.route("/")
def index():
    return render_template('index.html')  # работа с рендерингом шаблонов


@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        if re.search(app.config['ALLOWED_EXTENSION'] + '$',
                     uploaded_file.filename) is not None:  # использование регекса
            uploaded_file.save(join(app.config['LAB_DIR'], app.config['UPLOAD_DIR'], uploaded_file.filename))
        else:
            return redirect(url_for('extension_err',  # роутинг с параметрами
                                    allowed=app.config['ALLOWED_EXTENSION'],
                                    forbidden=os.path.splitext(uploaded_file.filename)[1]))  # работа с экстеншенами
    return redirect(url_for('index'))  # работа с роутингом


@app.route('/extension_err?<string:allowed>&<string:forbidden>')  # работа с url rules
def extension_err(allowed, forbidden):
    return render_template('extension_err.html',  # рендеринг шаблона с передачей параметров
                           allowed=allowed,
                           forbidden=forbidden)


@app.route('/display')
def display():
    files = [join(app.config['UPLOAD_DIR'], f)  # работа с файлами/директориями
             for f in os.listdir(join(app.config['LAB_DIR'], app.config['UPLOAD_DIR']))
             if os.path.isfile(join(app.config['LAB_DIR'], app.config['UPLOAD_DIR'], f))]
    return render_template('display.html', images=files)


if __name__ == "__main__":
    app.run()
# итог - 9 мест, где студент может обосраться + 3 html-файла, в которых вставки js кода и jinja-синтаксиса

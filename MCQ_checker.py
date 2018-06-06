import os
import cgi
from flask import Flask
from flask import render_template
from os.path import join, dirname, realpath
from flask import request
from werkzeug.utils import secure_filename
from Grid_Evaluation import grid_check, answer_dict

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploads')
TEMPLATE = join(dirname(realpath(__file__)), 'static/template')
RESULT = join(dirname(realpath(__file__)), 'static/output')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/grid')
def grid():
    return render_template('grid_home.html')


@app.route('/alpha')
def alpha():
    return render_template('alpha_home.html')

@app.route('/gridAnswer', methods=['POST'])
def grid_answer():
    qes= request.form['Total_qes']

    return render_template('grid_answer.html', val=qes)


@app.route('/upload', methods=['POST'])
def upload_answer():
    file = request.files['inputTemplate']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    grid_check(file.filename)
    return render_template('gridResult.html', img=file.filename, out=filename)

@app.route('/Store_answer',methods=['POST'])
def store_answer():
    num= request.form.get('number')
    num=int(num)
    ans = 'answer1'
    answer = request.form.get(ans)
    answer=int(answer)
    ans_set={}
    for i in range(num):
        ans = 'answer'+str(i+1)
        answer= request.form.get(ans)
        answer = int(answer)
        ans_set[i]=answer
    # print ans_set
    answer_dict(ans_set)
    return render_template('grid_home.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['TEMPLATE'] = TEMPLATE
    app.config['RESULT'] = RESULT
    app.run()

import os
import cgi

import cv2
from flask import Flask
from flask import flash
from flask import render_template
from os.path import join, dirname, realpath
from flask import request
from werkzeug.utils import secure_filename
from Grid_Evaluation import grid_check, answer_dict
from performAction import alpha_dict, image_processing, recognition_character
from templateProcessing import template_image
from template_matching import templateMatch

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploads/')
TEMPLATE = join(dirname(realpath(__file__)), 'static/template')
RESULT = join(dirname(realpath(__file__)), 'static/output/')
PROCESSED = join(dirname(realpath(__file__)), 'static/processed')
CHECK =join(dirname(realpath(__file__)), 'static/check')



@app.route('/')
def home():
    return render_template('index.html')


@app.route('/grid')
def grid():
    return render_template('grid_home.html')

@app.route('/longGrid')
def longGrid():
    return render_template('longGrid_home.html')


@app.route('/alpha')
def alpha():
    return render_template('alpha_home.html')

# @app.route('/gridAnswer', methods=['POST'])
# def grid_answer():
#     qes= request.form['Total_qes']
#
#     return render_template('grid_answer.html', val=qes)


@app.route('/upload', methods=['POST'])
def upload_answer():
    file = request.files['inputTemplate']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    grid_check(file.filename)
    flash('filesh uploaded')
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

@app.route('/Store_answer2',methods=['POST'])
def store_answer2():
    num= request.form.get('number')
    num=int(num)
    ans = 'answer1'
    answer = request.form.get(ans)
    ans_set={}
    for i in range(num):
        ans = 'answer'+str(i+1)
        answer= request.form.get(ans)
        n=i+1
        if answer=='A' or answer=='a':
            ans_set[n]='A'
        if answer=='B' or answer=='b':
            ans_set[n]='B'
        if answer=='C' or answer=='c':
            ans_set[n]='C'
        if answer=='D' or answer=='d':
            ans_set[n]='D'
        if answer=='E' or answer=='e':
            ans_set[n]='E'
    # print ans_set
    alpha_dict(ans_set)

    return render_template('alpha_home.html')


@app.route('/longGrid', methods=['POST'])
def longGrid_template():
    file = request.files['template']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['TEMPLATE'], filename))
    template_image(file.filename)
    return render_template('longGrid_home.html')

@app.route('/longGrid_result', methods=['POST'])
def longGrid_result():
    file = request.files['answer']
    filenames = os.listdir(PROCESSED)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #
    # for filename in os.listdir(PROCESSED):
    #     img = cv2.imread('./static/processed/'+filename)
    #     filename2 = secure_filename(img.filename)
    print filenames
    templateMatch(file.filename, filenames[0])
    return render_template('longGrid_result.html',img=file.filename, out=filename, temp=filenames[0])

@app.route('/alphaResult', methods=['POST'])
def alpha_upload():
    file = request.files['alphaAnswer']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


    characters_img = image_processing(file.filename)
    ans = recognition_character(characters_img)
    img = cv2.imread(UPLOAD_FOLDER+filename)
    print ans
    cv2.putText(img, "Total Correct:" + str(ans), (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)
    cv2.imwrite(RESULT + filename, img)
    if not characters_img:
        return render_template('error.html')
    else:
        return render_template('alphaResult.html',img=file.filename, out=filename)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['TEMPLATE'] = TEMPLATE
    app.config['RESULT'] = RESULT
    app.config['PROCESSED']=PROCESSED
    app.config['CHECK']=CHECK
    app.debug = True
    app.run()

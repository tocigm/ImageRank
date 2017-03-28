import uuid
import os

from flask import Flask, request, redirect, url_for, make_response
from werkzeug import secure_filename
import json
from features.vgg16 import vgg16

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))+'/uploads/'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#create uploads folder
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash



# @app.before_request
# def before_request():
#     vgg = vgg16('vgg16_weights.npz')
#     im = imread("laska.png", mode='RGB')
#     vgg.get_feature(im)


# @app.teardown_request
# def teardown_request(exception):
#     db = getattr(g, 'db', None)
#     if db is not None:
#         db.close()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

vgg = vgg16('vgg16_weights.npz')


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            name, file_extension = os.path.splitext(filename)
            newfilename = str(uuid.uuid1()) + file_extension
            newfilepath = os.path.join(app.config['UPLOAD_FOLDER'], newfilename)
            file.save(newfilepath)
            feature = vgg.get_feature(newfilepath)
            list = feature.tolist()[0]
            os.remove(newfilepath);
            response = make_response(json.dumps(list))
            response.headers['Content-type'] = 'application/json'
            return response

if __name__ == '__main__':
    app.run(host='127.0.0.1')

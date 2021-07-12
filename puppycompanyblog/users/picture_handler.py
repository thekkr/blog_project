import os
from PIL import Image
from flask import url_for,current_app
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png','jpg','jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.split('.',1)[1] in ALLOWED_EXTENSIONS

def add_profile_pic(pic_upload,username):

    filename = secure_filename(pic_upload.filename)

    ext_type = filename.split('.')[-1]

    storage_filename = str(username)+'.'+ext_type

    pic_upload.save(os.path.join(current_app.root_path+'\\static\\profile_pics',filename))
    #
    # output_size = (200,200)
    #
    # pic = Image.open(pic_upload)
    # pic.thumbnail(output_size)
    # print(filepath)
    # pic.save(filepath,ext_type)

    return storage_filename

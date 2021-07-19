import os
from puppycompanyblog.models import BlogPost
from flask import render_template, Blueprint,request
from werkzeug.utils import secure_filename

core  = Blueprint('core',__name__)
ALLOWED_EXTENSIONS = {'png','jpeg','jpg'}

def allowed_file(filename):
    return '.' in filename and filename.split('.',1)[1] in ALLOWED_EXTENSIONS

@core.route('/')
def index():
    #More to add
    page = request.args.get('page',1,type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page,per_page=5)

    return render_template('index.html',blog_posts=blog_posts)

# @core.route('/',methods=['GET','POST'])
# def upload_image():
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             return redirect(request.url)
#
#         file = request.files['file']
#
#         if file.filename == '':
#             return redirect(request.url)
#
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
#             return render_template('index.html')
#     return render_template('index.html')


@core.route('/info')
def info():
    return render_template('info.html')

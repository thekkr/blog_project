
#register
#login
#Logout
#account (update form)
#user posts(blogposts)
import os
from flask import render_template,url_for,flash,redirect,request,Blueprint,current_app
from flask_login import login_required,login_user,logout_user,current_user
from puppycompanyblog import db,app
from puppycompanyblog.models import User,BlogPost
from puppycompanyblog.users.forms import LoginForm,RegistrationForm,UpdateForm
from puppycompanyblog.users.picture_handler import add_profile_pic
from werkzeug.utils import secure_filename
users = Blueprint('users',__name__)

ALLOWED_EXTENSIONS = {'png','jpg','jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.split('.',1)[1] in ALLOWED_EXTENSIONS
#logout_user

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index'))

#registered
@users.route('/registraton',methods=['GET','POST'])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email = form.email.data,username = form.username.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registraion Succesful')
        return redirect(url_for('users.login'))
    return render_template('register.html',form=form)


#login_view
@users.route('/login',methods=['GET','POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        user  = User.query.filter_by(email = form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Login Succesful')

            next = request.args.get('next')

            if next==None or not next[0]=='/':
                next = url_for('core.index')

            return redirect(next)

    return render_template('login.html',form=form)


@users.route('/account',methods=['GET','POST'])
@login_required

def account():

    form = UpdateForm()
    if form.validate_on_submit():
        if 'pitcure' not in request.files:
            flash('no image uplaoded')

        picture = request.files['picture']

        if picture.filename=='':
            flash('no file selected')
        if picture and allowed_file(picture.filename):
            filename = str(current_user.username)+'.'+picture.filename.split('.',1)[1]
            picture.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            pic = str(current_user.username)+'.'+filename.split('.',1)[1]
        current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        print('yes')
        db.session.commit()
        flash('User account updated')
        return redirect(url_for('users.account'))
    elif request.method=='GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    profile_image = url_for('static',filename ='profile_pics/'+current_user.profile_image)
    return render_template('account.html',profile_image=profile_image,form=form)





@users.route('/<username>')
def user_posts(username):

    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page,per_page=5)
    return render_template('user_blog_posts.html',blog_post=blog_posts,user=user)

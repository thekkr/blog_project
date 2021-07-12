from flask import render_template,request,url_for,Blueprint,redirect
from flask_login import current_user,login_required,login_user,logout_user
from project.models import User
from project.users.forms import LoginForm,RegistrationForm,UpdateForm
from project import db

users = Blueprint('users',__name__)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index'))

@users.route('/login',methods=['GET','POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data):
            login_user(user)

            next = request.args.get('next')

            if next == None or next[0]=='/':
                next = url_for('core.index')

            return redirect(next)

    return render_template('login.html',form=form)


@users.route('/register',methods=['GET','POST'])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,username=form.username.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users.login'))
    return render_template('register.html',form=form)

@users.route('/accout',methods=['GET','POST'])
def account():

    form = UpdateForm()

    if form.validate_on_submit():

        if form.picture.data:
            username = current_user.Username
            pic = add_profile_pic(form.picture.data,username)
            current_user.profile_image = pic

        current_user.email = form.email.data
        current_user.username = form.username.data
        db.session.commit()
        return redirect(url_for('users.account'))
    elif request.method=='GET':
        form.email.data = current_user.email
        form.username.data = current_user.username

    profile_image = url_for('static',filename='profile_pics/'+current_user.profile_image)
    return render_template('account.html',form=form,profile_image=profile_image)

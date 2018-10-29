from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from .forms import LoginForm, RegistrationForm
from .models import User, Category, File
from . import file_sys
from flask import jsonify


fs = file_sys.FileSys()


@app.route('/test/accounts/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('auth/login.html', form=form)


@app.route('/test/accounts/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('auth/register.html', form=form)


@app.route('/test/accounts/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/')
@app.route('/test')
@login_required
def index():
    categories = Category.query.filter_by(user=current_user)
    return render_template('index.html', categories=categories, fs=fs.get_content())


@app.route('/test/add_cat', methods=['POST'])
def add_category():
    name = request.form.get('name')
    if Category.query.filter_by(name=name, user=current_user):
        category = Category(name=name, user=current_user)
        db.session.add(category)
        db.session.commit()

    data = [cat.name for cat in Category.query.filter_by(user=current_user)]
    return jsonify(data)


@app.route('/test/del_cat', methods=['POST'])
def del_category():
    name = request.form.get('name')
    Category.query.filter_by(name=name, user=current_user).delete()
    db.session.commit()

    data = [cat.name for cat in Category.query.filter_by(user=current_user)]
    return jsonify(data)


@app.route('/test/go_to', methods=['POST'])
def go_to():
    folder = request.form.get('folder')
    data = fs.go_to(folder)
    return jsonify(data)


@app.route('/test/add_file', methods=['POST'])
def add_file():
    file_name = request.form.get('file')
    category = Category.query.filter_by(name=request.form.get('category'), user=current_user).first()

    if File.query.filter_by(name=file_name, category=category).count() == 0:
        file = File(name=file_name, category=category)
        db.session.add(file)
        db.session.commit()
        files = [cat.name for cat in category.files.all()]
        return jsonify(files)
    else:
        return jsonify(False)


@app.route('/test/del_file', methods=['POST'])
def del_file():
    file_name = request.form.get('file')
    cat_name = request.form.get('category')

    category = Category.query.filter_by(name=cat_name, user=current_user).first()

    File.query.filter_by(name=file_name, category=category).delete()
    db.session.commit()
    files = [cat.name for cat in category.files.all()]
    return jsonify(files)


@app.route('/test/get_files', methods=['POST'])
def get_files():
    category = Category.query.filter_by(name=request.form.get('category'), user=current_user).first()
    files = [cat.name for cat in category.files.all()]
    return jsonify(files)


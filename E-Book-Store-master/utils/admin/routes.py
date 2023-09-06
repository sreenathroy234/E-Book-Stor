from flask import render_template, session, redirect, request, url_for, flash
from utils import app, db, bcrypt
from .forms import RegistrationForm, LoginForm
from .models import User
from utils.products.models import Addproduct   #table name
from utils.products.models import Addproduct,Category,Brand
import os

@app.route('/admin')
def admin():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    products = Addproduct.query.all()
    return render_template('admin/index.html',title="Admin Page",products=products)

@app.route('/authors')
def brands():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/author.html', title='Authors',brands=brands)


@app.route('/categories')
def categories():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/author.html', title='categories',categories=categories)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data, username=form.username.data, email=form.email.data,password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'welcome {form.name.data}. Thanks for registering','success')
        return redirect(url_for('admin'))
    return render_template('admin/register.html', form=form, title="Admin Registration Page")


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            flash(f'welcome {form.email.data} you are logedin now','success')
            return redirect(url_for('admin'))
        else:
            flash(f'Wrong email/password', 'success')
            return redirect(url_for('login'))
    return render_template('admin/login.html',title='Admin Login page',form=form)

@app.route('/logout')
def logout():
    session.pop('email')
    return redirect(url_for('login'))



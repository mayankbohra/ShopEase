from flask import Blueprint, render_template, flash, redirect
from flask_login import login_user, login_required, logout_user

from .forms import *
from .models import Customer
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    form = signUpForm()

    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password1 = form.password1.data
        password2 = form.password2.data

        if password1 == password2:
            new_customer = Customer(email=email, username=username, password=password2)

            try:
                db.session.add(new_customer)
                db.session.commit()
                flash('Account Created Successfully', category='success')
                return redirect('/login')
            except Exception as e:
                print(e)
                flash('Account not created!, Email already exists')

            form.email.data = ''
            form.username.data = ''
            form.password1.data = ''
            form.password2.data = ''

    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = loginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        customer = Customer.query.filter_by(email=email).first()

        if customer:
            if customer.verify_password(password):
                login_user(customer)
                flash('Login Successful', category='success')
                return redirect('/')
            else:
                flash('Invalid Password', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template('login.html', form=form)


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('/login')


@auth.route('/profile/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def profile(customer_id):
    customer = Customer.query.get(customer_id)
    return render_template('profile.html', customer=customer)


@auth.route('/change-password/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def change_password(customer_id):
    form = passwordChangeForm()

    customer = Customer.query.get(customer_id)

    if form.validate_on_submit():
        current_password = form.current_password.data
        new_password = form.new_password.data
        confirm_new_password = form.confirm_new_password.data

        if customer.verify_password(current_password):
            if new_password == confirm_new_password:
                customer.password = new_password
                db.session.commit()
                flash('Password Changed Successfully', category='success')
                return redirect(f'/profile/{customer_id}')
            else:
                flash('Passwords do not match', category='error')
        else:
            flash('Invalid Password', category='error')

    return render_template('change_password.html', form=form)

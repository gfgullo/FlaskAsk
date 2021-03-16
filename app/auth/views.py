from .. import db
from . import auth
from flask import render_template, redirect, url_for, flash
from app.auth.forms import SignupForm, LoginForm
from app.models import User
from app.send_mail import send_mail
from flask_login import login_user, current_user, login_required, logout_user
from flask import current_app

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if(form.validate_on_submit()):
        flash("Check your inbox")
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        if(user.email==current_app.config['ADMIN_EMAIL']):
            user.is_admin = True
        db.session.add(user)
        db.session.commit()
        login_user(user, True)
        send_mail(user.email, "Confirm your email", "mails/email_confirm", user=user, token=user.generate_confirmation_token())
    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if(form.validate_on_submit()):
        user = User.query.filter_by(email=form.email.data).first()

        if(user is not None and user.check_password(form.password.data)):
            if(not user.confirmed):
                flash("You need to confirm your account ! Check your inbox")
            else:
                login_user(user, form.remember_me.data)
                return redirect(url_for("main.index"))
        else:
            flash("Invalid email or password")

    return render_template('login.html', form=form)


@auth.route('/confirm/<token>')
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('auth.login'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for("auth.login"))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

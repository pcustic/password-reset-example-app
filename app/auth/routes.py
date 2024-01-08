from flask import render_template, redirect, url_for, flash, render_template_string
from sqlalchemy import select

from flask_login import current_user, login_user, logout_user
from flask_mailman import EmailMessage

from app import db, email
from app.models import User
from app.auth import bp
from app.auth.forms import (
    LoginForm,
    RegistrationForm,
    ResetPasswordRequestForm,
    ResetPasswordForm,
)
from app.templates.auth.reset_password_email_content import (
    reset_password_email_html_content,
)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user: User | None = db.session.scalar(
            select(User).where(User.email == form.email.data)
        )
        if user is None or not user.check_password(form.password.data):
            flash("Invalid email or password. Please try again.")
            return redirect(url_for("auth.login"))

        login_user(user)

        return redirect(url_for("main.protected"))

    return render_template("auth/login.html", title="Login", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("Congratulations, you are now a registered user!")

        return redirect(url_for("main.index"))

    return render_template("auth/register.html", title="Register", form=form)


def send_reset_password_email(user):
    reset_password_url = url_for(
        "auth.reset_password",
        token=user.generate_reset_password_token(),
        user_id=user.id,
        _external=True,
    )

    email_body = render_template_string(
        reset_password_email_html_content, reset_password_url=reset_password_url
    )

    message = EmailMessage(
        subject="Reset your password",
        body=email_body,
        to=[user.email],
    )
    message.content_subtype = "html"

    message.send()


@bp.route("/reset_password", methods=["GET", "POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user_select = select(User).where(User.email == form.email.data)
        user = db.session.scalar(user_select)

        if user:
            send_reset_password_email(user)

        flash("Instructions to reset your password were sent to your email address.")

        return redirect(url_for("auth.reset_password_request"))

    return render_template(
        "auth/reset_password_request.html", title="Reset Password", form=form
    )


@bp.route("/reset_password/<token>/<int:user_id>", methods=["GET", "POST"])
def reset_password(token, user_id):
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    user = User.validate_reset_password_token(token, user_id)
    if not user:
        return redirect(url_for("main.index"))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()

        return render_template(
            "auth/reset_password_success.html", title="Reset Password success"
        )

    return render_template(
        "auth/reset_password.html", title="Reset Password", form=form
    )

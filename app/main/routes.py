from app.main import bp
from flask import render_template

from flask_login import login_required, current_user


@bp.route("/", methods=["GET"])
def index():
    return render_template("main/index.html", title="Home")


@bp.route("/protected", methods=["GET"])
@login_required
def protected():
    return render_template("main/protected.html", title="Protected view")

from flask import Blueprint, render_template, request, redirect, url_for, session
from models.user_model import validar_usuario, crear_usuario

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        usuario = validar_usuario(username, password)

        if usuario:
            session["usuario_id"] = usuario["id"]
            session["username"] = usuario["username"]
            return redirect(url_for("dashboard"))

        return render_template("login.html", error="Usuario o contraseña incorrectos")

    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if len(password) < 4:
            return render_template("register.html", error="La contraseña debe tener al menos 4 caracteres")

        crear_usuario(username, password)
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
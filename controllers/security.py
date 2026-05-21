from flask import session, redirect, url_for


def login_required():
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))
    return None


def admin_required():
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("rol") != "admin":
        return redirect(url_for("dashboard"))

    return None


def usuario_required():
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("rol") != "usuario":
        return redirect(url_for("dashboard"))

    return None
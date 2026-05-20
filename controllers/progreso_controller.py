from flask import Blueprint, render_template, request, redirect, url_for, session
from models.progreso_model import (obtener_progresos_por_usuario, crear_progreso, eliminar_progreso)

progreso_bp = Blueprint("progreso", __name__)


def login_required():
    return "usuario_id" in session


def validar_progreso(peso_actual, porcentaje_grasa):
    if peso_actual <= 0:
        return "El peso actual debe ser mayor a 0"

    if porcentaje_grasa < 0:
        return "El porcentaje de grasa no puede ser negativo"

    if porcentaje_grasa > 100:
        return "El porcentaje de grasa no puede ser mayor a 100"

    return None


@progreso_bp.route("/progresos")
def listar_progresos():
    if not login_required():
        return redirect(url_for("auth.login"))

    usuario_id = session["usuario_id"]
    progresos = obtener_progresos_por_usuario(usuario_id)

    return render_template("progresos.html", progresos=progresos)


@progreso_bp.route("/progresos/crear", methods=["GET", "POST"])
def crear():
    if not login_required():
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        fecha = request.form["fecha"]
        observacion = request.form["observacion"]

        try:
            peso_actual = float(request.form["peso_actual"])
            porcentaje_grasa = float(request.form["porcentaje_grasa"])
        except ValueError:
            return render_template(
                "crear_progreso.html",
                error="El peso y porcentaje de grasa deben ser valores numéricos"
            )

        error = validar_progreso(peso_actual, porcentaje_grasa)

        if error:
            return render_template("crear_progreso.html", error=error)

        crear_progreso(
            session["usuario_id"],
            fecha,
            peso_actual,
            porcentaje_grasa,
            observacion
        )

        return redirect(url_for("progreso.listar_progresos"))

    return render_template("crear_progreso.html")


@progreso_bp.route("/progresos/eliminar/<int:id>")
def eliminar(id):
    if not login_required():
        return redirect(url_for("auth.login"))

    eliminar_progreso(id, session["usuario_id"])
    return redirect(url_for("progreso.listar_progresos"))
from flask import Blueprint, render_template, request, redirect, url_for, session
from models.rutina_ejercicio_model import (
    obtener_asignaciones,
    crear_asignacion,
    eliminar_asignacion
)
from models.rutina_model import obtener_rutinas
from models.ejercicio_model import obtener_ejercicios
from controllers.security import admin_required

rutina_ejercicio_bp = Blueprint("rutina_ejercicio", __name__)





@rutina_ejercicio_bp.route("/asignaciones")
def listar_asignaciones():
    proteccion = admin_required()
    if proteccion:
        return proteccion

    asignaciones = obtener_asignaciones()
    return render_template("asignaciones.html", asignaciones=asignaciones)


@rutina_ejercicio_bp.route("/asignaciones/crear", methods=["GET", "POST"])
def crear():
    proteccion = admin_required()
    if proteccion:
        return proteccion

    rutinas = obtener_rutinas()
    ejercicios = obtener_ejercicios()

    if request.method == "POST":
        rutina_id = request.form["rutina_id"]
        ejercicio_id = request.form["ejercicio_id"]
        try:
            series = int(request.form["series"])
            repeticiones = int(request.form["repeticiones"])
        except ValueError:
            return render_template(
                "crear_asignacion.html",
                rutinas=rutinas,
                ejercicios=ejercicios,
                error="Las series y repeticiones deben ser números válidos"
            )
        # Validaciones Back-End importantes para el core
        if not rutina_id or not ejercicio_id:
            return render_template(
                "crear_asignacion.html",
                rutinas=rutinas,
                ejercicios=ejercicios,
                error="Debe seleccionar una rutina y un ejercicio"
            )

        if series <= 0:
            return render_template(
                "crear_asignacion.html",
                rutinas=rutinas,
                ejercicios=ejercicios,
                error="Las series deben ser mayores a 0"
            )

        if repeticiones <= 0:
            return render_template(
                "crear_asignacion.html",
                rutinas=rutinas,
                ejercicios=ejercicios,
                error="Las repeticiones deben ser mayores a 0"
            )

        crear_asignacion(rutina_id, ejercicio_id, series, repeticiones)
        return redirect(url_for("rutina_ejercicio.listar_asignaciones"))

    return render_template(
        "crear_asignacion.html",
        rutinas=rutinas,
        ejercicios=ejercicios
    )


@rutina_ejercicio_bp.route("/asignaciones/eliminar/<int:id>")
def eliminar(id):
    proteccion = admin_required()
    if proteccion:
        return proteccion

    eliminar_asignacion(id)
    return redirect(url_for("rutina_ejercicio.listar_asignaciones"))
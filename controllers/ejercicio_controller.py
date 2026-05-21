from flask import Blueprint, render_template, request, redirect, url_for, session
from models.ejercicio_model import (
    obtener_ejercicios,
    obtener_ejercicio_por_id,
    crear_ejercicio,
    actualizar_ejercicio,
    eliminar_ejercicio
)
from controllers.security import admin_required

ejercicio_bp = Blueprint("ejercicio", __name__)


def login_required():
    return "usuario_id" in session


@ejercicio_bp.route("/ejercicios")
def listar_ejercicios():
    proteccion = admin_required()
    if proteccion:
        return proteccion

    ejercicios = obtener_ejercicios()
    return render_template("ejercicios.html", ejercicios=ejercicios)


@ejercicio_bp.route("/ejercicios/crear", methods=["GET", "POST"])
def crear():
    proteccion = admin_required()
    if proteccion:
        return proteccion

    if request.method == "POST":
        nombre = request.form["nombre"]
        tipo = request.form["tipo"]
        try:
            calorias = int(request.form["calorias"])
        except ValueError:
            return render_template(
                "crear_ejercicio.html",
                error="Las calorías deben ser un número válido"
        )

        # Validaciones Back-End
        if len(nombre.strip()) < 3:
            return render_template(
                "crear_ejercicio.html",
                error="El nombre del ejercicio debe tener al menos 3 caracteres"
            )

        if calorias <= 0:
            return render_template(
                "crear_ejercicio.html",
                error="Las calorías deben ser mayores a 0"
            )

        crear_ejercicio(nombre, tipo, calorias)
        return redirect(url_for("ejercicio.listar_ejercicios"))

    return render_template("crear_ejercicio.html")


@ejercicio_bp.route("/ejercicios/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    proteccion = admin_required()
    if proteccion:
        return proteccion

    ejercicio = obtener_ejercicio_por_id(id)

    if request.method == "POST":
        nombre = request.form["nombre"]
        tipo = request.form["tipo"]
        try:
            calorias = int(request.form["calorias"])
        except ValueError:
            return render_template(
                "editar_ejercicio.html",
                ejercicio=ejercicio,
                error="Las calorías deben ser un número válido"
            )

        # Validaciones Back-End
        if len(nombre.strip()) < 3:
            return render_template(
                "editar_ejercicio.html",
                ejercicio=ejercicio,
                error="El nombre del ejercicio debe tener al menos 3 caracteres"
            )

        if calorias <= 0:
            return render_template(
                "editar_ejercicio.html",
                ejercicio=ejercicio,
                error="Las calorías deben ser mayores a 0"
            )

        actualizar_ejercicio(id, nombre, tipo, calorias)
        return redirect(url_for("ejercicio.listar_ejercicios"))

    return render_template("editar_ejercicio.html", ejercicio=ejercicio)


@ejercicio_bp.route("/ejercicios/eliminar/<int:id>")
def eliminar(id):
    proteccion = admin_required()
    if proteccion:
        return proteccion

    eliminar_ejercicio(id)
    return redirect(url_for("ejercicio.listar_ejercicios"))
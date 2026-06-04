from flask import Blueprint, render_template, request, redirect, url_for, session
from models.rutina_model import (
    obtener_rutinas,
    obtener_rutina_por_id,
    crear_rutina,
    actualizar_rutina,
    eliminar_rutina
)
from controllers.security import admin_required

rutina_bp = Blueprint("rutina", __name__)




@rutina_bp.route("/rutinas")
def listar_rutinas():
    proteccion = admin_required()
    if proteccion:
        return proteccion

    rutinas = obtener_rutinas()
    return render_template("rutinas.html", rutinas=rutinas)

    
@rutina_bp.route("/rutinas/crear", methods=["GET", "POST"])
def crear():
    proteccion = admin_required()
    if proteccion:
        return proteccion

    if request.method == "POST":
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]
        nivel = request.form["nivel"]
        objetivo = request.form["objetivo"]

        # Validación Back-End básica
        if len(nombre.strip()) < 3:
            return render_template(
                "crear_rutina.html",
                error="El nombre de la rutina debe tener al menos 3 caracteres"
            )

        crear_rutina(nombre, descripcion, nivel, objetivo)
        return redirect(url_for("rutina.listar_rutinas"))

    return render_template("crear_rutina.html")


@rutina_bp.route("/rutinas/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    proteccion = admin_required()
    if proteccion:
        return proteccion

    rutina = obtener_rutina_por_id(id)

    if request.method == "POST":
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]
        nivel = request.form["nivel"]
        objetivo = request.form["objetivo"]

        if len(nombre.strip()) < 3:
            return render_template(
                "editar_rutina.html",
                rutina=rutina,
                error="El nombre de la rutina debe tener al menos 3 caracteres"
            )

        actualizar_rutina(id, nombre, descripcion, nivel, objetivo)
        return redirect(url_for("rutina.listar_rutinas"))

    return render_template("editar_rutina.html", rutina=rutina)


@rutina_bp.route("/rutinas/eliminar/<int:id>")
def eliminar(id):
    proteccion = admin_required()
    if proteccion:
        return proteccion

    eliminar_rutina(id)
    return redirect(url_for("rutina.listar_rutinas"))
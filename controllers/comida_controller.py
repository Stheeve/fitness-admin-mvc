from flask import Blueprint, render_template, request, redirect, url_for, session
from models.comida_model import (
    obtener_comidas,
    obtener_comida_por_id,
    crear_comida,
    actualizar_comida,
    eliminar_comida
)
from controllers.security import admin_required

comida_bp = Blueprint("comida", __name__)


def login_required():
    return "usuario_id" in session


def validar_datos_comida(nombre, calorias, proteinas, carbohidratos, grasas):
    if len(nombre.strip()) < 3:
        return "El nombre de la comida debe tener al menos 3 caracteres"

    if calorias <= 0:
        return "Las calorías deben ser mayores a 0"

    if proteinas < 0:
        return "Las proteínas no pueden ser negativas"

    if carbohidratos < 0:
        return "Los carbohidratos no pueden ser negativos"

    if grasas < 0:
        return "Las grasas no pueden ser negativas"

    return None


@comida_bp.route("/comidas")
def listar_comidas():
    proteccion = admin_required()
    if proteccion:
        return proteccion

    comidas = obtener_comidas()
    return render_template("comidas.html", comidas=comidas)


@comida_bp.route("/comidas/crear", methods=["GET", "POST"])
def crear():
    proteccion = admin_required()
    if proteccion:
        return proteccion

    if request.method == "POST":
        nombre = request.form["nombre"]
        tipo = request.form["tipo"]

        try:
            calorias = int(request.form["calorias"])
            proteinas = float(request.form["proteinas"])
            carbohidratos = float(request.form["carbohidratos"])
            grasas = float(request.form["grasas"])
        except ValueError:
            return render_template(
                "crear_comida.html",
                error="Calorías, proteínas, carbohidratos y grasas deben ser valores numéricos"
            )

        error = validar_datos_comida(nombre, calorias, proteinas, carbohidratos, grasas)

        if error:
            return render_template("crear_comida.html", error=error)

        crear_comida(nombre, tipo, calorias, proteinas, carbohidratos, grasas)
        return redirect(url_for("comida.listar_comidas"))

    return render_template("crear_comida.html")


@comida_bp.route("/comidas/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    proteccion = admin_required()
    if proteccion:
        return proteccion

    comida = obtener_comida_por_id(id)

    if request.method == "POST":
        nombre = request.form["nombre"]
        tipo = request.form["tipo"]

        try:
            calorias = int(request.form["calorias"])
            proteinas = float(request.form["proteinas"])
            carbohidratos = float(request.form["carbohidratos"])
            grasas = float(request.form["grasas"])
        except ValueError:
            return render_template(
                "editar_comida.html",
                comida=comida,
                error="Calorías, proteínas, carbohidratos y grasas deben ser valores numéricos"
            )

        error = validar_datos_comida(nombre, calorias, proteinas, carbohidratos, grasas)

        if error:
            return render_template("editar_comida.html", comida=comida, error=error)

        actualizar_comida(id, nombre, tipo, calorias, proteinas, carbohidratos, grasas)
        return redirect(url_for("comida.listar_comidas"))

    return render_template("editar_comida.html", comida=comida)


@comida_bp.route("/comidas/eliminar/<int:id>")
def eliminar(id):
    proteccion = admin_required()
    if proteccion:
        return proteccion

    eliminar_comida(id)
    return redirect(url_for("comida.listar_comidas"))
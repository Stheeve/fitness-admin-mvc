from flask import Blueprint, render_template, request, redirect, url_for, session
from models.registro_comida_model import (
    obtener_registros_comida,
    crear_registro_comida,
    eliminar_registro_comida
)
from models.comida_model import obtener_comidas, obtener_comida_por_id
from controllers.security import usuario_required

registro_comida_bp = Blueprint("registro_comida", __name__)


def login_required():
    return "usuario_id" in session


@registro_comida_bp.route("/mis-comidas")
def listar():
    proteccion = usuario_required()
    if proteccion:
        return proteccion

    registros = obtener_registros_comida(session["usuario_id"])
    return render_template("mis_comidas.html", registros=registros)


@registro_comida_bp.route("/mis-comidas/crear", methods=["GET", "POST"])
def crear():
    proteccion = usuario_required()
    if proteccion:
        return proteccion

    comidas = obtener_comidas()

    if request.method == "POST":
        comida_id = request.form["comida_id"]
        fecha = request.form["fecha"]

        try:
            cantidad = float(request.form["cantidad"])
        except ValueError:
            return render_template(
                "crear_mi_comida.html",
                comidas=comidas,
                error="La cantidad debe ser un número válido"
            )

        if not comida_id:
            return render_template(
                "crear_mi_comida.html",
                comidas=comidas,
                error="Debe seleccionar una comida"
            )

        if cantidad <= 0:
            return render_template(
                "crear_mi_comida.html",
                comidas=comidas,
                error="La cantidad debe ser mayor a 0"
            )

        comida = obtener_comida_por_id(comida_id)

        if not comida:
            return render_template(
                "crear_mi_comida.html",
                comidas=comidas,
                error="La comida seleccionada no existe"
            )

        calorias_totales = comida["calorias"] * cantidad

        crear_registro_comida(
            session["usuario_id"],
            comida_id,
            fecha,
            cantidad,
            calorias_totales
        )

        return redirect(url_for("registro_comida.listar"))

    return render_template("crear_mi_comida.html", comidas=comidas)


@registro_comida_bp.route("/mis-comidas/eliminar/<int:id>")
def eliminar(id):
    proteccion = usuario_required()
    if proteccion:
        return proteccion

    eliminar_registro_comida(id, session["usuario_id"])
    return redirect(url_for("registro_comida.listar"))
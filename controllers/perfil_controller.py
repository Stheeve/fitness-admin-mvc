from flask import Blueprint, render_template, request, redirect, url_for, session
from models.perfil_model import ( obtener_perfil_por_usuario, crear_perfil, actualizar_perfil)
from controllers.security import usuario_required

perfil_bp = Blueprint("perfil", __name__)


def login_required():
    return "usuario_id" in session


def validar_perfil(edad, peso, altura):
    if edad < 12 or edad > 100:
        return "La edad debe estar entre 12 y 100 años"

    if peso <= 0:
        return "El peso debe ser mayor a 0"

    if altura <= 0:
        return "La altura debe ser mayor a 0"

    return None


@perfil_bp.route("/perfil", methods=["GET", "POST"])
def perfil():
    proteccion = usuario_required()
    if proteccion:
        return proteccion

    usuario_id = session["usuario_id"]
    perfil_existente = obtener_perfil_por_usuario(usuario_id)

    if request.method == "POST":
        try:
            edad = int(request.form["edad"])
            peso = float(request.form["peso"])
            altura = float(request.form["altura"])
        except ValueError:
            return render_template(
                "perfil.html",
                perfil=perfil_existente,
                error="Edad, peso y altura deben ser valores numéricos"
            )

        contextura = request.form["contextura"]
        nivel_actividad = request.form["nivel_actividad"]
        objetivo = request.form["objetivo"]

        error = validar_perfil(edad, peso, altura)

        if error:
            return render_template(
                "perfil.html",
                perfil=perfil_existente,
                error=error
            )

        if perfil_existente:
            actualizar_perfil(
                usuario_id, edad, peso, altura,
                contextura, nivel_actividad, objetivo
            )
        else:
            crear_perfil(
                usuario_id, edad, peso, altura,
                contextura, nivel_actividad, objetivo
            )

        return redirect(url_for("perfil.perfil"))

    return render_template("perfil.html", perfil=perfil_existente)
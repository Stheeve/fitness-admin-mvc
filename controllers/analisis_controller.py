from flask import Blueprint, render_template, session

from controllers.security import usuario_required
from core.services.analisis_service import AnalisisService


analisis_bp = Blueprint("analisis", __name__)

analisis_service = AnalisisService()


@analisis_bp.route("/analisis")
def ver_analisis():
    proteccion = usuario_required()

    if proteccion:
        return proteccion

    usuario_id = session["usuario_id"]

    resultado = analisis_service.ejecutar_analisis(
        usuario_id
    )

    if resultado.get("error"):
        return render_template(
            "analisis.html",
            error=resultado["error"]
        )

    return render_template(
        "analisis.html",
        **resultado
    )
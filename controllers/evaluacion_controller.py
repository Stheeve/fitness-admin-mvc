from flask import Blueprint, render_template, session

from controllers.security import usuario_required
from core.factories.evaluacion_factory import EvaluacionFactory

from models.recomendacion_model import (
    desactivar_recomendaciones,
    obtener_recomendacion_activa,
    actualizar_resultado_recomendacion
)

from models.analisis_model import (
    obtener_perfil_usuario,
    obtener_progresos_usuario
)


evaluacion_bp = Blueprint("evaluacion", __name__)


@evaluacion_bp.route("/evaluar-recomendacion")
def evaluar_recomendacion():
    # Verifica que el usuario tenga sesión y rol de usuario.
    proteccion = usuario_required()

    if proteccion:
        return proteccion

    # Obtiene el ID del usuario que inició sesión.
    usuario_id = session["usuario_id"]

    # Busca el perfil físico del usuario.
    perfil = obtener_perfil_usuario(usuario_id)

    if not perfil:
        return render_template(
            "evaluacion_recomendacion.html",
            error="Primero debes registrar tu perfil físico."
        )

    # Busca la recomendación activa del usuario.
    recomendacion = obtener_recomendacion_activa(usuario_id)

    if not recomendacion:
        return render_template(
            "evaluacion_recomendacion.html",
            error=(
                "No tienes una recomendación activa. "
                "Primero ejecuta el análisis."
            )
        )

    # Obtiene todos los progresos ordenados cronológicamente.
    progresos = obtener_progresos_usuario(usuario_id)

    # Factory selecciona la estrategia correspondiente al objetivo.
    estrategia = EvaluacionFactory.crear_estrategia(
        perfil["objetivo"]
    )

    # Strategy evalúa el progreso del usuario.
    evaluacion = estrategia.evaluar(progresos)

    # Solo actualiza la recomendación cuando hay suficientes progresos.
    if evaluacion["resultado"] != "pendiente":
        actualizar_resultado_recomendacion(
            recomendacion["id"],
            evaluacion["resultado"],
            evaluacion["mensaje"]
        )

        # Si no funcionó, finaliza la recomendación activa.
        if evaluacion["resultado"] == "no funciono":
            desactivar_recomendaciones(usuario_id)

    return render_template(
        "evaluacion_recomendacion.html",
        perfil=perfil,
        recomendacion=recomendacion,
        evaluacion=evaluacion,
        progresos=progresos
    )
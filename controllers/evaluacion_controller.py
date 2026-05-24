from flask import Blueprint, render_template, redirect, url_for, session
from controllers.security import usuario_required

from models.recomendacion_model import (
    obtener_recomendacion_activa,
    actualizar_resultado_recomendacion
)

from models.analisis_model import (
    obtener_perfil_usuario,
    obtener_progresos_usuario
)


evaluacion_bp = Blueprint("evaluacion", __name__)


def evaluar_si_funciono(objetivo, progresos):
    if len(progresos) < 2:
        return {
            "resultado": "pendiente",
            "mensaje": "No existen suficientes registros de progreso para evaluar la recomendación.",
            "peso_inicial": None,
            "peso_final": None,
            "grasa_inicial": None,
            "grasa_final": None
        }

    primer_registro = progresos[0]
    ultimo_registro = progresos[-1]

    peso_inicial = primer_registro["peso_actual"]
    peso_final = ultimo_registro["peso_actual"]

    grasa_inicial = primer_registro["porcentaje_grasa"]
    grasa_final = ultimo_registro["porcentaje_grasa"]

    funciono = False

    if objetivo == "Ganar masa muscular":
        funciono = peso_final > peso_inicial and grasa_final <= grasa_inicial

    elif objetivo == "Perder peso":
        funciono = peso_final < peso_inicial and grasa_final < grasa_inicial

    elif objetivo == "Mejorar resistencia":
        funciono = grasa_final <= grasa_inicial

    elif objetivo == "Mantener condición física":
        funciono = abs(peso_final - peso_inicial) <= 2

    if funciono:
        resultado = "funciono"
        mensaje = "La recomendación está funcionando. Se sugiere continuar con la rutina y alimentación actual."
    else:
        resultado = "no funciono"
        mensaje = "La recomendación no muestra mejoras suficientes. Se recomienda ejecutar nuevamente el análisis para ajustar la rutina y alimentación."

    return {
        "resultado": resultado,
        "mensaje": mensaje,
        "peso_inicial": peso_inicial,
        "peso_final": peso_final,
        "grasa_inicial": grasa_inicial,
        "grasa_final": grasa_final
    }


@evaluacion_bp.route("/evaluar-recomendacion")
def evaluar_recomendacion():
    proteccion = usuario_required()
    if proteccion:
        return proteccion

    usuario_id = session["usuario_id"]

    perfil = obtener_perfil_usuario(usuario_id)

    if not perfil:
        return render_template(
            "evaluacion_recomendacion.html",
            error="Primero debes registrar tu perfil físico."
        )

    recomendacion = obtener_recomendacion_activa(usuario_id)

    if not recomendacion:
        return render_template(
            "evaluacion_recomendacion.html",
            error="No tienes una recomendación activa. Primero ejecuta el análisis."
        )

    progresos = obtener_progresos_usuario(usuario_id)

    evaluacion = evaluar_si_funciono(perfil["objetivo"], progresos)

    if evaluacion["resultado"] != "pendiente":
        actualizar_resultado_recomendacion(
            recomendacion["id"],
            evaluacion["resultado"],
            evaluacion["mensaje"]
        )

    return render_template(
        "evaluacion_recomendacion.html",
        perfil=perfil,
        recomendacion=recomendacion,
        evaluacion=evaluacion,
        progresos=progresos
    )
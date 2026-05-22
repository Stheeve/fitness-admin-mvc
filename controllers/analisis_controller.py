from flask import Blueprint, render_template, session
from controllers.security import usuario_required
from datetime import date

from models.analisis_model import (
    obtener_perfil_usuario,
    obtener_otros_perfiles,
    obtener_progresos_usuario,
    obtener_comidas_usuario,
    obtener_rutinas_por_objetivo
)

from models.recomendacion_model import (
    obtener_recomendacion_activa,
    guardar_recomendacion
)


analisis_bp = Blueprint("analisis", __name__)


def evaluar_exito(objetivo, progresos):
    if len(progresos) < 2:
        return False

    primer_registro = progresos[0]
    ultimo_registro = progresos[-1]

    peso_inicial = primer_registro["peso_actual"]
    peso_final = ultimo_registro["peso_actual"]

    grasa_inicial = primer_registro["porcentaje_grasa"]
    grasa_final = ultimo_registro["porcentaje_grasa"]

    if objetivo == "Ganar masa muscular":
        return peso_final > peso_inicial and grasa_final <= grasa_inicial

    if objetivo == "Perder peso":
        return peso_final < peso_inicial and grasa_final < grasa_inicial

    if objetivo == "Mejorar resistencia":
        return grasa_final <= grasa_inicial

    if objetivo == "Mantener condición física":
        return abs(peso_final - peso_inicial) <= 2

    return False


def calcular_cambio_peso(progresos):
    if len(progresos) < 2:
        return 0

    peso_inicial = progresos[0]["peso_actual"]
    peso_final = progresos[-1]["peso_actual"]

    return round(peso_final - peso_inicial, 2)


@analisis_bp.route("/analisis")
def ver_analisis():
    proteccion = usuario_required()
    if proteccion:
        return proteccion

    usuario_id = session["usuario_id"]

    perfil_actual = obtener_perfil_usuario(usuario_id)

    if not perfil_actual:
        return render_template(
            "analisis.html",
            error="Primero debes registrar tu perfil físico para realizar el análisis."
        )

    otros_perfiles = obtener_otros_perfiles(usuario_id)

    usuarios_similares = []
    casos_exitosos = []
    comidas_recomendadas = []

    # Rutinas sugeridas según el objetivo del usuario
    rutinas_recomendadas = obtener_rutinas_por_objetivo(perfil_actual["objetivo"])

    # Buscar si el usuario ya tiene una recomendación activa
    recomendacion_activa = obtener_recomendacion_activa(usuario_id)

    # Si no tiene recomendación activa, se guarda una automáticamente
    if rutinas_recomendadas and not recomendacion_activa:
        rutina_sugerida = rutinas_recomendadas[0]

        guardar_recomendacion(
            usuario_id,
            rutina_sugerida["id"],
            date.today(),
            "Recomendación generada automáticamente según el análisis de usuarios similares."
        )

        recomendacion_activa = obtener_recomendacion_activa(usuario_id)

    # FOREACH 1: recorrer todos los perfiles registrados y comparar con el usuario actual
    for perfil in otros_perfiles:
        coincidencias = 0

        if perfil["objetivo"] == perfil_actual["objetivo"]:
            coincidencias += 1

        if perfil["contextura"] == perfil_actual["contextura"]:
            coincidencias += 1

        if perfil["nivel_actividad"] == perfil_actual["nivel_actividad"]:
            coincidencias += 1

        if abs(perfil["edad"] - perfil_actual["edad"]) <= 5:
            coincidencias += 1

        if abs(perfil["peso"] - perfil_actual["peso"]) <= 10:
            coincidencias += 1

        if abs(perfil["altura"] - perfil_actual["altura"]) <= 10:
            coincidencias += 1

        # Se considera similar si cumple al menos 4 coincidencias
        if coincidencias >= 4:
            progresos = obtener_progresos_usuario(perfil["usuario_id"])
            cambio_peso = calcular_cambio_peso(progresos)

            usuario_similar = {
                "usuario_id": perfil["usuario_id"],
                "username": perfil["username"],
                "edad": perfil["edad"],
                "peso": perfil["peso"],
                "altura": perfil["altura"],
                "contextura": perfil["contextura"],
                "nivel_actividad": perfil["nivel_actividad"],
                "objetivo": perfil["objetivo"],
                "coincidencias": coincidencias,
                "cambio_peso": cambio_peso
            }

            usuarios_similares.append(usuario_similar)

            # FOREACH 2: evaluar si el usuario similar fue un caso exitoso
            if evaluar_exito(perfil_actual["objetivo"], progresos):
                casos_exitosos.append(usuario_similar)

                comidas = obtener_comidas_usuario(perfil["usuario_id"])

                # FOREACH 3: recopilar comidas usadas por usuarios exitosos
                for comida in comidas:
                    comidas_recomendadas.append(comida)

    total_similares = len(usuarios_similares)
    total_exitosos = len(casos_exitosos)

    promedio_cambio = 0

    # FOREACH 4: calcular promedio de cambio de peso en casos exitosos
    if total_exitosos > 0:
        suma_cambios = 0

        for caso in casos_exitosos:
            suma_cambios += caso["cambio_peso"]

        promedio_cambio = round(suma_cambios / total_exitosos, 2)

    return render_template(
        "analisis.html",
        perfil_actual=perfil_actual,
        usuarios_similares=usuarios_similares,
        casos_exitosos=casos_exitosos,
        comidas_recomendadas=comidas_recomendadas,
        rutinas_recomendadas=rutinas_recomendadas,
        recomendacion_activa=recomendacion_activa,
        total_similares=total_similares,
        total_exitosos=total_exitosos,
        promedio_cambio=promedio_cambio
    )
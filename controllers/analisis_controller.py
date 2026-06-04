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
    guardar_recomendacion,
    obtener_ultima_recomendacion_no_funciono,
    obtener_rutinas_exitosas_usuario
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

    # guarda rutinas exitosas de usuarios similares
    rutinas_recomendadas = []

    # Respaldo por si todavía no existen rutinas exitosas guardadas.
    rutinas_respaldo = obtener_rutinas_por_objetivo(perfil_actual["objetivo"])

    recomendacion_activa = obtener_recomendacion_activa(usuario_id)

    # recorrer todos los perfiles registrados
    for perfil in otros_perfiles:
        coincidencias = 0

        # Comparar características del usuario actual con cada perfil
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

        # Si tiene suficientes coincidencias, se considera usuario similar
        if coincidencias >= 4:
            progresos = obtener_progresos_usuario(perfil["usuario_id"])

            peso_inicial = None
            peso_final = None
            grasa_inicial = None
            grasa_final = None

            # recorrer historial de progreso del usuario similar
            for indice, progreso in enumerate(progresos):
                if indice == 0:
                    peso_inicial = progreso["peso_actual"]
                    grasa_inicial = progreso["porcentaje_grasa"]

                peso_final = progreso["peso_actual"]
                grasa_final = progreso["porcentaje_grasa"]

            cambio_peso = 0

            if peso_inicial is not None and peso_final is not None:
                cambio_peso = round(peso_final - peso_inicial, 2)

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

            usuario_exitoso = False

            if len(progresos) >= 2:
                if perfil_actual["objetivo"] == "Ganar masa muscular":
                    usuario_exitoso = peso_final > peso_inicial and grasa_final <= grasa_inicial

                elif perfil_actual["objetivo"] == "Perder peso":
                    usuario_exitoso = peso_final < peso_inicial and grasa_final < grasa_inicial

                elif perfil_actual["objetivo"] == "Mejorar resistencia":
                    usuario_exitoso = grasa_final <= grasa_inicial

                elif perfil_actual["objetivo"] == "Mantener condición física":
                    usuario_exitoso = abs(peso_final - peso_inicial) <= 2

            if usuario_exitoso:
                casos_exitosos.append(usuario_similar)

                # Obtener rutinas que sí funcionaron a este usuario similar
                rutinas_exitosas = obtener_rutinas_exitosas_usuario(perfil["usuario_id"])

                #  recorrer rutinas exitosas del usuario similar
                for rutina in rutinas_exitosas:
                    rutinas_recomendadas.append(rutina)

                comidas = obtener_comidas_usuario(perfil["usuario_id"])

                #recorrer comidas consumidas del usuario exitoso
                for comida in comidas:
                    comida_recomendada = {
                        "nombre": comida["nombre"],
                        "tipo": comida["tipo"],
                        "calorias": comida["calorias"],
                        "cantidad": comida["cantidad"],
                        "calorias_totales": comida["calorias_totales"],
                        "usuario_origen": perfil["username"]
                    }

                    comidas_recomendadas.append(comida_recomendada)

    # Si no hay rutinas exitosas de usuarios similares usar rutinas por objetivo como respaldo
    if len(rutinas_recomendadas) == 0:
        rutinas_recomendadas = rutinas_respaldo

    # Guardar recomendación activa evitando repetir la última que no funcionó
    if rutinas_recomendadas and not recomendacion_activa:
        ultima_fallida = obtener_ultima_recomendacion_no_funciono(usuario_id)

        rutina_sugerida = None

        # recorrer rutinas recomendadas y evitar repetir la última fallida
        for rutina in rutinas_recomendadas:
            rutina_id = rutina.get("id") or rutina.get("rutina_id")

            if not ultima_fallida or rutina_id != ultima_fallida["rutina_id"]:
                rutina_sugerida = rutina
                break

        # Si todas coinciden o solo hay una, usar la primera disponible
        if not rutina_sugerida:
            rutina_sugerida = rutinas_recomendadas[0]

        rutina_id_final = rutina_sugerida.get("id") or rutina_sugerida.get("rutina_id")

        guardar_recomendacion(
            usuario_id,
            rutina_id_final,
            date.today(),
            "Recomendación generada según rutinas exitosas de usuarios similares."
        )

        recomendacion_activa = obtener_recomendacion_activa(usuario_id)

    total_similares = len(usuarios_similares)
    total_exitosos = len(casos_exitosos)

    promedio_cambio = 0

    # recorrer casos exitosos y calcular promedio de cambio de peso
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
from datetime import date

from core.factories.evaluacion_factory import EvaluacionFactory

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


class AnalisisService:
    """
    Servicio responsable de ejecutar la lógica del core.
    """

    MINIMO_COINCIDENCIAS = 4
    DIFERENCIA_MAXIMA_EDAD = 5
    DIFERENCIA_MAXIMA_PESO = 10
    DIFERENCIA_MAXIMA_ALTURA = 10

    def ejecutar_analisis(self, usuario_id):
        perfil_actual = obtener_perfil_usuario(usuario_id)

        if not perfil_actual:
            return {
                "error": (
                    "Primero debes registrar tu perfil físico."
                )
            }

        otros_perfiles = obtener_otros_perfiles(usuario_id)

        usuarios_similares = []
        casos_exitosos = []
        comidas_recomendadas = []
        rutinas_recomendadas = []

        estrategia = EvaluacionFactory.crear_estrategia(
            perfil_actual["objetivo"]
        )

        for perfil in otros_perfiles:
            if perfil["objetivo"] != perfil_actual["objetivo"]:
                continue
            coincidencias = self.calcular_coincidencias(
                perfil_actual,
                perfil
            )

            if coincidencias < self.MINIMO_COINCIDENCIAS:
                continue

            progresos = obtener_progresos_usuario(
                perfil["usuario_id"]
            )

            evaluacion = estrategia.evaluar(progresos)

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
                "cambio_peso": evaluacion["cambio_peso"]
            }

            usuarios_similares.append(usuario_similar)

            if evaluacion["resultado"] != "funciono":
                continue

            casos_exitosos.append(usuario_similar)

            rutinas_exitosas = (
                obtener_rutinas_exitosas_usuario(
                    perfil["usuario_id"]
                )
            )

            for rutina in rutinas_exitosas:
                self.agregar_rutina_sin_duplicar(
                    rutinas_recomendadas,
                    rutina
                )

            comidas = obtener_comidas_usuario(
                perfil["usuario_id"]
            )

            for comida in comidas:
                comidas_recomendadas.append({
                    "nombre": comida["nombre"],
                    "tipo": comida["tipo"],
                    "calorias": comida["calorias"],
                    "cantidad": comida["cantidad"],
                    "calorias_totales": (
                        comida["calorias_totales"]
                    ),
                    "usuario_origen": perfil["username"]
                })

        if not rutinas_recomendadas:
            rutinas_recomendadas = (
                obtener_rutinas_por_objetivo(
                    perfil_actual["objetivo"]
                )
            )

        recomendacion_activa = (
            obtener_recomendacion_activa(usuario_id)
        )

        if rutinas_recomendadas and not recomendacion_activa:
            rutina_sugerida = self.seleccionar_rutina(
                usuario_id,
                rutinas_recomendadas
            )

            if rutina_sugerida:
                rutina_id = self.obtener_id_rutina(
                    rutina_sugerida
                )

                guardar_recomendacion(
                    usuario_id,
                    rutina_id,
                    date.today(),
                    (
                        "Recomendación generada según usuarios "
                        "similares exitosos."
                    )
                )

                recomendacion_activa = (
                    obtener_recomendacion_activa(usuario_id)
                )
        comidas_mas_consumidas = self.agrupar_comidas(
        comidas_recomendadas
        )
        return {
            "perfil_actual": perfil_actual,
            "usuarios_similares": usuarios_similares,
            "casos_exitosos": casos_exitosos,
            "comidas_recomendadas": comidas_mas_consumidas,
            "rutinas_recomendadas": rutinas_recomendadas,
            "recomendacion_activa": recomendacion_activa,
            "total_similares": len(usuarios_similares),
            "total_exitosos": len(casos_exitosos),
            "promedio_cambio": self.calcular_promedio(
                casos_exitosos
            )
        }

    def calcular_coincidencias(
        self,
        perfil_actual,
        perfil_comparado
    ):
        coincidencias = 0


        if (
            perfil_actual["contextura"]
            == perfil_comparado["contextura"]
        ):
            coincidencias += 1

        if (
            perfil_actual["nivel_actividad"]
            == perfil_comparado["nivel_actividad"]
        ):
            coincidencias += 1

        if abs(
            int(perfil_actual["edad"])
            - int(perfil_comparado["edad"])
        ) <= self.DIFERENCIA_MAXIMA_EDAD:
            coincidencias += 1

        if abs(
            float(perfil_actual["peso"])
            - float(perfil_comparado["peso"])
        ) <= self.DIFERENCIA_MAXIMA_PESO:
            coincidencias += 1

        if abs(
            float(perfil_actual["altura"])
            - float(perfil_comparado["altura"])
        ) <= self.DIFERENCIA_MAXIMA_ALTURA:
            coincidencias += 1

        return coincidencias

    def obtener_id_rutina(self, rutina):
        return rutina.get("id") or rutina.get("rutina_id")

    def agregar_rutina_sin_duplicar(
        self,
        lista_rutinas,
        nueva_rutina
    ):
        nueva_id = self.obtener_id_rutina(nueva_rutina)

        for rutina in lista_rutinas:
            if self.obtener_id_rutina(rutina) == nueva_id:
                return

        lista_rutinas.append(nueva_rutina)

    def seleccionar_rutina(self, usuario_id, rutinas):
        ultima_fallida = (
            obtener_ultima_recomendacion_no_funciono(
                usuario_id
            )
        )

        for rutina in rutinas:
            rutina_id = self.obtener_id_rutina(rutina)

            if not ultima_fallida:
                return rutina

            if rutina_id != ultima_fallida["rutina_id"]:
                return rutina

        return rutinas[0] if rutinas else None

    def calcular_promedio(self, casos_exitosos):
        if not casos_exitosos:
            return 0

        suma = 0

        for caso in casos_exitosos:
            suma += caso["cambio_peso"]

        return round(
            suma / len(casos_exitosos),
            2
        )
        
    def agrupar_comidas(self, comidas):
        resumen = {}

        for comida in comidas:
            nombre = comida["nombre"]

            if nombre not in resumen:
                resumen[nombre] = {
                    "nombre": comida["nombre"],
                    "tipo": comida["tipo"],
                    "calorias": comida["calorias"],
                    "veces_consumida": 0,
                    "cantidad_total": 0,
                    "calorias_totales": 0,
                    "usuarios": set()
                }

            resumen[nombre]["veces_consumida"] += 1
            resumen[nombre]["cantidad_total"] += float(
                comida["cantidad"]
            )
            resumen[nombre]["calorias_totales"] += float(
                comida["calorias_totales"]
            )
            resumen[nombre]["usuarios"].add(
                comida["usuario_origen"]
            )

        comidas_agrupadas = []

        for comida in resumen.values():
            comida["cantidad_total"] = round(
                comida["cantidad_total"],
                2
            )

            comida["calorias_totales"] = round(
                comida["calorias_totales"],
                2
            )

            comida["total_usuarios"] = len(
                comida["usuarios"]
            )

            comida["usuarios"] = ", ".join(
                sorted(comida["usuarios"])
            )

            comidas_agrupadas.append(comida)

        comidas_agrupadas.sort(
            key=lambda comida: comida["veces_consumida"],
            reverse=True
        )

        return comidas_agrupadas
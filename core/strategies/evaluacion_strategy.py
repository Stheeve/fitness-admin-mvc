from abc import ABC, abstractmethod


class EvaluacionStrategy(ABC):
    """
    Clase base del patrón Strategy.
    Define el contrato común para evaluar el progreso.
    """

    @abstractmethod
    def cumple_objetivo(
        self,
        peso_inicial,
        peso_final,
        grasa_inicial,
        grasa_final
    ):
        pass

    def evaluar(self, progresos):
        """
        Obtiene el primer y último progreso
        y delega la condición de éxito a la estrategia concreta.
        """

        if len(progresos) < 2:
            return {
                "resultado": "pendiente",
                "funciono": False,
                "mensaje": "No existen suficientes registros de progreso.",
                "peso_inicial": None,
                "peso_final": None,
                "grasa_inicial": None,
                "grasa_final": None,
                "cambio_peso": 0
            }

        primer_registro = progresos[0]
        ultimo_registro = progresos[-1]

        peso_inicial = float(primer_registro["peso_actual"])
        peso_final = float(ultimo_registro["peso_actual"])

        grasa_inicial = float(
            primer_registro["porcentaje_grasa"]
        )

        grasa_final = float(
            ultimo_registro["porcentaje_grasa"]
        )

        funciono = self.cumple_objetivo(
            peso_inicial,
            peso_final,
            grasa_inicial,
            grasa_final
        )

        if funciono:
            resultado = "funciono"
            mensaje = (
                "La recomendación produjo el progreso esperado."
            )
        else:
            resultado = "no funciono"
            mensaje = (
                "La recomendación no produjo el progreso esperado."
            )

        return {
            "resultado": resultado,
            "funciono": funciono,
            "mensaje": mensaje,
            "peso_inicial": peso_inicial,
            "peso_final": peso_final,
            "grasa_inicial": grasa_inicial,
            "grasa_final": grasa_final,
            "cambio_peso": round(
                peso_final - peso_inicial,
                2
            )
        }


class GanarMasaMuscularStrategy(EvaluacionStrategy):

    def cumple_objetivo(
        self,
        peso_inicial,
        peso_final,
        grasa_inicial,
        grasa_final
    ):
        return (
            peso_final > peso_inicial
            and grasa_final <= grasa_inicial
        )


class PerderPesoStrategy(EvaluacionStrategy):

    def cumple_objetivo(
        self,
        peso_inicial,
        peso_final,
        grasa_inicial,
        grasa_final
    ):
        return (
            peso_final < peso_inicial
            and grasa_final < grasa_inicial
        )


class MejorarResistenciaStrategy(EvaluacionStrategy):

    def cumple_objetivo(
        self,
        peso_inicial,
        peso_final,
        grasa_inicial,
        grasa_final
    ):
        return grasa_final <= grasa_inicial



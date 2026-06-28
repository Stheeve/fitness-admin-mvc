from core.strategies.evaluacion_strategy import (
    GanarMasaMuscularStrategy,
    PerderPesoStrategy,
    MejorarResistenciaStrategy
)


class EvaluacionFactory:

    _estrategias = {
        "Ganar masa muscular": GanarMasaMuscularStrategy,
        "Perder peso": PerderPesoStrategy,
        "Mejorar resistencia": MejorarResistenciaStrategy
    }

    @classmethod
    def crear_estrategia(cls, objetivo):
        estrategia_clase = cls._estrategias.get(objetivo)

        if estrategia_clase is None:
            raise ValueError(
                f"No existe una estrategia para el objetivo: {objetivo}"
            )

        return estrategia_clase()
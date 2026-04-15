try:
    import ollama
    OLLAMA_AVAILABLE = True
except Exception:
    OLLAMA_AVAILABLE = False
from .traductor_crimenes_service import traductor_datosCrimen


def generar_cronica(datos: dict, prediccion: dict = None, etiquetas: dict = None) -> str:
    if not OLLAMA_AVAILABLE:

        sexo = datos.get("Vict Sex", "")
        edad = datos.get("Vict Age", 0)
        arma = datos.get("Weapon Desc", "").upper()

        # ── género ─────────────────────────
        if sexo == "F":
            sujeto = "ella"
            victima = "la víctima"
            if edad <= 12:
                victima = "la niña"
        else:
            sujeto = "él"
            victima = "el hombre"

        # ── arma ───────────────────────────
        if "GUN" in arma:
            arma_txt = "un arma de fuego"
        elif "VEHICLE" in arma:
            arma_txt = "un vehículo"
        else:
            arma_txt = "un objeto desconocido"

        # ── narrativa simple coherente ─────
        texto = (
            f"{victima.capitalize()} fue encontrada en la escena. "
            f"{sujeto.capitalize()} no tuvo oportunidad de reaccionar. "
            f"El crimen involucró {arma_txt}. "
            f"La investigación sigue abierta."
        )

        return texto


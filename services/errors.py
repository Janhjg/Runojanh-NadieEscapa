from fastapi import HTTPException

# =============================================
# 400 — BAD REQUEST
# Caso ya resuelto / datos inconsistentes
# =============================================
 
def error_400(detalle: str):
    raise HTTPException(
        status_code=400,
        detail={
            "error": "BAD_REQUEST",
            "codigo": 400,
            "mensaje": detalle
        }
    )
 
 
# =============================================
# 404 — NOT FOUND
# ID no encontrado en el dataset
# =============================================
 
def error_404(detalle: str):
    raise HTTPException(
        status_code=404,
        detail={
            "error": "NOT_FOUND",
            "codigo": 404,
            "mensaje": detalle
        }
    )
 
 
# =============================================
# 422 — UNPROCESSABLE ENTITY
# Validacion fallida / campos incorrectos
# =============================================
 
def error_422(detalle: str):
    raise HTTPException(
        status_code=422,
        detail={
            "error": "VALIDATION_ERROR",
            "codigo": 422,
            "mensaje": detalle
        }
    )
 
 
# =============================================
# 503 — SERVICE UNAVAILABLE
# Fallo de HuggingFace o IA Generativa
# =============================================
 
def error_503(detalle: str):
    raise HTTPException(
        status_code=503,
        detail={
            "error": "SERVICE_UNAVAILABLE",
            "codigo": 503,
            "mensaje": detalle
        }
    )
 
 
# =============================================
# 504 — GATEWAY TIMEOUT
# Timeout de la IA Generativa
# =============================================
 
def error_504(detalle: str):
    raise HTTPException(
        status_code=504,
        detail={
            "error": "GATEWAY_TIMEOUT",
            "codigo": 504,
            "mensaje": detalle
        }
    )